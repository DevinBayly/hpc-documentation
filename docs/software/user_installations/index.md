# User Installations

## Package managers

Many popular programs, in particular [Python](../popular_software/python_and_anaconda/python/) and [R](../popular_software/R/) have built-in package managers that can be used to collect new software from the internet and easily install them to your environment. See the section corresponding to your prefered language on the left under the "Popular Software" heading for more detailed instructions.

## Manual installations

You are encouraged to download and compile(1) any desired software in your own account. Commands like ```git clone``` and ```wget``` are available to pull repositories from the internet. The installation process may involve changing install locations from system folders (e.g. ```/usr/bin/xyz```) to user folders (e.g. ```/home/ux/netid/``` or ```/groups/pi_netid/netid/```), and will vary substantially from software to software, so providing instructions for all cases is beyond the scope of this page. If you encounter difficulties while installing your own software, the HPC Consult team is available for assistance. 
{ .annotate }

1.  on a compute node!

While you cannot add or update system software or libraries using tools that require root privileges such as ```yum```, many software packages can be installed locally without needing to be a superuser. Frequently linux packages make use of the "```configure```, ```make```, ```make install```" method which allows you to customize your installation location. An example of how to do this is shown below. 

!!! tip 
    * Software is not available on the login nodes. To install custom software, log into an interactive session.
    * For a typical Linux installation, the default settings may attempt to install files in system locations. This is not permitted, so the installation process (specifically, the ```./configure``` step) needs to be changed so that files are installed somewhere you have write access to.  There is frequently done with the syntax ```--prefix=/path/to/software```.
    
=== "configure/make/make install example"
    Here is a typical example of installing software on a Linux cluster with the ```configure```, ```make```, ```make install``` method. We'll use a simple hello world example downloaded from [https://ftp.gnu.org/gnu/hello/](https://ftp.gnu.org/gnu/hello/)

    1. **Download and unpack the software**

        ```
        [user@cpu39 make_example]$ wget https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz
        [user@cpu39 make_example]$ tar xzvf hello-2.10.tar.gz 
        [user@cpu39 make_example]$ cd hello-2.10
        ```
    
    2. **Configure your software**

        The ```./configure``` command generates a Makefile tailored to the specific environment and requirements of the system where the software is being installed. The use of the ```--prefix``` option allows users to install the software to a custom directory, circumventing the standard root locations which users do not have permission to modify. In this example, we'll install the software to a directory called hello_world in our home. 

        ```
        [user@cpu39 hello-2.10]$ ./configure --prefix=$HOME/hello_install
        ```
    
    3. **Compile and install your software**

        !!! tip
            Often, there is an additional option to test your software after compiling it and before installing it. Usually, this is something like ```make test``` or ```make check```

        The ```make``` command compiles the software according to the instructions provided in the Makefile generated by `./configure`. Once the software is compiled, ```make install``` will install the software in the directory you specified with the ```--prefix``` option.

        ```
        [user@cpu39 hello-2.10]$ make
        [user@cpu39 hello-2.10]$ make install
        [user@cpu39 hello-2.10]$ ls $HOME/hello_install 
        bin  share
        ```

    4. **Modify your environment**

        Different environment variables control where the system looks for executables, libraries, header files, etc. Modifying your environment variables will allow you to use your new software without specifying the full paths. These variables can either be set manually on the command line for each new session, or can be added to your bashrc to make the changes permanent. For more information, see the sections Environment Variables and Hidden Files and Directories in our [Bash cheat sheet](../../support_and_training/cheat_sheet/).

        ```
        [user@cpu39 hello-2.10]$ export PATH=$HOME/hello_install/bin:$PATH
        ```

    5. **Use your software**

        ```
        [user@cpu39 hello-2.10]$ hello
        Hello, world!
        ```

=== "cmake"

    Here is a typical example of installing software on a Linux cluster with the ```cmake``` method. We'll use the software library Eigen as an example. 

    1. **Download the software**

        In this example, we'll ```git clone``` the source code from the Gitlab repository [https://gitlab.com/libeigen/eigen](https://gitlab.com/libeigen/eigen)

        ```
        [user@cpu39 cmake_example]$ git clone https://gitlab.com/libeigen/eigen.git
        [user@cpu39 cmake_example]$ cd eigen/
        ```

    2. **Create and set your build environment**

        Next, create a subdirectory called build where build files will be generated and stored. 
        
        ```
        [user@cpu39 eigen]$ mkdir build
        [user@cpu39 eigen]$ cd build
        ```

        Additionally, you'll often need to set some environment variables to point to compilers and libraries. In this case, we'll set ```CC``` (which sets your C compiler), ```CXX``` (which sets your C++ compiler), and ```FC``` (which sets your Fortran compiler).

        ```
        [user@cpu39 build]$ export CC=$(which gcc)
        [user@cpu39 build]$ export CXX=$(which g++)
        [user@cpu39 build]$ export FC=$(which gfortran)
        ```

        !!! tip
            The command ```which``` returns a full filepath to an executable. Running something like ```export FOO=$(which foo)``` will take the output of ```which foo``` and store it as the environment variable ```FOO```

    3. **Configure your build**

        Use ```cmake``` to configure your build. Use ```-DCMAKE_INSTALL_PREFIX``` to set a custom installation directory that you have access to. This will prevent the installation process from trying to access default root-owned locations which users don't have permission to modify. The ```..``` is a shortcut for the directory one level above which is where the CMakeLists.txt file lives.

        ```
        [user@cpu39 build]$ cmake -DCMAKE_INSTALL_PREFIX=$HOME/eigen_install ..
        ```

    4. **Compile and install your software**

        ```
        [user@cpu39 build]$ make
        [user@cpu39 build]$ make install
        [user@cpu39 build]$ ls $HOME/eigen_install
        include  share
        ```
    
    5. **Modify your environment**

        Different environment variables control where the system looks for executables, libraries, header files, etc. Modifying your environment variables will allow you to use your new software without specifying the full paths. These variables can either be set manually on the command line for each new session, or can be added to your bashrc to make the changes permanent. For more information, see the sections Environment Variables and Hidden Files and Directories in our [Bash cheat sheet](../../support_and_training/cheat_sheet/).

        In this case, we'll set ```INCLUDE``` and ```CPPFLAGS```

        ```
        [user@cpu39 build]$ export INCLUDE=$HOME/eigen_install:$INSTALL
        [user@cpu39 build]$ export CPPFLAGS="-I$HOME/eigen_install $CPPFLAGS"
        ```
