Name:           hello
Version:        1.0.0 
Release:        1%{?dist}
Summary:        GaiaX RPM Hacks test code
Group:          Gaiax Test
License:        GPL License
URL:            https://github.com/jojoagogogo/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:         "GaiaX co.,ltd."

BuildRequires: glibc-devel  
Requires:      glibc

%description


%prep
%setup -q -n hello-1.0.0


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc



%changelog
