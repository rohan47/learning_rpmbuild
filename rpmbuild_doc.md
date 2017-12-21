# Building RPM for personal project.
The project for which i am building the rpm is a python cgi based web application. The files need to be present in the document root of the apache server i.e., html and css files in html(by default) folder and the python cgi files in the cgi-bin folder.

1. Install **rpm-build** and **rpmdevtools**.
   ```
   $ yum install rpm-build rpmdevtools
   ```
2. Now run the bellow command, that will setup the directory structure required for rpmbuild as shown in the directory tree bellow. 
   ```
   $ rpmdev-setuptree
   ```
   
   - **BUILD** - The rpmbuild command builds software in this directory.   
   - **RPMS** - The rpmbuild command stores binary RPMs it creates in this directory.
      *NOTE*:Binary packages are likely the real reason to make an RPM. We can package an application, a programming library, or almost anything we want. Armed with a binary RPM, we can transfer one file to another machine and install the application there, taking full advantage of the RPM system.
   - **SOURCES** - The sources for the application should be put in this directory.
   - **SPEC** - The spec file for each RPM we plan to build should be in this directory.
   - **SRPMS** - The rpmbuild command stores source RPMs it creates in this directory.
      *NOTE*:Creating a source RPM also allows us to transfer the entire set of sourc es for a package to another system, since the source. RPM is just one file and it contains all the program sources along with the instructions, called a spec file, for building the binary RPM. Furthermore, creating a source RPM makes it easier to create binary RPMs on different processor architectures or different versions of Linux.

3. Go to SOURCES directory and create a directory with the name of your project and then copy the html and cgi-bin folder into that directory. example SOURCES/myproject/html/* and SOURCES/myproject/cgi-bin/*
4. Create SPECS/myproject.spec file. This file is the main file which has the specification for the rpm that is going to be created.

So the directory structure till now:

```
    rpmbuild
    |-- BUILD
    |-- RPMS
    |-- SOURCES
    |   `-- myproject
    |       |-- cgi-bin
    |       |   `-- <all cgi files>
    |       `-- html
    |           |-- css
    |           |   `-- <css files>
    |           |-- <all html files>
    |-- SPECS
    |   `-- myproject.spec
    |-- SRPMS
```

## The myproject.spec file

```
# %define is used to define macros

%define _topdir     /home/harry/rpmbuild      # _topdir has the complete path to rpmbuild dir.
%define name        myproject                 # name of the project
%define release     1                         # release of the project. Its 1 because it is the 1st release
%define version     1                           
%define buildroot   %{_topdir}/%{name}-%{version}-root  # It is the mock location where the project will be copied during the rpmbuild process where the project files will be packed into rpm.

# The specifications of the project
BuildRoot:      %{buildroot}                      # value of buildroot is assigned to BuildRoot
Summary:        This is my project
License:        none
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source:         %{name}
Prefix:         /var                             # to make the package relocable
Group:          Development/Tools                # the group or catagory in which the project belongs
Requires:       tty,shellinabox,ansible,httpd,python2,
                pip,libvirt,qemu-kvm,virt-manager        # the tools required by the project

%description
This is my cloud.

# This section contains commands to be executed to install the files. Here the commands are for the buildroot directory and will be executed during the rpm build process but the same will happen during installing the rpm in the system.
%install

# Here are the commands that will copy the contents of html and cgi-bin folder present in the source directory to the /var/www/html , /var/www/cgi-bin directory respectively.
mkdir -p %{buildroot}/var/www/html
mkdir -p %{buildroot}/var/www/cgi-bin
cp -rf  %{_topdir}/SOURCES/myproject/cgi-bin/* %buildroot/var/www/cgi-bin/
cp -rf  %{_topdir}/SOURCES/myproject/html/* %buildroot/var/www/html/

# we set the permissions to the copied files and the files are moved from the buildroot to the system root /var/www/* .
%files
%defattr(0777, root,root)
/var/www/cgi-bin/*
/var/www/html/*

# cleaning the build root directory.
%clean            
rm -rf $RPM_BUILD_ROOT

```

5. Now run the following command to build the rpm.
   ``` 
   $ rpmbuild -v -bb --clean ~/myprojectrpm/SPECS/myproject.spec  
   ```
   This command uses the named spec file to build a binary package (-bb for "build binary") with verbose output (-v). 
   The build utility removes the build tree after the packages are made (--clean). 

   rpmbuild performs the following steps:

       - Reads and parses the myproject.spec file.
       - Runs the %prep section to copy the source code into a temporary directory. Here, the temporary directory is BUILD.
       - Runs the %install section to install the code into directories on the build machine.
       - Reads the list of files from the %files section, gathers them up, and creates a binary RPM (and source RPM files, if you elect). 

6. The rpm created will be present in the RPM directory.



## SIGNING THE CREATED RPM:

To sign the rpm we need to have gnupg tool installed.

1. The following command generates the key after you fill the required info an give an appropriate passphrase.
   ```
   $ gpg  --gen-key
   ```

2. You can check the keys using the following command:
   ```
   $ gpg --list-keys --fingerprint 
   /home/vagrant/.gnupg/pubring.gpg
   --------------------------------
   pub   2048R/52FF0C17 2017-07-25 [expires: 2019-07-25]
         Key fingerprint = D03A 419B 6EB3 D392 425A  14DB 8BF2 6C03 52FF 0C17
   uid                  rohan
   sub   2048R/0AB04010 2017-07-25 [expires: 2019-07-25]
   ```

3. Now we export the key into a file:
   ```
   $ gpg --export --armor "rohan" > TEST-RPM-GPG-KEY
   ```

4. Now import the key into rpm 
   ```
   $ rpm --import TEST-RPM-GPG-KEY
   ```

5. Enter the following in ~/.rpmmacros:
   ```
   %_signature         %gpg
   %_gpg_name          rohan
   ```
   
6. To sign the rpm package 
   ```
   $ rpm --resign tree-1.5.3-2.el7.centos.x86_64.rpm
   ```
   
7. To check the signature of the package:
   ```
   $ rpm -qip tree-1.5.3-2.el7.centos.x86_64.rpm
   ```

## EXTRA SPEC FILE SECTIONS 

```
%pre        # Steps to be taken before installation of a package.
%post       # Steps to be taken after installation of a package.
%preun      # Steps to be taken before removal of package.
%postun     # Stepd to be taken after removal of packages.
```
