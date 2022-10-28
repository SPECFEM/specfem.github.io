**Table of Contents**

-   [Adjoint Simulations](#adjoint-simulations)
    -   [Adjoint Simulations for Sources Only (not for the Model)](#adjoint-simulations-for-sources-only-not-for-the-model)
    -   [Adjoint Simulations for Finite-Frequency Kernels (Kernel Simulation)](#adjoint-simulations-for-finite-frequency-kernels-kernel-simulation)

Adjoint Simulations
===================

Adjoint simulations are generally performed for two distinct applications. First, they can be used in point source moment-tensor inversions, or source imaging for earthquakes with large ruptures such as the Lander’s earthquake (Wald and Heaton 1994). Second, they can be used to generate finite-frequency sensitivity kernels that are a critical part of tomographic inversions based upon 3D reference models (J. Tromp, Tape, and Liu 2005; Liu and Tromp 2006; J. Tromp, Komatitsch, and Liu 2008; Q. Liu and Tromp 2008). In either case, source parameter or velocity structure updates are sought to minimize a specific misfit function (e.g., waveform or traveltime differences), and the adjoint simulation provides a means of computing the gradient of the misfit function and further reducing it in successive iterations. Applications and procedures pertaining to source studies and finite-frequency kernels are discussed in Sections [sec:Adjoint-simulation-sources] and [sec:Adjoint-simulation-finite], respectively. The two related parameters in the `Par_file` are `SIMULATION_TYPE` (1, 2 or 3) and the `SAVE_FORWARD` (boolean).

Adjoint Simulations for Sources Only (not for the Model)
--------------------------------------------------------

When a specific misfit function between data and synthetics is minimized to invert for earthquake source parameters, the gradient of the misfit function with respect to these source parameters can be computed by placing time-reversed seismograms at the receivers as virtual sources in an adjoint simulation. Then the value of the gradient is obtained from the adjoint seismograms recorded at the original earthquake location.

1.  **Prepare the adjoint sources** [enu:Prepare-the-adjoint]

    1.  First, run a regular forward simulation (`SIMULATION_TYPE = 1` and `SAVE_FORWARD = .false.`). You can automatically set these two variables using the `utils/change_simulation_type.pl`<span> script:</span>

            utils/change_simulation_type.pl -f

        and then collect the recorded seismograms at all the stations given in `DATA/STATIONS`.

    2.  Then select the stations for which you want to compute the time-reversed adjoint sources and run the adjoint simulation, and compile them into the `DATA/STATIONS_ADJOINT` file, which has the same format as the regular `DATA/STATIONS` file.

        -   Depending on what type of misfit function is used for the source inversion, adjoint sources need to be computed from the original recorded seismograms for the selected stations and saved in a sub-directory called `SEM/` in the root directory of the code, with the format `NT.STA.BX?.adj`, where `NT`, `STA` are the network code and station name given in the `DATA/STATIONS_ADJOINT` file, and `BX?` represents the component name of a particular adjoint seismogram. Please note that the band code can change depending on your sampling rate (see Appendix [cha:channel-codes] for further details).

        -   The adjoint seismograms are in the same format as the original seismogram (`NT.STA.BX?.sem?`), with the same start time, time interval and record length.

    3.  Notice that even if you choose to time reverse only one component from one specific station, you still need to supply all three components because the code is expecting them (you can set the other two components to be zero).

    4.  Also note that since time-reversal is done in the code itself, no explicit time-reversing is needed for the preparation of the adjoint sources, i.e., the adjoint sources are in the same forward time sense as the original recorded seismograms.

2.  **Set the related parameters and run the adjoint simulation**
    In the `DATA/Par_file`, set the two related parameters to be `SIMULATION_TYPE = 2` and `SAVE_FORWARD = .false.`. More conveniently, use the scripts `utils/change_simulation_type.pl` to modify the `Par_file` automatically (`change_simulation_type.pl -a`). Then run the solver to launch the adjoint simulation.

3.  **Collect the seismograms at the original source location**

    After the adjoint simulation has completed successfully, collect the seismograms from `LOCAL_PATH`.

    -   These adjoint seismograms are recorded at the locations of the original earthquake sources given by the `DATA/CMTSOLUTION` file, and have names of the form `NT.S?????.S??.sem` for the six-component strain tensor (`SNN,SEE,SZZ,SNE,SNZ,SEZ`) at these locations, and
        `NT.S?????.BX?.sem` for the three-component displacements (`BXN,BXE,BXZ`) recorded at these locations.

    -   `S?????` denotes the source number; for example, if the original `CMTSOLUTION` provides only a point source, then the seismograms collected will start with `S00001`.

    -   These adjoint seismograms provide critical information for the computation of the gradient of the misfit function.

Adjoint Simulations for Finite-Frequency Kernels (Kernel Simulation)
--------------------------------------------------------------------

Finite-frequency sensitivity kernels are computed in two successive simulations (please refer to Liu and Tromp (2006) and J. Tromp, Komatitsch, and Liu (2008) for details).

1.  **Run a forward simulation with the state variables saved at the end of the simulation**

    Prepare the `CMTSOLUTION`<span> and </span>`STATIONS`<span> files, set the parameters </span>`SIMULATION_TYPE`<span> </span>`=`<span> </span>`1`<span> and </span>`SAVE_FORWARD =`<span> </span>`.true.`<span> in the </span>`Par_file`<span> (</span>`change_simulation_type -F`<span>), and run the solver.</span>

    -   Notice that attenuation is not implemented yet for the computation of finite-frequency kernels; therefore set `ATTENUATION = .false.` in the `Par_file`.

    -   We also suggest you modify the half duration of the `CMTSOLUTION` to be similar to the accuracy of the simulation (see Equation [eq:shortest<sub>p</sub>eriod]) to avoid too much high-frequency noise in the forward wavefield, although theoretically the high-frequency noise should be eliminated when convolved with an adjoint wavefield with the proper frequency content.

    -   This forward simulation differs from the regular simulations (`SIMULATION_TYPE`<span> </span>`=`<span> </span>`1`<span> and </span>`SAVE_FORWARD`<span> </span>`=`<span> </span>`.false.`<span>) described in the previous chapters in that the state variables for the last time step of the simulation, including wavefields of the displacement, velocity, acceleration, etc., are saved to the </span>`LOCAL_PATH`<span> to be used for the subsequent simulation. </span>

    -   For regional simulations, the files recording the absorbing boundary contribution are also written to the `LOCAL_PATH` when `SAVE_FORWARD = .true.`.

2.  **Prepare the adjoint sources**

    The adjoint sources need to be prepared the same way as described in the Section [enu:Prepare-the-adjoint].

    -   In the case of travel-time finite-frequency kernel for one source-receiver pair, i.e., point source from the `CMTSOLUTION`, and one station in the `STATIONS_ADJOINT` list, we supply a sample program in `utils/adjoint_sources/traveltime/xcreate_adjsrc_traveltime` to cut a certain portion of the original displacement seismograms and convert it into the proper adjoint source to compute the finite-frequency kernel.

            xcreate_adjsrc_traveltime t1 t2 ifile[0-5] E/N/Z-ascii-files [baz]

        where `t1` and `t2` are the start and end time of the portion you are interested in, `ifile` denotes the component of the seismograms to be used (0 for all three components, 1 for East, 2 for North, and 3 for vertical, 4 for transverse, and 5 for radial component), `E/N/Z-ascii-files` indicate the three-component displacement seismograms in the right order, and `baz` is the back-azimuth of the station. Note that `baz` is only supplied when `ifile` = 4 or 5.

    -   Similarly, a sample program to compute adjoint sources for amplitude finite-frequency kernels may be found in `utils/adjoint_sources/amplitude` and used in the same way as described for traveltime measurements

            xcreate_adjsrc_amplitude t1 t2 ifile[0-5] E/N/Z-ascii-files [baz]

3.  **Run the kernel simulation**

    With the successful forward simulation and the adjoint source ready in the `SEM/` directory, set `SIMULATION_TYPE = 3` and `SAVE_FORWARD = .false.` in the `Par_file` (you can use `change_simulation_type.pl -b`), and rerun the solver.

    -   The adjoint simulation is launched together with the back reconstruction of the original forward wavefield from the state variables saved from the previous forward simulation, and the finite-frequency kernels are computed by the interaction of the reconstructed forward wavefield and the adjoint wavefield.

    -   The back-reconstructed seismograms at the original station locations are saved to the `LOCAL_PATH` at the end of the kernel simulations, and can be collected to the local disk.

    -   These back-constructed seismograms can be compared with the time-reversed original seismograms to assess the accuracy of the backward reconstruction, and they should match very well.

    -   The arrays for density, P-wave speed and S-wave speed kernels are also saved in the `LOCAL_PATH` with the names `proc??????_rho(alpha,beta)_kernel.bin`, where `proc??????` represents the processor number, `rho(alpha,beta)` are the different types of kernels.

4.  **Run the anisotropic kernel simulation**

    Instead of the kernels for the isotropic wave speeds, you can also compute the kernels for the 21 independent components \(C_{IJ},\, I,J=1,...,6\) (using Voigt’s notation) of the elastic tensor in the cartesian coordinate system. This is done by setting `ANISOTROPIC_KL` `=` `.true.` in `constants.h` before compiling the package. The definition of the parameters \(C_{IJ}\) in terms of the corresponding components \(c_{ijkl},ijkl,i,j,k,l=1,2,3\) of the elastic tensor in cartesian coordinates follows Chen and Tromp (2007). The 21 anisotropic kernels are saved in the `LOCAL_PATH` in one file with the name of `proc??????_cijkl_kernel.bin` (with `proc??????` the processor number). The output kernels correspond to absolute perturbations \(\delta C_{IJ}\) of the elastic parameters and their unit is in \(s/GPa/km^{3}\). For consistency, the output density kernels with this option turned on are for a perturbation \(\delta\rho\) (and not \(\frac{\delta\rho}{\rho}\)) and their unit is in s / (kg/m\(^{3}\)) / km\(^{3}\). These ‘primary’ anisotropic kernels can then be combined to obtain the kernels for different parameterizations of anisotropy. This can be done, for example, when combining the kernel files from slices into one mesh file (see Section [sec:Finite-Frequency-Kernels]).

    If `ANISOTROPIC_KL` `=` `.true.` by additionally setting `ANISOTROPIC_KL` `=` `.true.` in `constants.h` the package will save anisotropic kernels parameterized as velocities related to transverse isotropy based on the the Chen and Tromp parameters Chen and Tromp (2007). The kernels are saved as relative perturbations for horizontal and vertical P and S velocities, \(\alpha_{v},\alpha_{h},\beta_{v},\beta_{h}\). Explicit relations can be found in appendix B. of Sieminski et al. (2007)

    The anisotropic kernels are only currently available for CPU mode.

In general, the three steps need to be run sequentially to assure proper access to the necessary files. If the simulations are run through some cluster scheduling system (e.g., LSF), and the forward simulation and the subsequent kernel simulations cannot be assigned to the same set of computer nodes, the kernel simulation will not be able to access the database files saved by the forward simulation. Solutions for this dilemma are provided in Chapter [cha:Scheduler]. Visualization of the finite-frequency kernels is discussed in Section [sec:Finite-Frequency-Kernels].

References
----------

Chen, Min, and Jeroen Tromp. 2007. “Theoretical and Numerical Investigations of Global and Regional Seismic Wave Propagation in Weakly Anisotropic Earth Models.” *Geophys. J. Int.* 168 (3): 1130–52. doi:[10.1111/j.1365-246X.2006.03218.x](http://dx.doi.org/10.1111/j.1365-246X.2006.03218.x).

Liu, Q., and J. Tromp. 2008. “Finite-Frequency Sensitivity Kernels for Global Seismic Wave Propagation Based Upon Adjoint Methods.” *Geophys. J. Int.* 174 (1): 265–86. doi:[10.1111/j.1365-246X.2008.03798.x](http://dx.doi.org/10.1111/j.1365-246X.2008.03798.x).

Liu, Qinya, and Jeroen Tromp. 2006. “Finite-Frequency Kernels Based on Adjoint Methods.” *Bull. Seism. Soc. Am.* 96 (6): 2383–97. doi:[10.1785/0120060041](http://dx.doi.org/10.1785/0120060041).

Sieminski, Anne, Qinya Liu, Jeannot Trampert, and Jeroen Tromp. 2007. “Finite-Frequency Sensitivity of Body Waves to Anisotropy Based Upon Adjoint Methods.” *Geophys. J. Int.* 171: 368–89. doi:[10.1111/j.1365-246X.2007.03528.x](http://dx.doi.org/10.1111/j.1365-246X.2007.03528.x).

Tromp, Jeroen, Dimitri Komatitsch, and Qinya Liu. 2008. “Spectral-Element and Adjoint Methods in Seismology.” *Communications in Computational Physics* 3 (1): 1–32.

Tromp, Jeroen, Carl Tape, and Qinya Liu. 2005. “Seismic Tomography, Adjoint Methods, Time Reversal and Banana-Doughnut Kernels.” *Geophys. J. Int.* 160 (1): 195–216. doi:[10.1111/j.1365-246X.2004.02453.x](http://dx.doi.org/10.1111/j.1365-246X.2004.02453.x).

Wald, D. J., and T. H. Heaton. 1994. “Spatial and Temporal Distribution of Slip for the 1992 Landers, California Earthquake.” *Bull. Seism. Soc. Am.* 84: 668–91.

-----
> This documentation has been automatically generated by [pandoc](http://www.pandoc.org)
> based on the User manual (LaTeX version) in folder doc/USER_MANUAL/
> (Mar 10, 2020)

