Name:           hello
Version:        1.0.0 
Release:        1%{?dist}
Summary:        GaiaX RPM Hacks test code
Group:          Gaiax Test
License:        GPL License
URL:            https://github.com/jojoagogogo/
Source0:        %{name}-%{version}.tar.gz
Patch0:         %{name}.patch0
#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Vendor:         "GaiaX co.,ltd."

BuildRequires: autoconf automake
Requires:      glibc

Prefix: /usr/local/bin

%description
hello sample spec :)

%prep
%setup -q
%patch0 -p0


%build
rm -rf $RPM_BUILD_ROOT
%if %{with configure}
%configure
%endif
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}
#make install DESTDIR=$RPM_BUILD_ROOT
make install DEST=$RPM_BUILD_ROOT%{prefix}


%clean
#rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{prefix}/hello


%changelog
