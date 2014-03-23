import paramiko
import getpass


def ssh_connection(user, host, port=22, password=None, key_filename=None):
    """
    with password='' you will be prompted for a password when the script runs
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password == '':
        # ask for one on stdin
        password = getpass.getpass('Password for %s@%s: ' % (user, host))
    ssh.connect(host, port=port, username=user, password=password, key_filename=key_filename)
    # custom attributes
    ssh.user = user
    if user == 'root':
        ssh.homedir = '/root'
    else:
        ssh.homedir = '/home/%s' % user
    ssh.password = password
    ssh.use_sudo = False
    return ssh


def run_remote(ssh, cmd, check_exit_status=True, verbose=True):
    chan = ssh.get_transport().open_session()
    stdin = chan.makefile('wb')
    stdout = chan.makefile('rb')
    stderr = chan.makefile_stderr('rb')
    processed_cmd = cmd
    if ssh.use_sudo:
        processed_cmd = 'sudo -S bash -c "%s"' % cmd.replace('"', '\\"')
    chan.exec_command(processed_cmd)
    if stdout.channel.closed is False: # If stdout is still open then sudo is asking us for a password
        stdin.write('%s\n' % ssh.password)
        stdin.flush()
    result = {
        'stdout': [],
        'stderr': [],
    }
    exit_status = chan.recv_exit_status()
    result['exit_status'] = exit_status
    def print_output():
        for line in stdout:
            result['stdout'].append(line)
            print line,
        for line in stderr:
            result['stderr'].append(line)
            print line,
    if check_exit_status and exit_status != 0:
        print_output()
        print 'non-zero exit status (%d) when running "%s"' % (exit_status, cmd)
        exit(exit_status)
    if verbose:
        print_output()
    return result
