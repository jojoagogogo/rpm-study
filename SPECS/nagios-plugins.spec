### rpmbuild -ba --define="__check_files %{nil}" SPECS/nagios-plugins.spec
Name: nagios-plugins
Version: 1.4.16
Release: 5%{?dist}_smtp_gx
Summary: Host/service/network monitoring program plugins for Nagios

Group: Applications/System
License: GPLv2+
URL: http://nagiosplug.sourceforge.net/
Source0: http://downloads.sourceforge.net/nagiosplug/%{name}-%{version}.tar.gz
Source1: nagios-plugins.README.Fedora
Patch1:	nagios-plugins-0001-Do-not-use-usr-local-for-perl.patch
Patch2: nagios-plugins-0002-Remove-assignment-of-not-parsed-to-jitter.patch
Patch3: nagios-plugins-0003-Fedora-specific-fixes-for-searching-for-diff-and-tai.patch
Patch4: nagios-plugins-0004-Fedora-specific-patch-for-not-to-fixing-fully-qualif.patch
# https://bugzilla.redhat.com/512559
Patch6: nagios-plugins-0006-Prevent-check_swap-from-returning-OK-if-no-swap-acti.patch
Patch7: nagios-plugins-0007-undef-gets-and-glibc-2.16.patch
Patch8: nagios-plugins-0008-ntpdate-and-ntpq-paths.patch
Patch555: check_smtp.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: openldap-devel
#BuildRequires: mysql-devel
#BuildRequires: net-snmp-devel
#BuildRequires: net-snmp-utils
#BuildRequires: samba-client
#BuildRequires: postgresql-devel
BuildRequires: gettext
BuildRequires: %{_bindir}/ssh
BuildRequires: bind-utils
#BuildRequires: ntp
#BuildRequires: %{_bindir}/mailq
#BuildRequires: %{_sbindir}/fping
#BuildRequires: perl(Net::SNMP)
#%if 0%{?el4}
#%else
#BuildRequires: radiusclient-ng-devel
#%endif
BuildRequires: qstat

Requires: nagios-common >= 3.3.1-1

# nagios-plugins-1.4.16: the included gnulib files were last updated
# in June/July 2010
# Bundled gnulib exception (https://fedorahosted.org/fpc/ticket/174)
Provides: bundled(gnulib)

%global reqfilt sh -c "%{__perl_requires} | sed -e 's!perl(utils)!nagios-plugins-perl!'"
%define __perl_requires %{reqfilt}


%description
Nagios is a program that will monitor hosts and services on your
network, and to email or page you when a problem arises or is
resolved. Nagios runs on a Unix server as a background or daemon
process, intermittently running checks on various services that you
specify. The actual service checks are performed by separate "plugin"
programs which return the status of the checks to Nagios. This package
contains those plugins.

%package smtp
Summary: Nagios Plugin - check_smtp
Group: Applications/System
Requires: nagios-plugins = %{version}-%{release}

%description smtp
Provides check_smtp support for Nagios.

%prep
%setup -q
%patch1 -p1 -b .no_usr_local
%patch2 -p1 -b .not_parsed
%patch3 -p1 -b .proper_paths
%patch4 -p1 -b .no_need_fo_fix_paths
%patch6 -p1 -b .fix_missing_swap
%patch7 -p1 -b .gets
%patch8 -p1 -b .ext_ntp_cmds
%patch555 -p1 -b .check_smtp

%build
%configure \
	--libexecdir=%{_libdir}/nagios/plugins \
	--with-mysql \
	PATH_TO_QSTAT=%{_bindir}/quakestat \
	PATH_TO_FPING=%{_sbindir}/fping \
	PATH_TO_NTPQ=%{_sbindir}/ntpq \
	PATH_TO_NTPDC=%{_sbindir}/ntpdc \
	PATH_TO_NTPDATE=%{_sbindir}/ntpdate \
	PATH_TO_RPCINFO=%{_sbindir}/rpcinfo \
	--with-ps-command="`which ps` -eo 's uid pid ppid vsz rss pcpu etime comm args'" \
	--with-ps-format='%s %d %d %d %d %d %f %s %s %n' \
	--with-ps-cols=10 \
	--enable-extra-opts \
	--with-ps-varlist='procstat,&procuid,&procpid,&procppid,&procvsz,&procrss,&procpcpu,procetime,procprog,&pos'

