**Table of Contents**

-   [Post-Processing Scripts](#post-processing-scripts)
    -   [Process Data and Synthetics](#process-data-and-synthetics)
        -   [Data processing script `process_data.pl`](#data-processing-script-process_datapl)
        -   [Synthetics processing script `process_syn.pl`](#synthetics-processing-script-process_synpl)
        -   [Script `rotate.pl`](#script-rotatepl)
    -   [Collect Synthetic Seismograms](#collect-synthetic-seismograms)
    -   [Clean Local Database](#clean-local-database)
    -   [Plot Movie Snapshots and Synthetic Shakemaps](#plot-movie-snapshots-and-synthetic-shakemaps)
        -   [Script `movie2gif.gmt.pl`](#script-movie2gifgmtpl)
        -   [Script `plot_shakemap.gmt.pl`](#script-plot_shakemapgmtpl)
    -   [Map Local Database](#map-local-database)

Post-Processing Scripts
=======================

Several post-processing scripts/programs are provided in the `utils/` directory, and most of them need to be adjusted when used on different systems, for example, the path of the executable programs. Here we only list a few of the available scripts and provide a brief description, and you can either refer to the related sections for detailed usage or, in a lot of cases, type the script/program name without arguments for its usage.

Process Data and Synthetics
---------------------------

In many cases, the SEM synthetics are calculated and compared to data seismograms recorded at seismic stations. Since the SEM synthetics are accurate for a certain frequency range, both the original data and the synthetics need to be processed before a comparison can be made.

For such comparisons, the following steps are recommended:

1.  Make sure that both synthetic and observed seismograms have the correct station/event and timing information.

2.  Convolve synthetic seismograms with a source time function with the half duration specified in the `CMTSOLUTION` file, provided, as recommended, you used a zero half duration in the SEM simulations.

3.  Resample both observed and synthetic seismograms to a common sampling rate.

4.  Cut the records using the same window.

5.  Remove the trend and mean from the records and taper them.

6.  Remove the instrument response from the observed seismograms (recommended) or convolve the synthetic seismograms with the instrument response.

7.  Make sure that you apply the same filters to both observed and synthetic seismograms. Preferably, avoid filtering your records more than once.

8.  Now, you are ready to compare your synthetic and observed seismograms.

We generally use the following scripts provided in the `utils/seis_process/` directory:

### Data processing script `process_data.pl`

This script cuts a given portion of the original data, filters it, transfers the data into a displacement record, and picks the first P and S arrivals. For more functionality, type ‘`process_data.pl`’ without any argument. An example of the usage of the script:

    process_data.pl -m CMTSOLUTION -s 1.0 -l 0/4000 -i -f -t 40/500 -p -x bp DATA/1999.330*.BH?.SAC

which has resampled the SAC files to a sampling rate of 1 seconds, cut them between 0 and 4000 seconds, transfered them into displacement records and filtered them between 40 and 500 seconds, picked the first P and S arrivals, and added suffix ‘`bp`’ to the file names.

Note that all of the scripts in this section actually use the SAC and/or IASP91 to do the core operations; therefore make sure that the SAC and IASP91 packages are installed properly on your system, and that all the environment variables are set properly before running these scripts.

### Synthetics processing script `process_syn.pl`

This script converts the synthetic output from the SEM code from ASCII to SAC format, and performs similar operations as ‘`process_data.pl`’. An example of the usage of the script:

    process_syn.pl -m CMTSOLUTION -h -a STATIONS -s 1.0 -l 0/4000 -f -t 40/500 -p -x bp SEM/*.BX?.semd

which will convolve the synthetics with a triangular source-time function from the `CMTSOLUTION` file, convert the synthetics into SAC format, add event and station information into the SAC headers, resample the SAC files with a sampling rate of 1 seconds, cut them between 0 and 4000 seconds, filter them between 40 and 500 seconds with the same filter used for the observed data, pick the first P and S arrivals, and add the suffix ‘`bp`’ to the file names.

More options are available for this script, such as adding time shift to the origin time of the synthetics, convolving the synthetics with a triangular source time function with a given half duration, etc. Type `process_syn.pl` without any argument for a detailed usage.

In order to convert between SAC format and ASCII files, useful scripts are provided in the subdirectories
`utils/sac2000_alpha_convert/` and `utils/seis_process/asc2sac/`.

### Script `rotate.pl`

The original data and synthetics have three components: vertical (BHZ resp. BXZ), north (BHN resp. BXN) and east (BHE resp. BXE). However, for most seismology applications, transverse and radial components are also desirable. Therefore, we need to rotate the horizontal components of both the data and the synthetics to the transverse and radial direction, and `rotate.pl`<span> can be used to accomplish this:</span>

    rotate.pl -l 0 -L 180 -d DATA/*.BHE.SAC.bp
    rotate.pl -l 0 -L 180 SEM/*.BXE.semd.sac.bp

where the first command performs rotation on the SAC data obtained through Seismogram Transfer Program (STP) , while the second command rotates the processed SEM synthetics.

Collect Synthetic Seismograms
-----------------------------

The forward and adjoint simulations generate synthetic seismograms in the `OUTPUT_FILES/` directory by default. For the forward simulation, the files are named like `NT.STA.BX?.semd` for two-column time series, or `NT.STA.BX?.semd.sac` for ASCII SAC format, where NT and STA are the network code and station name, and `BX?` stands for the component name. Please see the Appendix [cha:Coordinates] and [cha:channel-codes] for further details.

The adjont simulations generate synthetic seismograms with the name `NT.S?????.S??.sem` (refer to Section [sec:Adjoint-simulation-sources] for details). The kernel simulations output the back-reconstructed synthetic seismogram in the name `NT.STA.BX?.semd`, mainly for the purpose of checking the accuracy of the reconstruction. Refer to Section [sec:Adjoint-simulation-finite] for further details.

You do have further options to change this default output behavior, given in the main constants file `constants.h` located in `src/shared/` directory:

<span>`SEISMOGRAMS_BINARY`</span>  
set to `.true.` to have seismograms written out in binary format.

<span>`WRITE_SEISMOGRAMS_BY_MASTER`</span>  
Set to `.true.` to have only the master process writing out seismograms. This can be useful on a cluster, where only the master process node has access to the output directory.

<span>`USE_OUTPUT_FILES_PATH`</span>  
Set to `.false.` to have the seismograms output to `LOCAL_PATH` directory specified in the main parameter file `DATA/Par_file`. In this case, you could collect the synthetics onto the frontend using the `collect_seismo_lsf_multi.pl` script located in the `utils/Cluster/lsf/` directory. The usage of the script would be e.g.:

    collect_seismo.pl machines DATA/Par_file

where `machines` is a file containing the node names and `DATA/Par_file` the parameter file used to extract the `LOCAL_PATH` directory used for the simulation.

Clean Local Database
--------------------

After all the simulations are done, the seismograms are collected, and the useful database files are copied to the frontend, you may need to clean the local scratch disk for the next simulation. This is especially important in the case of kernel simulation, where very large files are generated for the absorbing boundaries to help with the reconstruction of the regular forward wavefield. A sample script is provided in `utils/`:

    cleanbase.pl machines

where `machines` is a file containing the node names.

Plot Movie Snapshots and Synthetic Shakemaps
--------------------------------------------

### Script `movie2gif.gmt.pl`

With the movie data saved in `OUTPUT_FILES/` at the end of a movie simulation (`MOVIE_SURFACE=.true.`<span>), you can run the </span>`` `create_movie_shakemap_AVS_DX_GMT ``<span>’ code to convert these binary movie data into GMT xyz files for futher processing. A sample script </span>`movie2gif.gmt.pl`<span> is provided to do this conversion, and then plot the movie snapshots in GMT, for example:</span>

    movie2gif.gmt.pl -m CMTSOLUTION -g -f 1/40 -n -2 -p

which for the first through the 40th movie frame, converts the `moviedata` files into GMT xyz files, interpolates them using the ’nearneighbor’ command in GMT, and plots them on a 2D topography map. Note that ‘`-2`’ and ‘`-p`’ are both optional.

### Script `plot_shakemap.gmt.pl`

With the shakemap data saved in `OUTPUT_FILES/` at the end of a shakemap simulation
(`CREATE_SHAKEMAP=.true.`), you can also run `` `create_movie_shakemap_AVS_DX_GMT ``’ code to convert the binary shakemap data into GMT xyz files. A sample script `plot_shakemap.gmt.pl` is provided to do this conversion, and then plot the shakemaps in GMT, for example:

    plot_shakemap.gmt.pl data _dir type(1,2,3) CMTSOLUTION

where `type=1` for a displacement shakemap, `2` for velocity, and `3` for acceleration.

Map Local Database
------------------

A sample program `remap_database` is provided to map the local database from a set of machines to another set of machines. This is especially useful when you want to run mesher and solver, or different types of solvers separately through a scheduler (refer to Chapter [cha:Scheduler]).

    run_lsf.bash --gm-no-shmem --gm-copy-env remap_database old_machines 150

where `old_machines` is the LSF machine file used in the previous simulation, and `150` is the number of processors in total.

-----
> This documentation has been automatically generated by [pandoc](http://www.pandoc.org)
> based on the User manual (LaTeX version) in folder doc/USER_MANUAL/
> (Mar 10, 2020)

