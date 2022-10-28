**Table of Contents**

-   [Noise Cross-correlation Simulations](#noise-cross-correlation-simulations)
    -   [Input Parameter Files](#input-parameter-files)
    -   [Noise Simulations: Step by Step](#noise-simulations-step-by-step)
        -   [Pre-simulation](#pre-simulation)
        -   [Simulations](#simulations)
        -   [Post-simulation](#post-simulation)
    -   [Example](#example)

Noise Cross-correlation Simulations
===================================

Besides earthquake simulations, SPECFEM3D Cartesian includes functionality for seismic noise tomography as well. In order to proceed successfully in this chapter, it is critical that you have already familiarized yourself with procedures for meshing (Chapter [cha:Mesh-Generation]), creating distributed databases (Chapter [cha:Creating-Distributed-Databases]), running earthquake simulations (Chapters [cha:Running-the-Solver]) and adjoint simulations (Chapter [cha:Adjoint-Simulations]). Also, make sure you read the article ‘Noise cross-correlation sensitivity kernels’ (Tromp et al. 2010), in order to understand noise simulations from a theoretical perspective.

Input Parameter Files
---------------------

As usual, the three main input files are crucial: `Par_file`, `CMTSOLUTION` and `STATIONS`. Unless otherwise specified, those input files should be located in directory `DATA/`.

`CMTSOLUTION` is required for all simulations. At a first glance, it may seem unexpected to have it here, since the noise simulations should have nothing to do with the earthquake – `CMTSOLUTION`. However, for noise simulations, it is critical to have no earthquakes. In other words, the moment tensor specified in `CMTSOLUTION` must be set to zero manually!

`STATIONS` remains the same as in previous earthquake simulations, except that the order of receivers listed in `STATIONS` is now important. The order will be used to determine the ‘master’ receiver, i.e., the one that simultaneously cross correlates with the others.

`Par_file` also requires careful attention. A parameter called `NOISE_TOMOGRAPHY` has been added which specifies the type of simulation to be run. `NOISE_TOMOGRAPHY` is an integer with possible values 0, 1, 2 and 3. For example, when `NOISE_TOMOGRAPHY` equals 0, a regular earthquake simulation will be run. When it is 1/2/3, you are about to run step 1/2/3 of the noise simulations respectively. Should you be confused by the three steps, refer to Tromp et al. (2010) for details.

Another change to `Par_file` involves the parameter `NSTEP`. While for regular earthquake simulations this parameter specifies the length of synthetic seismograms generated, for noise simulations it specifies the length of the seismograms used to compute cross correlations. The actual cross correlations are thus twice this length, i.e., \(2 \mathrm{NSTEP}-1\). The code automatically makes the modification accordingly, if `NOISE_TOMOGRAPHY` is not zero.

There are other parameters in `Par_file` which should be given specific values. For instance, since the first two steps for calculating noise sensitivity kernels correspond to forward simulations, `SIMULATION_TYPE` must be 1 when `NOISE_TOMOGRAPHY` equals 1 or 2. Also, we have to reconstruct the ensemble forward wavefields in adjoint simulations, therefore we need to set `SAVE_FORWARD` to `.true.` for the second step, i.e., when `NOISE_TOMOGRAPHY` equals 2. The third step is for kernel constructions. Hence `SIMULATION_TYPE` should be 3, whereas `SAVE_FORWARD` must be `.false.`.

Finally, for most system architectures, please make sure that `LOCAL_PATH` in `Par_file` is in fact local, not globally shared. Because we have to save the wavefields at the earth’s surface at every time step, it is quite problematic to have a globally shared `LOCAL_PATH`, in terms of both disk storage and I/O speed.

Noise Simulations: Step by Step
-------------------------------

Proper parameters in those parameter files are not enough for noise simulations to run. We have more parameters to specify: for example, the ensemble-averaged noise spectrum, the noise distribution etc. However, since there are a few ‘new’ files, it is better to introduce them sequentially. In this section, standard procedures for noise simulations are described.

### Pre-simulation

-   As usual, we first configure the software package using:

        ./configure FC=ifort MPIFC=mpif90

    Use the following if SCOTCH is needed:

        ./configure FC=ifort MPIFC=mpif90 --with-scotch-dir=/opt/scotch

-   Next, we need to compile the source code using:

        make xgenerate_databases
        make xspecfem3D

-   Before we can run noise simulations, we have to specify the noise statistics, e.g., the ensemble-averaged noise spectrum. Matlab scripts are provided to help you to generate the necessary file:

        EXAMPLES/noise_tomography/NOISE_TOMOGRAPHY.m  (main program)
        EXAMPLES/noise_tomography/PetersonNoiseModel.m

    In Matlab, simply run:

        NOISE_TOMOGRAPHY(NSTEP, DT, Tmin, Tmax, NOISE_MODEL)

    `DT` is given in `Par_file`, but <span> `NSTEP` is NOT the one specified in `Par_file`</span>. <span>**Instead, you have to feed \(2 \mathrm{NSTEP}-1\) to account for the doubled length of cross correlations**</span>. `Tmin` and `Tmax` correspond to the period range you are interested in, whereas `NOISE_MODEL` denotes the noise model you will be using (`’NLNM’` for New Low Noise Model or `’NHNM’` for New High Noise Model). Details can be found in the Matlab script.

    After running the Matlab script, you will be given the following information (plus a figure in Matlab):

        *************************************************************
        the source time function has been saved in:
        ..../S_squared (note this path must be different)
        S_squared should be put into directory:
        ./NOISE_TOMOGRAPHY/ in the SPECFEM3D Cartesian package

    In other words, the Matlab script creates a file called `S_squared`, which is the first ‘new’ input file we encounter for noise simulations.

    One may choose a flat noise spectrum rather than Peterson’s noise model. This can be done easily by modifying the Matlab script a little.

-   Create a new directory in the SPECFEM3D Cartesian package, name it as `./NOISE_TOMOGRAPHY/`. We will add some parameter files later in this folder.

-   Put the Matlab-generated-file `S_squared` in `./NOISE_TOMOGRAPHY/`.

    That’s to say, you will have a file `./NOISE_TOMOGRAPHY/S_squared` in the example provided in the SPECFEM3D Cartesian package.

-   Create a file called `./NOISE_TOMOGRAPHY/irec_master_noise`. Note that this file is located in directory `./NOISE_TOMOGRAPHY/` as well. In general, all noise simulation related parameter files go into that directory. `irec_master_noise` contains only one integer, which is the ID of the ‘master’ receiver. For example, if this file contains 5, it means that the fifth receiver listed in `DATA/STATIONS` becomes the ‘master’. That’s why we mentioned previously that the order of receivers in `DATA/STATIONS` is important.

    Note that in some simulations, the `DATA/STATIONS` might contain receivers which are outside of our computational domains. Therefore, the integer in `irec_master_noise` is actually the ID in `DATA/STATIONS_FILTERED` (which is generated by `bin/xgenerate_databases`).

-   Create a file called `./NOISE_TOMOGRAPHY/nu_master`. This file holds three numbers, forming a (unit) vector. It describes which component we are cross-correlating at the ‘master’ receiver, i.e., \({\hat{{\bf \nu}}}^{\alpha}\) in Tromp et al. (2010). The three numbers correspond to E/N/Z components respectively. Most often, the vertical component is used, and in those cases the three numbers should be 0, 0 and 1.

-   Describe the noise direction and distributions in `src/specfem3d/noise_tomography.f90`. Search for a subroutine called `noise_distribution_direction` in `noise_tomography.f90`. It is actually located at the very beginning of `noise_tomography.f90`. The default assumes vertical noise and a uniform distribution across the whole free surface of the model. It should be quite self-explanatory for modifications. Should you modify this part, you have to re-compile the source code.

### Simulations

With all of the above done, we can finally launch our simulations. Again, please make sure that the `LOCAL_PATH` in `DATA/Par_file` is not globally shared. It is quite problematic to have a globally shared `LOCAL_PATH`, in terms of both disk storage and speed of I/O (we have to save the wavefields at the earth’s surface at every time step).

As discussed in Tromp et al. (2010), it takes three steps/simulations to obtain one contribution of the ensemble sensitivity kernels:

-   Step 1: simulation for generating wavefields

        SIMULATION_TYPE = 1
        NOISE_TOMOGRAPHY = 1
        SAVE_FORWARD (not used, can be either .true. or .false.)

-   Step 2: simulation for ensemble forward wavefields

        SIMULATION_TYPE = 1
        NOISE_TOMOGRAPHY = 2
        SAVE_FORWARD = .true.

-   Step 3: simulation for ensemble adjoint wavefields and sensitivity kernels

        SIMULATION_TYPE = 3
        NOISE_TOMOGRAPHY = 3
        SAVE_FORWARD = .false.

    Note Step 3 is an adjoint simulation, please refer to previous chapters on how to prepare adjoint sources and other necessary files, as well as how adjoint simulations work.

It is better to run the three steps continuously within the same job on a cluster, otherwise you have to collect the saved surface movies from the old nodes to the new nodes. This process varies from cluster to cluster and thus cannot be discussed here. Please ask your cluster administrator for information/configuration of the cluster you are using.

### Post-simulation

After those simulations, you have all stuff you need, either in the `OUTPUT_FILES/` or in the directory specified by `LOCAL_PATH` in `DATA/Par_file` (which are most probably on local nodes). Collect whatever you want from the local nodes to your workstation, and then visualize them. This process is the same as what you may have done for regular earthquake simulations. Refer to other chapters if you have problems.

Simply speaking, two outputs are the most interesting: the simulated ensemble cross correlations and one contribution of the ensemble sensitivity kernels.

The simulated ensemble cross correlations are obtained after the second simulation (Step 2). Seismograms in `OUTPUT_FILES/` are actually the simulated ensemble cross correlations. Collect them immediately after Step 2, or the Step 3 will overwrite them. Note that we have a ‘master’ receiver specified by `irec_master_noise`, the seismogram at one station corresponds to the cross correlation between that station and the ‘master’. Since the seismograms have three components, we may obtain cross correlations for different components as well, not necessarily the cross correlations between vertical components.

One contribution of the ensemble cross-correlation sensitivity kernels are obtained after Step 3, stored in the `DATA/LOCAL_PATH` on local nodes. The ensemble kernel files are named the same as regular earthquake kernels.

You need to run another three simulations to get the other contribution of the ensemble kernels, using different forward and adjoint sources given in Tromp et al. (2010).

Example
-------

In order to illustrate noise simulations in an easy way, one example is provided in `EXAMPLES/noise_tomography/`. See `EXAMPLES/noise_tomography/README` for explanations.

Note, however, that they are created for a specific workstation (CLOVER@PRINCETON), which has at least 4 cores with ‘mpif90’ working properly.

If your workstation is suitable, you can run the example in `EXAMPLES/noise_tomography/` using:

`./pre-processing.sh`

Even if this script does not work on your workstation, the procedure it describes is universal. You may review the whole process described in the last section by following the commands in `pre-processing.sh`, which should contain enough explanations for all the commands.

References
----------

Tromp, Jeroen, Yang Luo, Shravan Hanasoge, and Daniel Peter. 2010. “Noise Cross-Correlation Sensitivity Kernels.” *Geophys. J. Int.* 183: 791–819. doi:[10.1111/j.1365-246X.2010.04721.x](http://dx.doi.org/10.1111/j.1365-246X.2010.04721.x).

-----
> This documentation has been automatically generated by [pandoc](http://www.pandoc.org)
> based on the User manual (LaTeX version) in folder doc/USER_MANUAL/
> (Mar 10, 2020)

