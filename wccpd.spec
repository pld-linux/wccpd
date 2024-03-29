Summary:	A WCCP Server Daemon
Summary(pl.UTF-8):	Serwer WCCP
Name:		wccpd
Version:	0.2
Release:	4
License:	GPL v2
Group:		Daemons
Source0:	http://dl.sourceforge.net/wccpd/%{name}-%{version}.tar.gz
# Source0-md5:	5f15c274de61dfb88e0dbfc1ccbe6b67
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://wccpd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts >= 0.2.0
Requires:	/sbin/chkconfig
Requires:	bc
Requires:	fileutils
Requires:	iproute2
Requires:	ipvsadm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The WCCP (Web Cache Coordination Protocol) provides a method to
coordinate a farm of Web Caches from a central router. It allows
transparent redirection based on reachability.

%description -l pl.UTF-8
WCCP (Web Cache Coordination Protocol) dostarcza metodę do
koordynowania farm Web Cache'ów z centralnego routera. Pozwala to na
przezroczyste przekierowania oparte na osiągalności hosta w danym
momencie.

%prep
%setup -q

%build
rm -f missing support/missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_libdir}/wccpd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wccpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/wccpd
install contrib/linux-ipvs/scripts/*cache $RPM_BUILD_ROOT%{_libdir}/wccpd
install contrib/linux-ipvs/scripts/*wccp $RPM_BUILD_ROOT%{_libdir}/wccpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add wccpd
%service wccpd restart "wccpd daemon"

%preun
if [ "$1" = "0" ]; then
	%service wccpd stop
	/sbin/chkconfig --del wccpd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README INSTALL.Linux doc/*.txt doc/html/*
%attr(754,root,root) %{_sbindir}/*
%dir %{_libdir}/wccpd
%attr(754,root,root) %{_libdir}/wccpd/*cache
%attr(754,root,root) %{_libdir}/wccpd/*wccp
%attr(754,root,root) /etc/rc.d/init.d/wccpd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/wccpd
%{_mandir}/man8/*.8*
