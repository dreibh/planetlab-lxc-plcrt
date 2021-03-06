#
# $Id$
# 

%define url $URL: svn+ssh://svn.planet-lab.org/svn/PLCRT/trunk/plcrt.spec $

%define name plcrt
%define version 1.0
%define taglevel 11

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

function install_file()
{
    mod=$1
    dest=$2
    file=$3
    if [ -z "$file" ] ; then 
        file=$( basename $dest )
    fi
    if [ -f $file ] ; then
        install -D -m $mod $file $dest
    fi
}
function chmod_pattern()
{
    mod=$1
    pattern=$2
    for file in $pattern ; do 
        if [ -f $file ] ; then
            chmod $mod $file
        fi
    done
}

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
install_file 755 $RPM_BUILD_ROOT/%{_sysconfdir}/plc.d/plcrt plcrt.init

echo " * Installing core scripts"
rsync -a ./ $RPM_BUILD_ROOT/%{_datadir}/%{name}/

install_file 644 $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/rt.cron
install_file 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/getpersons.py
install_file 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/adduserstort.pl

echo " * Installing cron scripts"
chmod_pattern 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/cron.d/*.py 
chmod_pattern 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/cron.d/*.sh


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
    sed -i 's|<category id="plc_net">| <category id="plc_rt">\n <name>RT Configuration</name>\n <description>RT</description>\n <variablelist>\n <variable id="enabled" type="boolean">\n <name>Enabled</name>\n <value>false</value>\n <description>Enable on this machine.</description>\n </variable>\n <variable id="host" type="hostname">\n <name>Hostname</name>\n <value>localhost.localdomain</value>\n <description>The fully qualified hostname.</description>\n </variable>\n <variable id="ip" type="ip">\n <name>IP Address</name>\n <value/>\n <description>The IP address of the RT server.</description>\n </variable>\n <variable id="web_user" type="string">\n <name>username</name>\n <value>root</value>\n <description>The user name for RT access.</description>\n </variable>\n <variable id="web_password" type="password">\n <name>password</name>\n <value>password</value>\n <description>password to the rt user.</description>\n </variable>\n <variable id="cc_address" type="email">\n <name>email list</name>\n <value>root+list@localhost.localdomain</value>\n <description></description>\n </variable>\n <variable id="dbpassword" type="password">\n <name>Database Password</name>\n <value></value>\n <description>Password to use when accessing the RT database.</description>\n </variable>\n </variablelist>\n </category>\n <category id="plc_net">|' /etc/planetlab/default_config.xml
fi

mkdir -p /etc/planetlab/configs
plc-config --category plc_rt --variable cc_address \
    --value 'root+list@localhost.localdomain'\
    --save /etc/planetlab/default_config.xml /etc/planetlab/default_config.xml

plc-config --category plc_rt --variable enabled --value true \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/default_config.xml

# NOTE: setup default values until myplc includes them by default.
plc-config --category plc_rt --variable host --value localhost.localdomain \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/configs/site.xml 
plc-config --category plc_rt --variable ip --value "" \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/configs/site.xml 
plc-config --category plc_rt --variable web_user --value root \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/configs/site.xml 
plc-config --category plc_rt --variable web_password --value password \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/configs/site.xml 
plc-config --category plc_rt --variable dbpassword --value "" \
    --save /etc/planetlab/configs/site.xml /etc/planetlab/configs/site.xml 

# NOTE: not sure why these aren't setup by the rt package...
mkdir -p /var/log/rt3
touch /var/log/rt3/rt.log
chown apache.apache /var/log/rt3/rt.log

cp /usr/share/rt3/html/NoAuth/images/bplogo.gif /var/www/html/misc/logo.gif

%changelog
* Tue Nov 03 2009 Marc Fiuczynski <mef@cs.princeton.edu> - PLCRT-1.0-11
- Make sure to do updates to sendmail files, rather than appeneding same
- hostname values to the end of files.

* Mon Sep 21 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-10
- add reverse-lookup on given host IP addr to add any extra hostnames this
- server may be aliasing as.

* Mon Sep 21 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-9
- be more selective about which files to chmod

* Mon Sep 21 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-8
- shorter polling period for faster sync
- remove attempt to install removed file

* Sun Sep 20 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-7
- replace callplcsh with simpler scripts for syncing users

* Sat Sep 19 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-6
- some plcs don't return site_ids so getpersons should not depend on this field
- make scripts exec on install
- use RT_HOST name rather than localhost for RT mailgate configuration

* Wed Jul 08 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-5
- add mailing list watchers to default queues
- add script to addwatchers to default queues
- improved templates in plcrt.init

* Mon Jul 06 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-4
- rt db password
- template conf.d/* files rather than one-shot re-write
- better %post in spec file for logo and default xml settings.

* Sat Jul 04 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-3
- renamed getpersons.py to accept a given 'role'
- changed syncadmins.sh to use callplcsh.py
- added callplcsh.py to allow either a local or remote plc using plcsh

* Tue Jun 30 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-2
- improved init setup
- added plcsh version of getadmins script to add users to RT's db.
- improved %post code for installation

* Fri Jun 26 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-1
- trying to get the tag to work for new package.

* Thu Jun 26 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - PLCRT-1.0-1
- initial addition.
