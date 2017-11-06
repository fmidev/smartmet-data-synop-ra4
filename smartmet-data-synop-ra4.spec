%define smartmetroot /smartmet

Name:           smartmet-data-synop-ra4
Version:        17.11.6
Release:        1%{?dist}.fmi
Summary:        SmartMet Data SYNOP RA4
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-synop-ra4
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       smartmet-qdtools
Requires:       lbzip2
Requires:       wget

%description
TODO

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/synop
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/synop
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/synop/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/synop-ra4.cron <<EOF
*/20 * * * * /smartmet/run/data/synop/bin/get_synop_ra4.sh &> /smartmet/logs/data/synop.log
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_synop <<EOF
#!/bin/sh
# Clean SYNOP data
cleaner -maxfiles 2 '_synop.sqd' %{smartmetroot}/data/gts/synop
cleaner -maxfiles 2 '_ship.sqd' %{smartmetroot}/data/gts/ship
cleaner -maxfiles 2 '_buoy.sqd' %{smartmetroot}/data/gts/buoy
cleaner -maxfiles 2 '_synop.sqd' %{smartmetroot}/editor/in
cleaner -maxfiles 2 '_ship.sqd' %{smartmetroot}/editor/in
cleaner -maxfiles 2 '_buoy.sqd' %{smartmetroot}/editor/in

# Clean incoming SYNOP data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/synop -type f -mmin +10080 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-synop-ra4/get_synop_ra4.sh %{buildroot}%{smartmetroot}/run/data/synop/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/synop-ra4.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_synop
%attr(2775,smartmet,gts)  %dir %{smartmetroot}/data/incoming/synop
%{smartmetroot}/*

%changelog
* Mon Nov 6 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.6-1.el7.fmi
- Switch from bzip2 to lbzip2 for faster operations
* Fri Apr 21 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.4.21-1.el7.fmi
- Initial Version
