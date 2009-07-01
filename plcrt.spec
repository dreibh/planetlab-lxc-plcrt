#
# $Id$
# 

%define url $URL: svn+ssh://svn.planet-lab.org/svn/PLCRT/trunk/plcrt.spec $

%define name plcrt
%define version 1.0
%define taglevel 2

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %(echo %{url} | cut -d ' ' -f 2)

Summary: PLCRT account initialization for the root image.
Group: Applications/System
Requires: python
Requires: perl
Requires: rt3
Requires: rt3-mailgate
Requires: myplc

%description
PLCRT is a collection of configuration scripts for configuring RT.
By default RT does not come with all the settings needed for a standard PLC,
or PlanetLab in particular.  

%prep
%setup -q

%install

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -D -m 755 plcrt.init $RPM_BUILD_ROOT/%{_sysconfdir}/plc.d/plcrt

echo " * Installing core scripts"
rsync -a ./ $RPM_BUILD_ROOT/%{_datadir}/%{name}/

echo " * Installing cron scripts"
install -D -m 644 rt.cron $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/rt.cron

chmod 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/adduserstort.pl
chmod 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/cron.d/*.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
#%config /etc/plcrt.conf
%{_datadir}/%{name}
%{_sysconfdir}/plc.d/plcrt
%{_sysconfdir}/cron.d/rt.cron

%post
if grep 'pam_loginuid.so' /etc/pam.d/crond ; then
    sed -i -e 's/^session    required   pam_loginuid.so/#session    required   pam_loginuid.so/g' /etc/pam.d/crond
fi

if ! grep '<category id="plc_rt">' /etc/planetlab/default_config.xml ; then 
    sed -i 's|<category id="plc_net">| <category id="plc_rt">\n <name>RT Configuration</name>\n <description>RT</description>\n <variablelist>\n <variable id="enabled" type="boolean">\n <name>Enabled</name>\n <value>false</value>\n <description>Enable on this machine.</description>\n </variable>\n <variable id="host" type="hostname">\n <name>Hostname</name>\n <value>localhost.localdomain</value>\n <description>The fully qualified hostname.</description>\n </variable>\n <variable id="ip" type="ip">\n <name>IP Address</name>\n <value/>\n <description>The IP address of the RT server.</description>\n </variable>\n </variablelist>\n </category>\n <category id="plc_net">|' /etc/planetlab/default_config.xml
fi

mkdir -p /etc/planetlab/configs
plc-config --save /etc/planetlab/configs/site.xml \
		--category plc_rt --variable enabled --value true

mkdir -p /var/log/rt3
touch /var/log/rt3/rt.log
chown apache.apache /var/log/rt3/rt.log

%changelog
* Tue Jun 30 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-2
- improved init setup
- added plcsh version of getadmins script to add users to RT's db.
- improved %post code for installation

* Fri Jun 26 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-1
- trying to get the tag to work for new package.

* Thu Jun 26 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-1
- initial addition.
