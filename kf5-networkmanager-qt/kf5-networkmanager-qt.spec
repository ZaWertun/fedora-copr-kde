%global framework networkmanager-qt

Name:    kf5-%{framework}
Version: 5.60.0
Release: 1%{?dist}
Summary: A Tier 1 KDE Frameworks 5 module that wraps NetworkManager DBus API

License: LGPLv2+
URL:     https://cgit.kde.org/%{framework}.git

%global majmin %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/frameworks/%{majmin}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules >= %{majmin}
BuildRequires:  kf5-rpm-macros >= %{majmin}
BuildRequires:  qt5-qtbase-devel

BuildRequires:  pkgconfig(libnm)

%if 0%{?fedora} > 22
Recommends:     NetworkManager
%else
Requires:       NetworkManager >= 0.9.9.0
%endif
Requires:       kf5-filesystem >= %{majmin}

%description
A Tier 1 KDE Frameworks 5 Qt library for NetworkManager.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
Requires:       pkgconfig(libnm)
%description    devel
Qt libraries and header files for developing applications
that use NetworkManager.


%prep
%autosetup -p1 -n %{framework}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

%make_build -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}


%ldconfig_scriptlets

%files
%doc README.md
%license COPYING.LIB
%{_kf5_libdir}/libKF5NetworkManagerQt.so.*
%{_kf5_datadir}/qlogging-categories5/networkmanager-qt.categories

%files devel
%{_kf5_libdir}/libKF5NetworkManagerQt.so
%{_kf5_libdir}/cmake/KF5NetworkManagerQt/
%{_kf5_includedir}/NetworkManagerQt/
%{_kf5_includedir}/networkmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_NetworkManagerQt.pri


%changelog
* Sat Jul 13 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.60.0-1
- 5.60.0

* Sat Jun 08 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.59.0-1
- 5.59.0

* Tue May 14 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.58.0-1
- 5.58.0

* Sun Apr 28 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.57.0-1
- 5.57.0

* Mon Feb 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.55.0-1
- 5.55.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.54.0-1
- 5.54.0

* Sun Dec 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.53.0-1
- 5.53.0

* Sun Nov 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.52.0-1
- 5.52.0

* Wed Oct 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.51.0-1
- 5.51.0

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.50.0-1
- 5.50.0

* Tue Aug 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.49.0-1
- 5.49.0

* Sun Jul 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-3
- .spec cosmetics

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-1
- 5.48.0

* Thu Jun 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-2
- cleanup, use %%majmin more

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-1
- 5.47.0

* Sat May 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.0-1
- 5.46.0

* Sun Apr 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.45.0-1
- 5.45.0

* Sat Mar 03 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.44.0-1
- 5.44.0

* Wed Feb 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.43.0-1
- 5.43.0

* Mon Jan 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.42.0-1
- 5.42.0

* Mon Dec 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.41.0-1
- 5.41.0

* Fri Nov 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.40.0-1
- 5.40.0

* Sun Oct 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.39.0-1
- 5.39.0

* Mon Sep 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.38.0-1
- 5.38.0

* Fri Aug 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.37.0-1
- 5.37.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.36.0-1
- 5.36.0

* Sun Jun 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.35.0-1
- 5.35.0

* Mon May 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.34.0-1
- 5.34.0

* Wed Apr 12 2017 Jan Grulich <jgrulich@redhat.com> - 5.33.0-2
- Set auto-negotiation based on NM version

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.33.0-1
- 5.33.0

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.32.0-1
- 5.32.0

* Mon Feb 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.31.0-1
- 5.31.0

* Fri Dec 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.29.0-1
- 5.29.0

* Fri Dec 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.29.0-1
- 5.29.0

* Mon Oct 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Wed Sep 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.26.0-1
- KDE Frameworks 5.26.0

* Mon Aug 08 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.25.0-1
- KDE Frameworks 5.25.0

* Wed Jul 06 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.24.0-1
- KDE Frameworks 5.24.0

* Wed Jun 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.23.0-3
- Recommends: NetworkManager (#1350973)

* Tue Jun 28 2016 Jan Grulich <jgrulich@redhat.com> - 5.23.0-2
- Do not set peap label based on peap version

* Tue Jun 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.23.0-1
- KDE Frameworks 5.23.0

* Tue Jun 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-2
- update URL, use autosetup, group Group: tags

* Mon May 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-1
- KDE Frameworks 5.22.0

* Mon Apr 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-1
- KDE Frameworks 5.21.0

* Mon Mar 14 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.20.0-1
- KDE Frameworks 5.20.0

* Thu Feb 11 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.19.0-1
- KDE Frameworks 5.19.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-3
- cosmetics, update URL, use %%license

* Tue Jan 05 2016 Jan Grulich <jgrulich@redhat.com> - 5.18.0-2
- Re-check connection state before we watch changes in case it gets changed too quickly
  kdebz:#352326

* Sun Jan 03 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.18.0-1
- KDE Frameworks 5.18.0

* Tue Dec 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.17.0-1
- KDE Frameworks 5.17.0

* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.16.0-1
- KDE Frameworks 5.16.0

* Thu Oct 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.15.0-1
- KDE Frameworks 5.15.0

* Wed Sep 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.14.0-1
- KDE Frameworks 5.14.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Fri Jul 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- KDE Frameworks 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-2
- F22+: Obsoletes/Provides libnm-qt

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Thu Apr 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-2
- -devel Requires NetworkManager

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Wed Feb 18 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Fix BR on Fedora > 21 (with NM 1.0)

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 15 2015 Jan Grulich <jgrulich@redhat.com> - 5.6.0-2
- Add generic setting
  Add minor vpn fixes

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.93-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.91-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-3.20140611gitef654fd
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-2.20140514git107e27d
- Update to latest git snapshot

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-1.20140418git2afe13e
- Upgrade libnm-qt to a Tier 2 KDE Frameworks module kf5-networkmanagerqt

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1:0.9.9.1-1.20140403git2afe13e
- Qt 5 fork of libnm-qt
