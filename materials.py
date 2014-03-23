'''
    This file manipulates the materials data (multi-group nuclear 
    cross-sections) for the OECD's C5G7 deterministic neutron transport
    benchmark problem according to enrichment factors for each material
    type, and writes the data to an HDF5 file. 
'''

import h5py
import numpy


def writeMaterialsFile(uo2_enr_mult, mox1_enr_mult, mox2_enr_mult, \
                      mox3_enr_mult, poison_enr_mult, boron_enr_mult):
    '''
        This method writes an HDF5 file for materials data for OpenMOC.
        It takes in the following arguments:

        uo2_enr_mult    - a factor to multiply the UO2 fission xs by
                          to simulate increasing the fuel enrichment
        mox1_enr_mult   - a factor multiply the MOX-4.3% fission xs by
                          to simulate increasing the fuel enrichment
        mox2_enr_mult   - a factor to multiply the MOX-7% fission xs by
                          to simulate increasing the fuel enrichment
        mox3_enr_mult   - a factor to multiply the MOX-8.7% fission xs
                          by to simulate increasing the fuel enrichment
        poison_enr_mult - a factor to multiply the guide tube absorption
                          xs by to simulate increasing a burnable poison
                          enrichment
        boron_enr_mult  - a factor to multiply the water absorption xs
                          by to simulate increasing the soluble boron
                          concentration
    '''


    print 'uo2 enr mult = %f' % (uo2_enr_mult)
    print 'mox1 enr mult = %f' % (mox1_enr_mult)
    print 'mox2 enr mult = %f' % (mox2_enr_mult)
    print 'mox3 enr mult = %f' % (mox3_enr_mult)
    print 'poison enr mult = %f' % (poison_enr_mult)
    print 'boron enr mult = %f' % (boron_enr_mult)

    # Create the file to store the manipulated C5G7 multi-group cross-sections
    f = h5py.File('design-a-reactor-materials.hdf5', 'w')
    f.attrs["Energy Groups"] = 7


    #### NOTE: Should we also multiply sigma_s????
    #### NOTE: Should we also increase absorption minus fission????


    ###########################################################################
    ##############################      UO2      ##############################
    ###########################################################################

    # Create a subgroup for UO2 materials data
    uo2 = f.create_group('UO2')
    
    sigma_f = numpy.array([7.212060E-03, 8.193010E-04, 6.453200E-03,
                        1.856480E-02, 1.780840E-02, 8.303480E-02, 
                           2.160040E-01]) * uo2_enr_mult
    nu_sigma_f = numpy.array([2.005998E-02, 2.027303E-03, 1.570599E-02, 
                        4.518301E-02, 4.334208E-02, 2.020901E-01, 
                              5.257105E-01]) * uo2_enr_mult
    sigma_a = numpy.array([8.024800E-03, 3.717400E-03, 2.676900E-02, 
                            9.623600E-02, 3.002000E-02, 1.112600E-01, 
                           2.827800E-01])
    sigma_a += (uo2_enr_mult - 1.0) * sigma_f
    sigma_s = numpy.array([1.275370E-01, 4.237800E-02, 9.437400E-06, 
                           5.516300E-09, 0., 0., 0., 0., 3.244560E-01,
                           1.631400E-03, 3.142700E-09, 0., 0., 0., 0.,
                           0., 4.509400E-01, 2.679200E-03, 0., 0., 0., 
                           0.,	0., 0., 4.525650E-01, 5.566400E-03, 0., 
                           0., 0., 0., 0., 1.252500E-04, 2.714010E-01,
                           1.025500E-02, 1.002100E-08, 0., 0.,	0., 0.,
                           1.296800E-03, 2.658020E-01, 1.680900E-02, 
                           0., 0., 0., 0., 0., 8.545800E-03, 
                           2.730800E-01])
    chi = numpy.array([5.87910E-01, 4.11760E-01, 3.39060E-04, 
                        1.17610E-07, 0., 0., 0.])
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    uo2.create_dataset('Total XS', data=sigma_t) 
    uo2.create_dataset('Absorption XS', data=sigma_a)
    uo2.create_dataset('Scattering XS', data=sigma_s)
    uo2.create_dataset('Fission XS', data=sigma_f)
    uo2.create_dataset('Nu Fission XS', data=nu_sigma_f)
    uo2.create_dataset('Chi', data=chi)


    ###########################################################################
    ############################      MOX (4.3%)     ##########################
    ###########################################################################

    # Create a subgroup for MOX-4.3%  materials data
    mox43 = f.create_group('MOX-4.3%')

    sigma_f = numpy.array([7.62704E-03, 8.76898E-04, 5.69835E-03, 
                           2.28872E-02, 1.07635E-02, 2.32757E-01, 
                           2.48968E-01]) * mox1_enr_mult
    nu_sigma_f = numpy.array([2.175300E-02, 2.535103E-03, 1.626799E-02, 
                              6.547410E-02, 3.072409E-02, 6.666510E-01, 
                              7.139904E-01]) * mox1_enr_mult

    sigma_a = numpy.array([8.433900E-03, 3.757700E-03, 2.797000E-02, 
                           1.042100E-01, 1.399400E-01, 4.091800E-01, 
                           4.093500E-01])
    sigma_a += (mox1_enr_mult - 1.0) * sigma_f
    sigma_s = numpy.array([1.288760E-01, 4.141300E-02, 8.229000E-06, 
                           5.040500E-09, 0., 0., 0., 0., 3.254520E-01, 
                           1.639500E-03, 1.598200E-09, 0., 0., 0., 0., 0., 
                           4.531880E-01, 2.614200E-03, 0., 0., 0., 0., 0., 0., 
                           4.571730E-01, 5.539400E-03, 0., 0., 0., 0., 0., 
                           1.604600E-04, 2.768140E-01, 9.312700E-03, 
                           9.165600E-09, 0., 0., 0., 0., 2.005100E-03, 
                           2.529620E-01, 1.485000E-02, 0., 0., 0., 0., 0., 
                           8.494800E-03, 2.650070E-01])
    chi = numpy.array([5.87910E-01, 4.11760E-01, 3.39060E-04, 1.17610E-07,
                       0., 0., 0.])
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    mox43.create_dataset('Total XS', data=sigma_t)
    mox43.create_dataset('Absorption XS', data=sigma_a)
    mox43.create_dataset('Scattering XS', data=sigma_s)
    mox43.create_dataset('Fission XS', data=sigma_f)
    mox43.create_dataset('Nu Fission XS', data=nu_sigma_f)
    mox43.create_dataset('Chi', data=chi)


    ###########################################################################
    ############################      MOX (7%)     ############################
    ###########################################################################

    # Create a subgroup for MOX-7% materials data
    mox7 = f.create_group('MOX-7%')

    sigma_f = numpy.array([8.25446E-03, 1.32565E-03, 8.42156E-03, 
                           3.28730E-02, 1.59636E-02, 3.23794E-01, 
                           3.62803E-01]) * mox2_enr_mult
    nu_sigma_f = numpy.array([2.381395E-02, 3.858689E-03, 2.413400E-02, 
                              9.436622E-02, 4.576988E-02, 9.281814E-01, 
                              1.043200E+00]) * mox2_enr_mult
    sigma_a = numpy.array([9.065700E-03, 4.296700E-03, 3.288100E-02, 
                           1.220300E-01, 1.829800E-01, 5.684600E-01, 
                           5.852100E-01])
    sigma_a += (mox2_enr_mult - 1.0) * sigma_f
    sigma_s = numpy.array([1.304570E-01, 4.179200E-02, 8.510500E-06, 
                           5.132900E-09, 0., 0., 0., 0., 3.284280E-01, 
                           1.643600E-03, 2.201700E-09, 0., 0., 0., 0., 0., 
                           4.583710E-01, 2.533100E-03, 0., 0., 0., 0., 0., 0., 
                           4.637090E-01, 5.476600E-03, 0., 0., 0., 0., 0., 
                           1.761900E-04, 2.823130E-01, 8.728900E-03, 
                           9.001600E-09, 0., 0., 0., 0., 2.276000E-03, 
                           2.497510E-01, 1.311400E-02, 0., 0., 0., 0., 0., 
                           8.864500E-03, 2.595290E-01])
    chi = numpy.array([5.87910E-01, 4.11760E-01, 3.39060E-04, 1.17610E-07, 
                       0., 0., 0.])
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    mox7.create_dataset('Total XS', data=sigma_t)
    mox7.create_dataset('Absorption XS', data=sigma_a)
    mox7.create_dataset('Scattering XS', data=sigma_s)
    mox7.create_dataset('Fission XS', data=sigma_f)
    mox7.create_dataset('Nu Fission XS', data=nu_sigma_f)
    mox7.create_dataset('Chi', data=chi)


    ###########################################################################
    ############################      MOX (8.7%)     ##########################
    ###########################################################################

    # Create a subgroup for MOX-8.7% materials data
    mox87 = f.create_group('MOX-8.7%')

    sigma_f = numpy.array([8.67209E-03, 1.62426E-03, 1.02716E-02, 
                           3.90447E-02, 1.92576E-02, 3.74888E-01, 
                           4.30599E-01]) * mox3_enr_mult
    nu_sigma_f = numpy.array([2.518600E-02, 4.739509E-03, 2.947805E-02, 
                              1.122500E-01, 5.530301E-02, 1.074999E+00, 
                              1.239298E+00]) * mox3_enr_mult
    sigma_a = numpy.array([9.486200E-03, 4.655600E-03, 3.624000E-02, 
                           1.327200E-01, 2.084000E-01, 6.587000E-01, 
                           6.901700E-01])
    sigma_a += (mox3_enr_mult - 1.0) * sigma_f
    sigma_s = numpy.array([1.315040E-01, 4.204600E-02, 8.697200E-06, 
                           5.193800E-09, 0., 0., 0., 0., 3.304030E-01, 
                           1.646300E-03, 2.600600E-09, 0., 0., 0., 0., 0., 
                           4.617920E-01, 2.474900E-03, 0., 0., 0., 0., 0., 0., 
                           4.680210E-01, 5.433000E-03, 0., 0., 0., 0., 0., 
                           1.859700E-04, 2.857710E-01, 8.397300E-03, 
                           8.928000E-09, 0., 0., 0., 0., 2.391600E-03, 
                           2.476140E-01, 1.232200E-02, 0., 0., 0., 0., 0., 
                           8.968100E-03, 2.560930E-01])
    chi = numpy.array([5.87910E-01, 4.11760E-01, 3.39060E-04, 1.17610E-07,
                       0., 0., 0.])
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    mox87.create_dataset('Total XS', data=sigma_t)
    mox87.create_dataset('Absorption XS', data=sigma_a)
    mox87.create_dataset('Scattering XS', data=sigma_s)
    mox87.create_dataset('Fission XS', data=sigma_f)
    mox87.create_dataset('Nu Fission XS', data=nu_sigma_f)
    mox87.create_dataset('Chi', data=chi)


    ###########################################################################
    ##########################      Fission Chamber     #######################
    ###########################################################################

    # Create a subgroup for fission chamber materials data
    fiss_chamber = f.create_group('Fission Chamber')

    sigma_f = numpy.array([4.79002E-09, 5.82564E-09, 4.63719E-07, 
                           5.24406E-06, 1.45390E-07, 7.14972E-07, 
                           2.08041E-06])
    nu_sigma_f = numpy.array([1.323401E-08, 1.434500E-08, 1.128599E-06,
                              1.276299E-05, 3.538502E-07, 1.740099E-06, 
                              5.063302E-06])
    sigma_a = numpy.array([5.113200E-04, 7.580100E-05, 3.157200E-04,
                           1.158200E-03, 3.397500E-03, 9.187800E-03,
                           2.324200E-02])
    sigma_s = numpy.array([6.616590E-02, 5.907000E-02, 2.833400E-04, 
                           1.462200E-06, 2.064200E-08, 0., 0., 0., 2.403770E-01,
                           5.243500E-02, 2.499000E-04, 1.923900E-05, 
                           2.987500E-06, 4.214000E-07,  0., 0., 1.834250E-01, 
                           9.228800E-02, 6.936500E-03, 1.079000E-03, 
                           2.054300E-04, 0., 0., 0., 7.907690E-02, 1.699900E-01,
                           2.586000E-02, 4.925600E-03, 0., 0., 0., 3.734000E-05,
                           9.975700E-02, 2.067900E-01, 2.447800E-02, 0., 0., 0.,
                           0., 9.174200E-04, 3.167740E-01, 2.387600E-01, 0., 0.,
                           0., 0., 0., 4.979300E-02, 1.09910E+00])
    chi = numpy.array([5.87910E-01, 4.11760E-01, 3.39060E-04, 
                       1.17610E-07, 0., 0., 0.])
    sigma_t = numpy.array([1.260320E-01, 2.931600E-01, 2.842400E-01, 
                           2.809600E-01, 3.344400E-01, 5.656400E-01, 
                           1.172150E+00])

    # Create datasets for each cross-section type
    fiss_chamber.create_dataset('Total XS', data=sigma_t)
    fiss_chamber.create_dataset('Absorption XS', data=sigma_a)
    fiss_chamber.create_dataset('Scattering XS', data=sigma_s)
    fiss_chamber.create_dataset('Fission XS', data=sigma_f)
    fiss_chamber.create_dataset('Nu Fission XS', data=nu_sigma_f)
    fiss_chamber.create_dataset('Chi', data=chi)


    ###########################################################################
    ############################      Guide Tube      #########################
    ###########################################################################

    # Create a subgroup for guide tube materials data
    guide_tube = f.create_group('Guide Tube')
    
    sigma_f = numpy.zeros(7)
    nu_sigma_f = numpy.zeros(7)
    sigma_a = numpy.array([5.113200E-04, 7.581300E-05, 3.164300E-04, 
                           1.167500E-03, 3.397700E-03, 9.188600E-03, 
                           2.324400E-02]) * poison_enr_mult
    sigma_s = numpy.array([6.616590E-02, 5.907000E-02, 2.833400E-04, 
                    1.462200E-06, 2.064200E-08, 0., 0., 0., 2.403770E-01,
                    5.243500E-02, 2.499000E-04, 1.923900E-05, 2.987500E-06, 
                    4.214000E-07, 0., 0., 1.834250E-01, 9.228800E-02, 
                    6.936500E-03, 1.079000E-03, 2.054300E-04, 0., 0., 0.,
                    7.907690E-02, 1.699900E-01, 2.586000E-02, 4.925600E-03,
                    0., 0., 0., 3.734000E-05, 9.975700E-02, 2.067900E-01,
                    2.447800E-02, 0., 0., 0., 0., 9.174200E-04, 3.167740E-01, 
                    2.387600E-01, 0., 0., 0., 0., 0., 4.979300E-02, 
                    1.099100E+00])
    chi = numpy.zeros(7)
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    guide_tube.create_dataset('Total XS', data=sigma_t)
    guide_tube.create_dataset('Absorption XS', data=sigma_a)
    guide_tube.create_dataset('Scattering XS', data=sigma_s)
    guide_tube.create_dataset('Fission XS', data=sigma_f)
    guide_tube.create_dataset('Nu Fission XS', data=nu_sigma_f)
    guide_tube.create_dataset('Chi', data=chi)


    ###########################################################################
    ##############################      Water      ############################
    ###########################################################################

    # Create a subgroup for water materials data
    water = f.create_group('Water')
    
    sigma_f = numpy.zeros(7)
    nu_sigma_f = numpy.zeros(7)
    sigma_a = numpy.array([6.010500E-04, 1.579300E-05, 3.371600E-04,
                           1.940600E-03, 5.741600E-03, 1.500100E-02, 
                           3.723900E-02]) * boron_enr_mult
    sigma_s = numpy.array([4.447770E-02, 1.134000E-01, 7.234700E-04,
                           3.749900E-06, 5.318400E-08, 0., 0., 0., 2.823340E-01,
                           1.299400E-01, 6.234000E-04, 4.800200E-05, 
                           7.448600E-06, 1.045500E-06, 0., 0., 3.452560E-01, 
                           2.245700E-01, 1.699900E-02, 2.644300E-03, 
                           5.034400E-04, 0., 0., 0.,
                           9.102840E-02, 4.155100E-01, 6.373200E-02, 
                           1.213900E-02, 0., 0., 0., 7.143700E-05, 1.391380E-01,
                           5.118200E-01, 6.122900E-02, 0., 0., 0., 0., 
                           2.215700E-03, 6.999130E-01, 5.373200E-01, 0., 0., 0.,
                           0., 0., 1.324400E-01, 2.480700E+00])
    chi = numpy.zeros(7)
    sigma_t = computeSigmaT(sigma_a, sigma_s, 7)

    # Create datasets for each cross-section type
    water.create_dataset('Total XS', data=sigma_t)
    water.create_dataset('Absorption XS', data=sigma_a)
    water.create_dataset('Scattering XS', data=sigma_s)
    water.create_dataset('Fission XS', data=sigma_f)
    water.create_dataset('Nu Fission XS', data=nu_sigma_f)
    water.create_dataset('Chi', data=chi)


    # Close the hdf5 data file
    f.close()



def computeSigmaT(sigma_a, sigma_s, num_groups):
    '''
    '''
    
    # Calculate total xs to accurately match the total absorption and scattering
    # cross-sections based on the enrichment factors
    sigma_t = numpy.zeros(num_groups)
    sigma_t[:] = sigma_a[:]

    for start in range(num_groups):
        stop = num_groups**2 - num_groups + start + 1
        sigma_t += sigma_s[start:stop:num_groups]

    return sigma_t