make %{?_smp_mflags}
cd plugins
#make check_ide_smart
#make check_ldap
#%if 0%{?el4}
#%else
#make check_radius
#%endif
#make check_pgsql

cd ..

#gawk -f plugins-scripts/subst contrib/check_linux_raid.pl > contrib/check_linux_raid
#mv plugins-scripts/check_ntp.pl plugins-scripts/check_ntp.pl.in
#gawk -f plugins-scripts/subst plugins-scripts/check_ntp.pl.in > plugins-scripts/check_ntp.pl

#cp %{SOURCE1} ./README.Fedora

%install
sed -i 's,^MKINSTALLDIRS.*,MKINSTALLDIRS = ../mkinstalldirs,' po/Makefile
rm -rf %{buildroot}
make AM_INSTALL_PROGRAM_FLAGS="" DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/nagios/plugins
install -m 0755 plugins/check_smtp %{buildroot}/%{_libdir}/nagios/plugins/check_smtp_gx


#install -m 0755 plugins-root/check_icmp %{buildroot}/%{_libdir}/nagios/plugins
#install -m 0755 plugins-root/check_dhcp %{buildroot}/%{_libdir}/nagios/plugins
#install -m 0755 contrib/check_linux_raid %{buildroot}/%{_libdir}/nagios/plugins
#install -m 0755 plugins/check_ide_smart %{buildroot}/%{_libdir}/nagios/plugins
#install -m 0755 plugins/check_ldap %{buildroot}/%{_libdir}/nagios/plugins
#install -m 0755 plugins-scripts/check_ntp.pl %{buildroot}/%{_libdir}/nagios/plugins
#%if 0%{?el4}
#%else
#install -m 0755 plugins/check_radius %{buildroot}/%{_libdir}/nagios/plugins
#%endif
#install -m 0755 plugins/check_pgsql %{buildroot}/%{_libdir}/nagios/plugins

#%ifarch ppc ppc64 sparc sparc64
#rm -f %{buildroot}/%{_libdir}/nagios/plugins/check_sensors
#%endif

#chmod 644 %{buildroot}/%{_libdir}/nagios/plugins/utils.pm

#%find_lang %{name}

%clean
rm -rf %{buildroot}

#%files -f %{name}.lang
#%defattr(-,root,root,-)
#%doc ACKNOWLEDGEMENTS AUTHORS BUGS ChangeLog CODING COPYING FAQ LEGAL NEWS README REQUIREMENTS SUPPORT THANKS README.Fedora
#%{_libdir}/nagios/plugins/negate
#%{_libdir}/nagios/plugins/urlize
#%{_libdir}/nagios/plugins/utils.sh

#%files all

%files smtp
%defattr(-,root,root,-)
%{_libdir}/nagios/plugins/check_smtp_gx

%changelog
* Fri Aug 17 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.16-5
- Fix the use lib statement and the external ntp commands paths in check-ntp.pl
  (nagios-plugins-0008-ntpdate-and-ntpq-paths.patch).

