**Table of Contents**

-   [Getting Started](#getting-started)
    -   [Adding OpenMP support in addition to MPI](#adding-openmp-support-in-addition-to-mpi)
    -   [Compiling on an IBM BlueGene](#compiling-on-an-ibm-bluegene)
    -   [Visualizing the subroutine calling tree of the source code](#visualizing-the-subroutine-calling-tree-of-the-source-code)
    -   [Using the ADIOS library for I/O](#using-the-adios-library-for-io)
    -   [Becoming a developer of the code, or making small modifications in the source code](#becoming-a-developer-of-the-code-or-making-small-modifications-in-the-source-code)

Getting Started
===============

To download the SPECFEM3D\_Cartesian software package, type this:

    git clone --recursive --branch devel https://github.com/geodynamics/specfem3d.git

*Note: for people who would like to run the package on Windows rather than on Unix machines, you can install Docker or VirtualBox (installing a Linux in VirtualBox in that latter case) and run it easily from inside that.*

We recommend that you add <span>`ulimit -S -s unlimited`</span> to your <span>`.bash_profile`</span> file and/or <span>`limit stacksize unlimited `</span> to your <span>`.cshrc`</span> file to suppress any potential limit to the size of the Unix stack.

Then, to configure the software for your system, run the `configure` shell script. This script will attempt to guess the appropriate configuration values for your system. However, at a minimum, it is recommended that you explicitly specify the appropriate command names for your Fortran compiler (another option is to define FC, CC and MPIF90 in your .bash\_profile or your .cshrc file):

        ./configure FC=gfortran CC=gcc

If you want to run in parallel, i.e., using more than one processor core, then you would type

        ./configure FC=gfortran CC=gcc MPIFC=mpif90 --with-mpi

You can replace the GNU compilers above (gfortran and gcc) with other compilers if you want to; for instance for Intel ifort and icc use FC=ifort CC=icc instead.

Note that MPI must be installed with MPI-IO enabled because parts of SPECFEM3D perform I/Os through MPI-IO.

Before running the `configure` script, you should probably edit file `flags.guess` to make sure that it contains the best compiler options for your system. Known issues or things to check are:

<span>`Intel ifort compiler`</span>  
See if you need to add `-assume byterecl` for your machine. **In the case of that compiler, we have noticed that initial release versions sometimes have bugs or issues that can lead to wrong results when running the code, thus we *strongly* recommend using a version for which at least one service pack or update has been installed.** *In particular, for version 17 of that compiler, users have reported problems (making the code crash at run time) with the `-assume buffered_io` option; if you notice problems, remove that option from file `flags.guess` or change it to `-assume nobuffered_io` and try again.*

<span>`IBM compiler`</span>  
See if you need to add `-qsave` or `-qnosave` for your machine.

<span>`Mac OS`</span>  
You will probably need to install `XCODE`.

When compiling on an IBM machine with the `xlf` and `xlc` compilers, we suggest running the `configure` script with the following options:

    ./configure FC=xlf90_r MPIFC=mpif90 CC=xlc_r CFLAGS="-O3 -q64" FCFLAGS="-O3 -q64" -with-scotch-dir=...

If you have problems configuring the code on a Cray machine, i.e. for instance if you get an error message from the `configure` script, try exporting these two variables: `MPI_INC=$CRAY_MPICH2_DIR/include and FCLIBS= `, and for more details if needed you can refer to the `utils/Cray_compiler_information` directory. You can also have a look at the configure script called `utils/Cray_compiler_information/configure_SPECFEM_for_Piz_Daint.bash`.

On SGI systems, `flags.guess` automatically informs `configure` to insert ‘`` `TRAP_FPE=OFF ``’’ into the generated `Makefile` in order to turn underflow trapping off.

You can add `–enable-vectorization` to the configuration options to speed up the code in the fluid (acoustic) and elastic parts. This works fine if (and only if) your computer always allocates a contiguous memory block for each allocatable array; this is the case for most machines and most compilers, but not all. To disable this feature, use option `–disable-vectorization`. For more details see [github.com/geodynamics/specfem3d/issues/81](https://github.com/geodynamics/specfem3d/issues/81) . To check if that option works fine on your machine, run the code with and without it for an acoustic/elastic model and make sure the seismograms are identical.

Note that we use CUBIT (now called Trelis) to create meshes of hexahedra, but other packages can be used as well, for instance GiD from <http://gid.cimne.upc.es> or Gmsh from <http://geuz.org/gmsh> (Geuzaine and Remacle 2009). Even mesh creation packages that generate tetrahedra, for instance TetGen from <http://tetgen.berlios.de>, can be used because each tetrahedron can then easily be decomposed into four hexahedra as shown in the picture of the TetGen logo at <http://tetgen.berlios.de/figs/Delaunay-Voronoi-3D.gif>; while this approach does not generate hexahedra of optimal quality, it can ease mesh creation in some situations and it has been shown that the spectral-element method can very accurately handle distorted mesh elements (Oliveira and Seriani 2011).

The SPECFEM3D Cartesian software package relies on the SCOTCH library to partition meshes created with CUBIT. METIS (Karypis and Kumar 1998a; Karypis and Kumar 1998b; Karypis and Kumar 1998c) can also be used instead of SCOTCH if you prefer, by editing file src/decompose\_mesh/decompose\_mesh.F90 and uncommenting the flag USE\_METIS\_INSTEAD\_OF\_SCOTCH. You will also then need to install and compile Metis version 4.0 (do <span>\*</span>NOT<span>\*</span> install Metis version 5.0, which has incompatible function calls) and edit `src/decompose_mesh/Makefile.in` and uncomment the METIS link flag in that file before running `configure`.

The SCOTCH library (Pellegrini and Roman 1996) provides efficient static mapping, graph and mesh partitioning routines. SCOTCH is a free software package developed by François Pellegrini et al. from LaBRI and INRIA in Bordeaux, France, downloadable from the web page <https://gforge.inria.fr/projects/scotch/>. In case no SCOTCH libraries can be found on the system, the configuration will bundle the version provided with the source code for compilation. The path to an existing SCOTCH installation can to be set explicitly with the option `--with-scotch-dir`. Just as an example:

    ./configure FC=ifort MPIFC=mpif90 --with-scotch-dir=/opt/scotch

If you use the Intel ifort compiler to compile the code, we recommend that you use the Intel icc C compiler to compile Scotch, i.e., use:

    ./configure CC=icc FC=ifort MPIFC=mpif90

When compiling for GPU cards i.e. using CUDA, you can use:

`./configure –with-cuda`

for CUDA version 4, or

`./configure –with-cuda=cuda5`

for CUDA version 5, or

`./configure –with-cuda=cuda6`

for CUDA version 6, or

`./configure –with-cuda=cuda8`

for CUDA version 8.

Before CUDA version 5, one version supported basically one new architecture and needed a different kind of compilation. Since version 5, the compilation has stayed the same, but newer versions supported newer architectures. However at the moment, we still have one version linked to one specific architecture:

- CUDA 4 for Fermi, - CUDA 5 for Tesla K20 - CUDA 6 for Tesla K80 - CUDA 8 for Pascal P100.

So even if you have the new CUDA toolkit version 8, but you want to run on say a K20 GPU, then you would still configure with:

`./configure –with-cuda=cuda5`

The compilation should work and the cuda5 setting chooses the right architecture (-gencode=arch=compute\_35,code=sm\_35 for K20 cards).

So, type

`./configure –with-cuda=cuda8`

for Pascal P100 boards.

When compiling the SCOTCH source code, if you get a message such as: “ld: cannot find -lz”, the Zlib compression development library is probably missing on your machine and you will need to install it or ask your system administrator to do so. On Linux machines the package is often called “zlib1g-dev” or similar. (thus “sudo apt-get install zlib1g-dev” would install it)

To compile a serial version of the code for small meshes that fits on one compute node and can therefore be run serially, run `configure` with the `--without-mpi` option to suppress all calls to MPI.

A summary of the most important configuration variables follows.

<span>`F90`</span>  
Path to the Fortran compiler.

<span>`MPIF90`</span>  
Path to MPI Fortran.

<span>`MPI_FLAGS`</span>  
Some systems require this flag to link to MPI libraries.

<span>`FLAGS_CHECK`</span>  
Compiler flags.

The configuration script automatically creates for each executable a corresponding `Makefile` in the `src/` subdirectory. The `Makefile` contains a number of suggested entries for various compilers, e.g., Portland, Intel, Absoft, NAG, and Lahey. The software has run on a wide variety of compute platforms, e.g., various PC clusters and machines from Sun, SGI, IBM, Compaq, and NEC. Select the compiler you wish to use on your system and choose the related optimization flags. Note that the default flags in the `Makefile` are undoubtedly not optimal for your system, so we encourage you to experiment with these flags and to solicit advice from your systems administrator. Selecting the right compiler and optimization flags can make a tremendous difference in terms of performance. We welcome feedback on your experience with various compilers and flags.

Now that you have set the compiler information, you need to select a number of flags in the `constants.h` file depending on your system:

<span>`LOCAL_PATH_IS_ALSO_GLOBAL`</span>  
Set to `.false.` on most cluster applications. For reasons of speed, the (parallel) distributed database generator typically writes a (parallel) database for the solver on the local disks of the compute nodes. Some systems have no local disks, e.g., BlueGene or the Earth Simulator, and other systems have a fast parallel file system, in which case this flag should be set to `.true.`. Note that this flag is not used by the database generator or the solver; it is only used for some of the post-processing.

The package can run either in single or in double precision mode. The default is single precision because for almost all calculations performed using the spectral-element method using single precision is sufficient and gives the same results (i.e. the same seismograms); and the single precision code is faster and requires exactly half as much memory. Select your preference by selecting the appropriate setting in the `constants.h` file:

<span>`CUSTOM_REAL`</span>  
Set to `SIZE_REAL` for single precision and `SIZE_DOUBLE` for double precision.

In the `precision.h` file:

<span>`CUSTOM_MPI_TYPE`</span>  
Set to `MPI_REAL` for single precision and `MPI_DOUBLE_PRECISION` for double precision.

On many current processors (e.g., Intel, AMD, IBM Power), single precision calculations are significantly faster; the difference can typically be 10% to 25%. It is therefore better to use single precision. What you can do once for the physical problem you want to study is run the same calculation in single precision and in double precision on your system and compare the seismograms. If they are identical (and in most cases they will), you can select single precision for your future runs.

If your compiler has problems with the `use mpi` statements that are used in the code, use the script called `replace_use_mpi_with_include_mpif_dot_h.pl` in the root directory to replace all of them with `include ’mpif.h’` automatically.

Adding OpenMP support in addition to MPI
----------------------------------------

NOTE FROM JULY 2013: OpenMP support is maybe / probably not maintained any more. Thus the section below is maybe obsolete.

OpenMP support can be enabled in addition to MPI. However, in many cases performance will not improve because our pure MPI implementation is already heavily optimized and thus the resulting code will in fact be slightly slower. A possible exception could be IBM BlueGene-type architectures.

To enable OpenMP, uncomment the OpenMP compiler option in two lines in file `src/specfem3D/Makefile.in` (before running `configure`) and also uncomment the `#define USE_OPENMP` statement in file
`src/specfem3D/specfem3D.F90`.

The DO-loop using OpenMP threads has a SCHEDULE property. The `OMP_SCHEDULE` environment variable can set the scheduling policy of that DO-loop. Tests performed by Marcin Zielinski at SARA (The Netherlands) showed that often the best scheduling policy is DYNAMIC with the size of the chunk equal to the number of OpenMP threads, but most preferably being twice as the number of OpenMP threads (thus chunk size = 8 for 4 OpenMP threads etc). If `OMP_SCHEDULE` is not set or is empty, the DO-loop will assume generic scheduling policy, which will slow down the job quite a bit.

Compiling on an IBM BlueGene
----------------------------

Edit file `flags.guess` and put this for `FLAGS_CHECK`:

    -g -qfullpath -O2 -qsave -qstrict -qtune=qp -qarch=qp -qcache=auto -qhalt=w
    -qfree=f90 -qsuffix=f=f90 -qlanglvl=95pure -Q -Q+rank,swap_all -Wl,-relax

The most relevant are the -qarch and -qtune flags, otherwise if these flags are set to “auto” then they are wrongly assigned to the architecture of the frond-end node, which is different from that on the compute nodes. You will need to set these flags to the right architecture for your BlueGene compute nodes, which is not necessarily “qp”; ask your system administrator. On some machines if is necessary to use -O2 in these flags instead of -O3 due to a compiler bug of the XLF version installed. We thus suggest to first try -O3, and then if the code does not compile or does not run fine then switch back to -O2. The debug flags (-g, -qfullpath) do not influence performance but are useful to get at least some insights in case of problems.

Before running `configure`, select the XL Fortran compiler by typing `module load bgq-xl/1.0` or `module load bgq-xl` (another, less efficient option is to load the GNU compilers using `module load bgq-gnu/4.4.6` or similar).

Then, to configure the code, type this:

    ./configure FC=bgxlf90_r MPIFC=mpixlf90_r CC=bgxlc_r LOCAL_PATH_IS_ALSO_GLOBAL=true

In order for the SCOTCH domain decomposer to compile, on some (but not all) Blue Gene systems you may need to run `configure` with `CC=gcc` instead of `CC=bgxlc_r`.

To compile the code on an IBM BlueGene, Laurent Léger from IDRIS, France, suggests the following: compile the code with

    FLAGS_CHECK="-O3 -qsave -qstrict -qtune=auto -qarch=450d -qcache=auto \
      -qfree=f90 -qsuffix=f=f90 -g -qlanglvl=95pure -qhalt=w -Q \
      -Q+rank,swap_all -Wl,-relax"

Option -Wl,-relax must be added on many (but not all) BlueGene systems to be able to link the binaries `xmeshfem3D` and `xspecfem3D` because the final link step is done by the GNU `ld` linker even if one uses `FC=bgxlf90_r, MPIFC=mpixlf90_r` and `CC=bgxlc_r` to create all the object files. On the contrary, on some BlueGene systems that use the native AIX linker option -Wl,-relax can lead to problems and must be suppressed from `flags.guess`.

Also, `AR=ar, ARFLAGS=cru` and `RANLIB=ranlib` are hardwired in all `Makefile.in` files by default, but to cross-compile on BlueGene/P one needs to change these values to `AR=bgar, ARFLAGS=cru` and `RANLIB=bgranlib`. Thus the easiest thing to do is to modify all `Makefile.in` files and the `configure` script to set them automatically by `configure`. One then just needs to pass the right commands to the `configure` script:

    ./configure --prefix=/path/to/SPECFEM3DG_SP --host=Babel --build=BGP \
      FC=bgxlf90_r MPIFC=mpixlf90_r CC=bgxlc_r AR=bgar ARFLAGS=cru \
      RANLIB=bgranlib LOCAL_PATH_IS_ALSO_GLOBAL=false

This trick can be useful for all hosts on which one needs to cross-compile.

On BlueGene, one also needs to run the `xcreate_header_file` binary file manually rather than in the Makefile:

    bgrun -np 1 -mode VN -exe ./bin/xcreate_header_file

Visualizing the subroutine calling tree of the source code
----------------------------------------------------------

Packages such as `Doxywizard` can be used to visualize the calling tree of the subroutines of the source code. `Doxywizard` is a GUI front-end for configuring and running `Doxygen`.

To do your own call graphs, you can follow these simple steps below.

1.  Install `Doxygen` `graphviz` (the two are usually in the package manager of classic Linux distribution).

2.  Run in the terminal : `doxygen -g`, which creates a `Doxyfile` that tells doxygen what you want it to do.

3.  Edit the Doxyfile. Two Doxyfile-type files have been already committed in the directory
    `specfem3d/doc/Call_trees`:

    -   `Doxyfile_truncated_call_tree` will generate call graphs with maximum 3 or 4 levels of tree structure,

    -   `Doxyfile_complete_call_tree` will generate call graphs with complete tree structure.

    The important entries in the Doxyfile are:

    <span>`PROJECT_NAME`</span>  

    <span>`OPTIMIZE_FOR_FORTRAN`</span>  
    Set to YES

    <span>`EXTRACT_ALL`</span>  
    Set to YES

    <span>`EXTRACT_PRIVATE`</span>  
    Set to YES

    <span>`EXTRACT_STATIC`</span>  
    Set to YES

    <span>`INPUT`</span>  
    From the directory `specfem3d/doc/Call_trees`, it is `../../src/`

    <span>`FILE_PATTERNS`</span>  
    In SPECFEM case, it is `*.f90* *.F90* *.c* *.cu* *.h*`

    <span>`HAVE_DOT`</span>  
    Set to YES

    <span>`CALL_GRAPH`</span>  
    Set to YES

    <span>`CALLER_GRAPH`</span>  
    Set to YES

    <span>`DOT_PATH`</span>  
    The path where is located the dot program graphviz (if it is not in your $PATH)

    <span>`RECURSIVE`</span>  
    This tag can be used to turn specify whether or not subdirectories should be searched for input files as well. In the case of SPECFEM, set to YES.

    <span>`EXCLUDE`</span>  
    Here, you can exclude:

        ../../src/specfem3D/older_not_maintained_partial_OpenMP_port
        ../../src/decompose_mesh/scotch
        ../../src/decompose_mesh/scotch_5.1.12b

    <span>`DOT_GRAPH_MAX_NODES`</span>  
    to set the maximum number of nodes that will be shown in the graph. If the number of nodes in a graph becomes larger than this value, doxygen will truncate the graph, which is visualized by representing a node as a red box. Minimum value: 0, maximum value: 10000, default value: 50.

    <span>`MAX_DOT_GRAPH_DEPTH`</span>  
    to set the maximum depth of the graphs generated by dot. A depth value of 3 means that only nodes reachable from the root by following a path via at most 3 edges will be shown. Using a depth of 0 means no depth restriction. Minimum value: 0, maximum value: 1000, default value: 0.

4.  Run : `doxygen Doxyfile`, HTML and LaTeX files created by default in `html` and `latex` subdirectories.

5.  To see the call trees, you have to open the file `html/index.html` in your . You will have many informations about each subroutines of SPECFEM (not only call graphs), you can click on every boxes / subroutines. It show you the call, and, the caller graph of each subroutine : the subroutines called by the concerned subroutine, and the previous subroutines who call this subroutine (the previous path), respectively. In the case of a truncated calling tree, the boxes with a red border indicates a node that has arrows than are shown (in other words: the graph is truncated with respect to this node).

Finally, some useful links:

-   a good and short summary for the basic utilisation of Doxygen:

    <http://www.softeng.rl.ac.uk/blog/2010/jan/30/callgraph-fortran-doxygen/>,

-   to configure the diagrams :

    [http://www.stack.nl/ dimitri/doxygen/manual/diagrams.html](http://www.stack.nl/ dimitri/doxygen/manual/diagrams.html),

-   the complete alphabetical index of the tags in Doxyfile:

    [http://www.stack.nl/ dimitri/doxygen/manual/config.html](http://www.stack.nl/ dimitri/doxygen/manual/config.html),

-   more generally, the Doxygen manual:

    [http://www.stack.nl/ dimitri/doxygen/manual/index.html](http://www.stack.nl/ dimitri/doxygen/manual/index.html).

Using the ADIOS library for I/O
-------------------------------

Regular POSIX I/O can be problematic when dealing with large simulations one large clusters (typically more than \(10,000\) processes). SPECFEM3D use the ADIOS library Liu et al. (2013) to deal transparently take advantage of advanced parallel file system features. To enable ADIOS, the following steps should be done:

1.  Install ADIOS (available from <https://www.olcf.ornl.gov/center-projects/adios/>). Make sure that your environment variables reference it.

2.  You may want to change ADIOS related values in the `constants.h.in` file. The default values probably suit most cases.

3.  Configure using the `–with-adios` flag.

ADIOS is currently only usable for meshfem3D generated mesh (i.e. not for meshes generated with CUBTI). Additional control parameters are discussed in section [cha:Main-Parameter].

Becoming a developer of the code, or making small modifications in the source code
----------------------------------------------------------------------------------

If you want to develop new features in the code, and/or if you want to make small changes, improvements, or bug fixes, you are very welcome to contribute. To do so, i.e. to access the development branch of the source code with read/write access (in a safe way, no need to worry too much about breaking the package, there is a robot called BuildBot that is in charge of checking and validating all new contributions and changes), please visit this Web page: <https://github.com/geodynamics/specfem3d/wiki/Using-Hub>.

To visualize the call tree (calling tree) of the source code, you can see the Doxygen tool available in directory `doc/call_trees_of_the_source_code`.

References
----------

Geuzaine, C., and J. F. Remacle. 2009. “Gmsh: A Three-Dimensional Finite Element Mesh Generator with Built-in Pre- and Post-Processing Facilities.” *Int. J. Numer. Methods Eng.* 79 (11): 1309–31.

Karypis, George, and Vipin Kumar. 1998a. “A Fast and High-Quality Multilevel Scheme for Partitioning Irregular Graphs.” *SIAM Journal on Scientific Computing* 20 (1): 359–92.

———. 1998b. “A Parallel Algorithm for Multilevel Graph Partitioning and Sparse Matrix Ordering.” *Journal of Parallel and Distributed Computing* 48: 71–85.

———. 1998c. “Multilevel \(k\)-Way Partitioning Scheme for Irregular Graphs.” *Journal of Parallel and Distributed Computing* 48 (1): 96–129.

Liu, Qing, Jeremy Logan, Yuan Tian, Hasan Abbasi, Norbert Podhorszki, Jong Youl Choi, Scott Klasky, et al. 2013. “Hello ADIOS: the challenges and lessons of developing leadership class I/O frameworks.” *Concurrency and Computation: Practice and Experience*, n/a–/a. doi:[10.1002/cpe.3125](http://dx.doi.org/10.1002/cpe.3125).

Oliveira, S. P., and G. Seriani. 2011. “Effect of Element Distortion on the Numerical Dispersion of Spectral-Element Methods.” *Communications in Computational Physics* 9 (4): 937–58.

Pellegrini, F., and J. Roman. 1996. “SCOTCH: A Software Package for Static Mapping by Dual Recursive Bipartitioning of Process and Architecture Graphs.” *Lecture Notes in Computer Science* 1067: 493–98.

-----
> This documentation has been automatically generated by [pandoc](http://www.pandoc.org)
> based on the User manual (LaTeX version) in folder doc/USER_MANUAL/
> (Mar 10, 2020)

