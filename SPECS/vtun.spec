Name: vtun
Version: 3.0.1
Release: 7%{?dist}
Summary: Virtual tunnel over TCP/IP networks
License: GPLv2+
Group: System Environment/Daemons
Url: http://vtun.sourceforge.net
Source0: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: vtund.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: xinetd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service 
BuildRequires: zlib-devel lzo-devel openssl-devel bison flex

%description
VTun provides a method for creating Virtual Tunnels over TCP/IP networks
and allows one to shape, compress, and encrypt traffic in those tunnels.
Supported types of tunnels are: PPP, IP, Ethernet and most other serial
protocols and programs.
VTun is easily and highly configurable: it can be used for various
network tasks like VPN, Mobile IP, Shaped Internet access, IP address
saving, etc. It is completely a user space implementation and does not
require modification to any kernel parts.

%prep
%setup -q

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -D -m 0755 -p %{SOURCE1} %{buildroot}/%{_initrddir}/vtund
%{__install} -D -m 0644 -p scripts/vtund.xinetd %{buildroot}/%{_sysconfdir}/xinetd.d/vtun
%{__sed} -i 's:/usr/local:%{_prefix}:' %{buildroot}/%{_sysconfdir}/xinetd.d/vtun
%{__make} install DESTDIR=%{buildroot} INSTALL_OWNER= INSTALL="/usr/bin/install -p"

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add vtund || :
fi

%preun
if [ $1 -eq 0 ]; then
	/sbin/service vtund stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del vtund || :
fi

%postun
if [ $1 -eq 1 ]; then
	/sbin/service vtund condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc ChangeLog Credits FAQ README README.LZO README.Setup README.Shaper TODO vtund.conf
%config(noreplace) %{_sysconfdir}/vtund.conf
%config(noreplace) %{_sysconfdir}/xinetd.d/vtun
%{_initrddir}/vtund
%{_sbindir}/vtund
%dir %{_localstatedir}/log/vtund
%dir %{_localstatedir}/lock/vtund
%{_mandir}/man5/vtund.conf.5*
%{_mandir}/man8/vtun.8*
%{_mandir}/man8/vtund.8*

%changelog
* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.0.1-7
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 3.0.1-4
- rebuild with new openssl

* Mon Nov 17 2008 Gabriel Somlo <somlo at cmu.edu> 3.0.1-3
- scriptlets fixes
* Fri Nov 14 2008 Gabriel Somlo <somlo at cmu.edu> 3.0.1-2
- spec file fixes: defattr, -p flag to install program
* Mon Oct 20 2008 Gabriel Somlo <somlo at cmu.edu> 3.0.1-1
- initial fedora package
