Summary:	A WCCP Server Daemon
Summary(pl):	Serwer WCCP
Name:		wccpd
Version:	0.2
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/wccpd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://wccpd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Prereq:		fileutils
Requires:	bc
Requires:	iproute2
Requires:	ipvsadm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The WCCP (Web Cache Coordination Protocol) provides a method to
coordinate a farm of Web Caches from a central router. It allows
transparent redirection based on reachability.

%description -l pl
WCCP (Web Cache Coordination Protocol) dostarcza metodê do
koordynowania farm Web Cache'ów z centralnego routera. Pozwala to na
przezroczyste przekierowania oparte na osi±galno¶ci hosta w danym
momencie.

%prep
%setup -q

%build
rm -f missing support/missing
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_libdir}/wccpd

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wccpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/wccpd
install contrib/linux-ipvs/scripts/*cache $RPM_BUILD_ROOT%{_libdir}/wccpd/
install contrib/linux-ipvs/scripts/*wccp $RPM_BUILD_ROOT%{_libdir}/wccpd/

gzip -9nf AUTHORS ChangeLog NEWS README doc/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add wccpd
if [ -f /var/lock/subsys/wccpd ]; then
	/etc/rc.d/init.d/wccpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/wccpd start\" to start wccpd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/wccpd ]; then
		/etc/rc.d/init.d/wccpd stop 1>&2
	fi
	/sbin/chkconfig --del wccpd
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz doc/html/*
%attr(754,root,root) %{_sbindir}/*
%dir %{_libdir}/wccpd/
%attr(754,root,root) %{_libdir}/wccpd/*cache
%attr(754,root,root) %{_libdir}/wccpd/*wccp
%attr(754,root,root) /etc/rc.d/init.d/wccpd
%attr(644,root,root) %config(noreplace) /etc/sysconfig/wccpd
%attr(644,root,root) %{_mandir}/man8/*.8*
