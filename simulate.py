from materials import *
from sshUtil import *
import os, sys
import matplotlib.pyplot as plt
import numpy as np

from PyQt4.QtCore import *


class RemoteSimulator(QThread):

    def __init__(self):
        QThread.__init__(self)

        self.materials_file = 'design-a-reactor-materials.hdf5'
        self.input_file = 'design-a-reactor.py'
        self.flux1_file = 'fsr-flux-group-1.png'
        self.flux7_file = 'fsr-flux-group-7.png'

        # NOTE: Need to query local path, and ignore remote path
        self.remote_path = ''
        self.local_path = ''

        # NOTE: What file will we use this time?
        self.output_file = 'output.txt'

        # NOTE: Need to query host, username and password and cache it
        self.port = 22
        self.host = 'mightywboyd.mit.edu'
        self.uname = ''
        self.pwd = ''

    def spawnSimulationThread(self):
        self.start()


    def run(self):

        # Copy the materials and input files to the cluster
        print 'Transferring input to workstation...'
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.uname, password=self.pwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(self.materials_file, self.materials_file)
        sftp.put(self.input_file, self.input_file)
        sftp.close()
        transport.close()

        # Setup a ssh connection for root and ask for the password interactively
        print 'Running OpenMOC on the GPU...'
        myconn = ssh_connection(self.uname, self.host, password=self.pwd)

        run_remote(myconn,
                    """
                    rm -rf log/ plots/
                    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-5.5/lib64/
                    export PATH=$PATH:/usr/local/cuda-5.5/bin/
                    python design-a-reactor.py -a 16 -t 8 --tolerance=1E-3
                    mv log/openmoc* log/output.txt
                    """)

        # Copy thermal flux plot to local directory
        print 'Retrieving output data...'
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.uname, password=self.pwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get('plots/' + self.flux1_file, self.flux1_file)
        sftp.get('plots/' + self.flux7_file, self.flux7_file)
        sftp.get('log/' + self.output_file, self.output_file)
        sftp.close()
        transport.close()

        self.processData()


    def processData(self):
        print 'Processing output data...'

        # Parse the output file with keff at each iteration
        data = open(self.output_file, "r" )
        keffs = []
        for line in data:
            tokens = line.split()
            if 'k_eff' not in tokens:
                continue
            else:
                keffs.append(float(tokens[7]))

        keffs = np.array(keffs)

        # Generate a scatter plot for keff convergence
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot([0.0, keffs.size], [1.0, 1.0], linestyle='-', linewidth='4')
        ax1.scatter(range(keffs.size), keffs, color='tomato');
        ax1.set_title('Multiplication Factor Convergence',fontsize=20)
        ax1.set_xlabel('Iteration #',fontsize=16)
        ax1.set_ylabel('Multiplication Factor',fontsize=16)
        ax1.set_xlim([0, keffs.size])
        ax1.grid(True, linestyle='-',color='1.0')
        ax1.legend(['Critical', 'Your Reactor'], loc=10)

        # Overlay txt to inform the user whether the reactor is critical
        # subcritical or super-critical
        if abs(keffs[keffs.size-1] - 1.0) < 1E-4:
            plt.figtext(0.42, 0.3, 'Critical!!!', fontsize=24)
            plt.figtext(0.43, 0.35, 'k = 1.0', fontsize=24)
        elif keffs[keffs.size-1] < 1.0:
            plt.figtext(0.40, 0.3, 'Sub-critical', fontsize=24)
            plt.figtext(0.39, 0.35, 'k = ' + str(keffs[keffs.size-1]), fontsize=24)
        else:
            plt.figtext(0.38, 0.3, 'Super-critical', fontsize=24)
            plt.figtext(0.38, 0.35, 'k = ' + str(keffs[keffs.size-1]), fontsize=24)    

        # Save plot and display to screen
        plt.savefig('keff.png', bbox_inches='tight')



class LocalSimulator(QThread):

    def __init__(self):
        QThread.__init__(self)

        self.materials_file = 'design-a-reactor-materials.hdf5'
        self.input_file = 'design-a-reactor.py'
        self.flux1_file = 'fsr-flux-group-1.png'
        self.flux7_file = 'fsr-flux-group-7.png'

        # NOTE: Need to query local path, and ignore remote path
        self.remote_path = ''
        self.local_path = ''

        # NOTE: What file will we use this time?
        self.output_file = 'output.txt'


    def spawnSimulationThread(self):
        self.start()


    def run(self):

        os.system('rm -rf log/ plots/')
        os.system('python design-a-reactor.py -a 16 -t 8 --tolerance=1E-3 -f True')
        os.system('mv plots/%s %s' % (self.flux1_file, self.flux1_file))
        os.system('mv plots/%s %s' % (self.flux7_file, self.flux7_file))
        os.system('mv log/openmoc* log/output.txt')
        os.system('cp log/%s output.txt' % self.output_file)

        self.processData()


    def processData(self):
        print 'Processing output data...'

        # Parse the output file with keff at each iteration
        data = open(self.output_file, "r" )
        keffs = []
        for line in data:
            tokens = line.split()
            if 'k_eff' not in tokens:
                continue
            else:
                keffs.append(float(tokens[7]))

        keffs = np.array(keffs)

        # Generate a scatter plot for keff convergence
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot([0.0, keffs.size], [1.0, 1.0], linestyle='-', linewidth='4')
        ax1.scatter(range(keffs.size), keffs, color='tomato');
        ax1.set_title('Multiplication Factor Convergence',fontsize=20)
        ax1.set_xlabel('Iteration #',fontsize=16)
        ax1.set_ylabel('Multiplication Factor',fontsize=16)
        ax1.set_xlim([0, keffs.size])
        ax1.grid(True, linestyle='-',color='1.0')
        ax1.legend(['Critical', 'Your Reactor'], loc=10)

        # Overlay txt to inform the user whether the reactor is critical
        # subcritical or super-critical
        if abs(keffs[keffs.size-1] - 1.0) < 1E-4:
            plt.figtext(0.42, 0.3, 'Critical!!!', fontsize=24)
            plt.figtext(0.43, 0.35, 'k = 1.0', fontsize=24)
        elif keffs[keffs.size-1] < 1.0:
            plt.figtext(0.40, 0.3, 'Sub-critical', fontsize=24)
            plt.figtext(0.39, 0.35, 'k = ' + str(keffs[keffs.size-1]), fontsize=24)
        else:
            plt.figtext(0.38, 0.3, 'Super-critical', fontsize=24)
            plt.figtext(0.38, 0.35, 'k = ' + str(keffs[keffs.size-1]), fontsize=24)    

        # Save plot and display to screen
        plt.savefig('keff.png', bbox_inches='tight')