* Thu Aug 16 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.16-4
- Remove the erroneous requirements of nagios-plugins-ntp (#848830)
- Ship check-ntp.pl in the new nagios-plugins-ntp-perl subpackage (#848830)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.16-2
- Provides bundled(gnulib) (#821779)

* Mon Jul  9 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.16-1
- Update to version 1.4.16
- Dropped nagios-plugins-0005-Patch-for-check_linux_raid-with-on-linear-raid0-arra.patch
  (upstream).

* Tue Jun 26 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.15-7
- glibc 2.16 no longer defines gets for ISO C11, ISO C++11, and _GNU_SOURCE
  (#835621): nagios-plugins-0007-undef-gets-and-glibc-2.16.patch

* Tue Jun 26 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4.15-6
- The nagios-plugins RPM no longer needs to own the /usr/lib{,64}/nagios/plugins
  directory; this directory is now owned by nagios-common (#835621)
- Small updates (clarification) to the file nagios-plugins.README.Fedora

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.4.15-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.15-2
- Dropped check_udp sub-package (see rhbz #634067). Anyway it
  provided just a symlink to check_tcp.
- Fixed weird issue with check_swap returning ok in case of
  missing swap (see rhbz #512559).

* Wed Aug 18 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.15-1
- Ver. 1.4.15
- Dropped patch for restoration of behaviour in case of ssl checks

* Tue May 18 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.14-4
- Restore ssl behaviour for check_http in case of self-signed
  certificates (see rhbz #584227).

* Sat Apr 24 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.14-3
- Removed Requires - nagios (see rhbz #469530).
- Added "Requires,Requires(pre): group(nagios)" where necessary
- Sorted %%files sections
- No need to ship INSTALL file
- Added more doc files to main package

* Mon Apr 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.14-2
- Added missing Requires - nagios (see rhbz #469530).
- Fixed path to qstat -> quakestat (see rhbz #533777)
- Disable radius plugin for EL4 - there is not radiuscleint-ng for EL-4

* Wed Mar 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4.14-1
- Ver. 1.4.14
- Rebased patches.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.13-17
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Mike McGrath <mmcgrath@redhat.com> - 1.4.13-15
- Added patch from upstream to fix ntp faults (bz #479030)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 1.4.13-13
- rebuild for dependencies

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.4.13-12
- rebuild with new openssl

* Mon Oct 20 2008 Robert M. Albrecht <romal@gmx.de> 1.4.13-11
- Enabled --with-extra-opts again

* Mon Oct 20 2008 Robert M. Albrecht <romal@gmx.de> 1.4.13-10
- removed provides perl plugins Bugzilla 457404

* Thu Oct 16 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-9
- This is a "CVS is horrible" rebuild

* Thu Oct  9 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-8
- Rebuilt with a proper patch

* Wed Oct  8 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-7
- Added changed recent permission changes to allow nagios group to execute

* Wed Oct  8 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-6
- Fixed up some permission issues

* Mon Oct  6 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-5
- Fixing patch, missing semicolon

* Sun Sep 28 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.13-4
- Upstream released new version #464419
- Added patch fix for check_linux_raid #253898
- Upstream releases fix for #451015 - check_ntp_peers
- Upstream released fix for #459309 - check_ntp
- Added Provides Nagios::Plugins for #457404
- Fixed configure line for #458985 check_procs

* Tue Jul 10 2008 Robert M. Albrecht <romal@gmx.de> 1.4.12-3
- Removed --with-extra-opts, does not build in Koji

* Mon Jun 30 2008 Robert M. Albrecht <romal@gmx.de> 1.4.12-2
- Enabled --with-extra-opts

* Sun Jun 29 2008 Robert M. Albrecht <romal@gmx.de> 1.4.12-1
- Upstream released version 1.4.12
- Removed patches ping_timeout.patch and pgsql-fix.patch

* Wed Apr 30 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.11-4
- added patch for check_pgsql

* Wed Apr 09 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.11-2
- Fix for 250588

* Thu Feb 28 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.11-1
- Upstream released version 1.4.11
- Added check_ntp peer and time

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.10-6
- Autorebuild for GCC 4.3

* Tue Feb 12 2008 Mike McGrath <mmcgrath@redhat.com> 1.4-10-5
- Rebuild for gcc43

* Thu Jan 10 2008 Mike McGrath <mmcgrath@redhat.com> 1.4.10-4
- Fixed check_log plugin #395601

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.4.10-2
- Rebuild for deps

* Thu Dec 06 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.10-1
- Upstream released new version
- Removed some patches

* Fri Oct 26 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.8-9
- Fix for Bug 348731 and CVE-2007-5623

* Wed Aug 22 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.8-7
- Rebuild for BuildID
- License change

* Fri Aug 10 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.8-6
- Fix for check_linux_raid - #234416
- Fix for check_ide_disk - #251635

* Tue Aug 07 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.8-2
- Fix for check_smtp - #251049

* Fri Apr 13 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.8-1
- Upstream released new version

* Fri Feb 23 2007 Mike McGrath <mmcgrath@redhat.com> 1.4.6-1
- Upstream released new version

* Sun Dec 17 2006 Mike McGrath <imlinux@gmail.com> 1.4.5-1
- Upstream released new version

* Fri Oct 27 2006 Mike McGrath <imlinux@gmail.com> 1.4.4-2
- Enabled check_smart_ide
- Added patch for linux_raid
- Fixed permissions on check_icmp

* Tue Oct 24 2006 Mike McGrath <imlinux@gmail.com> 1.4.4-1
- Upstream new version
- Disabled check_ide_smart (does not compile cleanly/too lazy to fix right now)
- Added check_apt

* Sun Aug 27 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-18
- Removed utils.pm from the base nagios-plugins package into its own package

* Tue Aug 15 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-17
- Added requires qstat for check_game

* Thu Aug 03 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-16
- Providing path to qstat

* Thu Aug 03 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-15
- Fixed permissions on check_dhcp
- Added check_game
- Added check_radius
- Added patch for ntp

* Sun Jul 23 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-14
- Patched upstream issue: 196356

* Sun Jul 23 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-13
- nagios-plugins-all now includes nagios-plugins-mysql

* Thu Jun 22 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-12
- removed sensors support for sparc and sparc64

* Thu Jun 22 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-11
- Created a README.Fedora explaining how to install other plugins

* Sun Jun 11 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-9
- Removed check_sensors in install section

* Sat Jun 10 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-8
- Inserted conditional blocks for ppc exception.

* Wed Jun 07 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-7
- Removed sensors from all plugins and added excludearch: ppc

* Tue Jun 06 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-6
- For ntp plugins requires s/ntpc/ntpdc/

* Sun Jun 03 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-5
- Fixed a few syntax errors and removed an empty export

* Sat May 19 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-4
- Now using configure macro instead of ./configure
- Added BuildRequest: perl(Net::SNMP)
- For reference, this was bugzilla.redhat.com ticket# 176374

* Sat May 19 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-3
- Added check_ide_smart
- Added some dependencies
- Added support for check_if* (perl-Net-SNMP now in extras)
- nagios-plugins now owns dir %%{_libdir}/nagios

* Sat May 13 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-2
- Added a number of requires that don't get auto-detected

* Sun May 07 2006 Mike McGrath <imlinux@gmail.com> 1.4.3-1
- Upstream remeased 1.4.3

* Tue Apr 18 2006 Mike McGrath <imlinux@gmail.com> 1.4.2-9
- Fixed a typo where nagios-plugins-all required nagios-plugins-httpd

* Mon Mar 27 2006 Mike McGrath <imlinux@gmail.com> 1.4.2-8
- Updated to CVS head for better MySQL support

* Sun Mar 5 2006 Mike McGrath <imlinux@gmail.com> 1.4.2-7
- Added a nagios-plugins-all package

* Wed Feb 1 2006 Mike McGrath <imlinux@gmail.com> 1.4.2-6
- Added provides for check_tcp

* Mon Jan 30 2006 Mike McGrath <imlinux@gmail.com> 1.4.2-5
- Created individual packages for all check_* scripts

* Tue Dec 20 2005 Mike McGrath <imlinux@gmail.com> 1.4.2-4
- Fedora friendly spec file

* Mon May 23 2005 Sean Finney <seanius@seanius.net> - cvs head
- just include the nagios plugins directory, which will automatically include
  all generated plugins (which keeps the build from failing on systems that
  don't have all build-dependencies for every plugin)

* Tue Mar 04 2004 Karl DeBisschop <karl[AT]debisschop.net> - 1.4.0alpha1
- extensive rewrite to facilitate processing into various distro-compatible specs

* Tue Mar 04 2004 Karl DeBisschop <karl[AT]debisschop.net> - 1.4.0alpha1
- extensive rewrite to facilitate processing into various distro-compatible specs

