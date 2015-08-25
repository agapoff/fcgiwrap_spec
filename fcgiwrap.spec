Name:		fcgiwrap
Version:	1.1.0
Release:	4%{?dist}
Summary:	Simple FastCGI wrapper for CGI scripts
Group:		System Environment/Daemons
License:	BSD-like
URL:		http://nginx.localdomain.pl/wiki/FcgiWrap
Source0:	%{name}-%{version}.tgz
BuildRequires:	autoconf automake fcgi-devel pkgconfig systemd-devel
Requires:	fcgi


%description
This package provides a simple FastCGI wrapper for CGI scripts with/
following features:
 - very lightweight (84KB of private memory per instance)
 - fixes broken CR/LF in headers
 - handles environment in a sane way (CGI scripts get HTTP-related env.
   vars from FastCGI parameters and inherit all the others from
   environment of fcgiwrap )
 - no configuration, so you can run several sites off the same
   fcgiwrap pool
 - passes CGI stderr output to stderr stream of cgiwrap or FastCGI
 - support systemd socket activation, launcher program like spawn-fcgi
   is no longer required on systemd-enabled distributions


%prep
%setup -q


%build
autoreconf -i
%configure --prefix=/
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if 0%{?el7:1}
  %{__mkdir} -p %{buildroot}%{_unitdir}
  cp %{_builddir}/%{name}-%{version}/systemd/fcgiwrap.service %{buildroot}%{_unitdir}
  cp %{_builddir}/%{name}-%{version}/systemd/fcgiwrap.socket %{buildroot}%{_unitdir}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/fcgiwrap
#TODO: figure out why the manpage file is compressed automatically
%doc %{_mandir}/man8/fcgiwrap.8.gz
%if 0%{?el7:1}
    %{_unitdir}/fcgiwrap.service
    %{_unitdir}/fcgiwrap.socket
%endif


%post
# enable socket activation for fcgiwrap
%if 0%{?el7:1}
if [ $1 -eq 2 ]; then
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
/usr/bin/systemctl enable fcgiwrap.socket
/usr/bin/systemctl start fcgiwrap.socket

cat <<BANNER
==================================================
FCGI service fcgiwrap is ready!!!
==================================================
BANNER
%endif


%preun
# stop and disable socket activation for fcgiwrap
%if 0%{?el7:1}
    /usr/bin/systemctl stop fcgiwrap.socket
    /usr/bin/systemctl disable fcgiwrap.socket
%endif


%changelog
* Mon Aug 25 2015 Vitaly Agapov <v.agapov@quotix.com> - 1.1.0-4
- Added BuildRequires systemd-devel

* Mon Aug 24 2015 Vitaly Agapov <v.agapov@quotix.com> - 1.1.0-3
- Install unit-files for CentOS7

* Mon Jun 22 2015 Vitaly Agapov <v.agapov@quotix.com> - 1.1.0-2
- Prepare spec for Quotix usage

* Tue Apr 22 2014 Justin Zhang <schnell18[AT]gmail.com> - 1.1.0-1
- version 1.1.0
- Create RPM spec file for the fcgiwrap
