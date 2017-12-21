%define _topdir           /home/harry/rpmbuild      
%define name              myproject                 
%define release           1              
%define version           1                           
%define buildroot         %{_topdir}/%{name}-%{version}-root  

BuildRoot:      %{buildroot}      
Summary:        This is my project
License:        none
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source:         %{name}
Prefix:         /var    
Group:          Applications/System 
Requires:       tty,shellinabox,ansible,httpd,python2,
                pip,libvirt,qemu-kvm,virt-manager

%description
This is my cloud.

%install

mkdir -p %{buildroot}/var/www/html
mkdir -p %{buildroot}/var/www/cgi-bin
cp -rf  %{_topdir}/SOURCES/myproject/cgi-bin/* %buildroot/var/www/cgi-bin/
cp -rf  %{_topdir}/SOURCES/myproject/html/* %buildroot/var/www/html/

%files
%defattr(0777, root,root)
/var/www/cgi-bin/*
/var/www/html/*

%clean            
rm -rf $RPM_BUILD_ROOT

