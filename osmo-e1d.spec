Name:           osmo-e1d
Version:        0.7.1
Release:        1.dcbw%{?dist}
Summary:        Osmocom e1 interface daemon and library
License:        GPL-2.0-or-later AND LGPL-3.0-or-later

URL:            https://osmocom.org/projects/osmo-e1d/wiki

BuildRequires:  git gcc autoconf automake libtool doxygen systemd-devel
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libusb1-devel libtalloc-devel

Source0: %{name}-%{version}.tar.bz2

Requires: osmo-usergroup

%description
osmo-e1d is an E1 interface daemon that is part of the Osmocom E1
interface driver architecture. It was primarily written for the
ICE40_E1_USB_interface (ICE40 based E1 framer IP core developed by
tnt).

osmo-e1d acts as an interface between the hardware/firmware of the E1
interface on the bottom side, and applications wanting to use E1
timeslots on the top side.

%package -n libosmo-e1d
Summary:        Osmocom E1 daemon protocol library

%description -n libosmo-e1d
Osmocom E1 Daemon Protocol Library.

%package -n libosmo-octoi
Summary:        Library for the Osmocom Community TDMoIP network

%description -n libosmo-octoi
Library for the Osmocom Community TDMoIP network.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%autosetup -p1

%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fi
%configure --enable-shared \
           --disable-static \
           --with-systemdsystemunitdir=%{_unitdir}

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
sed -i -e 's|UNKNOWN|%{version}|g' %{buildroot}/%{_libdir}/pkgconfig/*.pc


%check
make check


%ldconfig_scriptlets libosmo-e1d
%ldconfig_scriptlets libosmo-octoi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%files
%license COPYING COPYING.gpl2 COPYING.lgpl3
%doc README.md
%{_bindir}/osmo-e1d
%{_bindir}/osmo-e1d-pipe
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%{_unitdir}/%{name}.service
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_sysconfdir}/osmocom/%{name}.cfg

%files -n libosmo-e1d
%{_libdir}/libosmo-e1d.so.*

%files -n libosmo-octoi
%{_libdir}/libosmo-octoi.so.*

%files devel
%{_includedir}/osmocom/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.6.0
- Update to 1.6.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- github update releases
