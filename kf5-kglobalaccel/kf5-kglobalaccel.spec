%global framework kglobalaccel

Name:    kf5-%{framework}
Version: 5.57.0
Release: 1%{?dist}
Summary: KDE Frameworks 5 Tier 3 integration module for global shortcuts

License: LGPLv2+
URL:     https://cgit.kde.org/%{framework}.git

%global majmin %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{majmin}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules >= %{majmin}
BuildRequires:  kf5-rpm-macros
BuildRequires:  kf5-kconfig-devel >= %{majmin}
BuildRequires:  kf5-kcoreaddons-devel >= %{majmin}
BuildRequires:  kf5-kcrash-devel >= %{majmin}
BuildRequires:  kf5-kdbusaddons-devel >= %{majmin}
BuildRequires:  kf5-ki18n-devel >= %{majmin}
BuildRequires:  kf5-kservice-devel >= %{majmin}
BuildRequires:  kf5-kwindowsystem-devel >= %{majmin}

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel


Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Conflicts: plasma-workspace < 5.2.0-8

%description
%{summary}.

%package        libs
Summary:        Runtime libraries for %{name}
Requires:       %{name} = %{version}-%{release}
%description    libs
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{framework}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

%make_build -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang_kf5 kglobalaccel5_qt


%files -f kglobalaccel5_qt.lang
%doc README.md
%license COPYING.LIB
%{_kf5_sysconfdir}/xdg/%{framework}*
%{_kf5_bindir}/kglobalaccel5
%{_kf5_datadir}/kservices5/kglobalaccel5.desktop
%{_datadir}/dbus-1/services/org.kde.kglobalaccel.service

%ldconfig_scriptlets libs

%files libs
%{_kf5_libdir}/libKF5GlobalAccel.so.*
%{_kf5_libdir}/libKF5GlobalAccelPrivate.so.*
%{_kf5_qtplugindir}/org.kde.kglobalaccel5.platforms/

%files devel
%{_kf5_includedir}/kglobalaccel_version.h
%{_kf5_includedir}/KGlobalAccel/
%{_kf5_libdir}/libKF5GlobalAccel.so
%{_kf5_libdir}/cmake/KF5GlobalAccel/
%{_kf5_archdatadir}/mkspecs/modules/qt_KGlobalAccel.pri
%{_kf5_datadir}/dbus-1/interfaces/*


%changelog
* Sat Apr 27 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.57.0-1
- 5.57.0

* Mon Feb 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.55.0-1
- 5.55.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.54.0-1
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

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-1
- 5.48.0

* Fri Jun 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-3
- -devel: drop extraneous cmake(Qt5...) deps

* Thu Jun 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-2
- cleanup, use %%make_build %%ldconfig_scriptlets

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

* Thu Sep 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.38.1-1
- 5.38.1, fix %%description (sync w/summary), cosmetics

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

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.33.0-1
- 5.33.0

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.32.0-1
- 5.32.0

* Mon Feb 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.31.0-1
- 5.31.0

* Fri Dec 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.29.0-1
- 5.29.0

* Tue Oct 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Wed Sep 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.26.0-1
- KDE Frameworks 5.26.0

* Mon Aug 08 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.25.0-1
- KDE Frameworks 5.25.0

* Wed Jul 06 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.24.0-1
- KDE Frameworks 5.24.0

* Tue Jun 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.23.0-1
- KDE Frameworks 5.23.0

* Tue Jun 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-2
- update URL, use autosetup

* Mon May 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-1
- KDE Frameworks 5.22.0

* Mon Apr 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-1
- KDE Frameworks 5.21.0

* Mon Mar 14 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.20.0-1
- KDE Frameworks 5.20.0

* Thu Feb 11 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.19.0-1
- KDE Frameworks 5.19.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-2
- cosmetics, update URL, use %%license, move plugins to -libs

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

* Thu Jul 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Wed Apr 22 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- backport logging fix (kde#346429)
- -libs: add dep on main pkg
- bump minimal build deps

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Fri Feb 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.7.0-2
- Conflicts: plasma-workspace < 5.2.0-8

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Mon Dec 08 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- KDE Frameworks 5.4.0

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Thu Sep 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.100.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Tue May 06 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-2
- Rebuild against updated kf5-rpm-macros

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
