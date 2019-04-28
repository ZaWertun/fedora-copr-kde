%global         base_name oxygen

Name:    plasma-%{base_name}
Version: 5.15.4
Release: 1%{?dist}
Summary: Plasma and Qt widget style and window decorations for Plasma 5 and KDE 4

License: GPLv2+
URL:     https://cgit.kde.org/%{base_name}.git

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

# filter plugins
%global __provides_exclude_from ^(%{_kde4_libdir}/kde4/.*\\.so|%{_kf5_qtplugindir}/.*\\.so)$

BuildRequires:  libxcb-devel

# Qt 5
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

# KF5
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcmutils-devel

%if 0%{?fedora}
%global qt4 1
BuildRequires:  kdecoration-devel
BuildRequires:  kf5-kwayland-devel
%endif

Requires:       kf5-filesystem

Requires:       qt4-style-oxygen = %{version}-%{release}
Requires:       qt5-style-oxygen = %{version}-%{release}
Requires:       oxygen-cursor-themes = %{version}-%{release}
Requires:       oxygen-sound-theme = %{version}-%{release}
# for oxygen look-and-feel
Requires:       oxygen-icon-theme

# kwin-oxygen was removed in 5.1.95
Obsoletes:	kwin-oxygen < 5.1.95-1

%description
%{summary}.

%if 0%{?qt4}
%package -n     qt4-style-oxygen
Summary:        Oxygen widget style for Qt 4
# Qt 4 dependencies
BuildRequires:  kdelibs4-devel
Provides:       kde-style-oxygen%{?_isa} = %{version}-%{release}
# When this was created
Obsoletes:      kde-style-oxygen < 5.1.1-2
Obsoletes:      plasma-oxygen-kde4 < 5.1.1-2
%description -n qt4-style-oxygen
%{summary}.
%endif

%package -n     qt5-style-oxygen
Summary:        Oxygen widget style for Qt 5
Obsoletes:      plasma-oxygen < 5.1.1-2
%description -n qt5-style-oxygen
%{summary}.

%package -n     oxygen-cursor-themes
Summary:        Oxygen cursor themes
BuildArch:      noarch
Obsoletes:      plasma-oxygen-common < 5.1.1-2
%description -n oxygen-cursor-themes
%{summary}.

%package -n     oxygen-sound-theme
Summary:        Sounds for Oxygen theme
BuildArch:      noarch
Obsoletes:      plasma-oxygen-common < 5.1.1-2
%description -n oxygen-sound-theme
%{summary}.


%prep
%autosetup -n %{base_name}-%{version} -p1

%if ! 0%{?fedora}
sed -i.optional \
  -e 's| add_subdirectory(cursors)|#add_subdirectory(cursors)|' \
  -e 's| add_subdirectory(kdecoration)|#add_subdirectory(kdecoration)|' \
  CMakeLists.txt
%endif


%build
%if 0%{?qt4}
# Build for Qt 4
%global qt4_target_platform %{_target_platform}-qt4
mkdir %{qt4_target_platform}
pushd %{qt4_target_platform}
%{cmake_kde4} .. -DOXYGEN_USE_KDE4:BOOL=ON
popd

make %{?_smp_mflags} -C %{qt4_target_platform}
%endif

# Build for Qt 5
%global qt5_target_platform %{_target_platform}-qt5
mkdir %{qt5_target_platform}
pushd %{qt5_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{qt5_target_platform}

%install
%if 0%{?qt4}
make install/fast DESTDIR=%{buildroot} -C %{qt4_target_platform}
%endif
make install/fast DESTDIR=%{buildroot} -C %{qt5_target_platform}


## unpackaged files
# Don't bother with -devel subpackages, there are no headers anyway
rm -fv %{buildroot}%{_libdir}/liboxygenstyle5.so
rm -fv %{buildroot}%{_libdir}/liboxygenstyleconfig5.so
rm -fv %{buildroot}%{_kde4_libdir}/liboxygenstyle.so
rm -fv %{buildroot}%{_kde4_libdir}/liboxygenstyleconfig.so
%if ! 0%{?fedora}
rm -fv %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/oxygen_kdecoration.mo
#rm -fv %{buildroot}%{_datadir}/sounds/Oxygen-*
rm -rfv %{buildroot}%{_datadir}/icons/{KDE_Classic,Oxygen_*}
rm -fv %{buildroot}%{_kf5_qtplugindir}/org.kde.kdecoration2/oxygendecoration.so
rm -fv %{buildroot}%{_kf5_datadir}/kservices5/oxygendecorationconfig.desktop
rm -rfv %{buildroot}%{_kf5_datadir}/plasma/look-and-feel/org.kde.oxygen/
%endif

%find_lang oxygen --with-qt --all-name


%if 0%{?fedora}
%files
%{_kf5_datadir}/plasma/look-and-feel/org.kde.oxygen/
%endif

%if 0%{?qt4}
%post -n    qt4-style-oxygen -p /sbin/ldconfig
%postun -n  qt4-style-oxygen -p /sbin/ldconfig

%files -n   qt4-style-oxygen
%{_kde4_libdir}/liboxygenstyle.so.*
%{_kde4_libdir}/liboxygenstyleconfig.so.*
%{_kde4_libdir}/kde4/kstyle_oxygen_config.so
%{_kde4_libdir}/kde4/plugins/styles/oxygen.so
%{_kde4_appsdir}/kstyle/themes/oxygen.themerc
%{_kde4_bindir}/oxygen-demo
%endif

%post -n qt5-style-oxygen
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qt5-style-oxygen
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qt5-style-oxygen
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -n   qt5-style-oxygen -f oxygen.lang
%{_bindir}/oxygen-demo5
%{_bindir}/oxygen-settings5
%{_libdir}/liboxygenstyle5.so.*
%{_libdir}/liboxygenstyleconfig5.so.*
%{_kf5_qtplugindir}/styles/oxygen.so
%{_kf5_qtplugindir}/kstyle_oxygen_config.so
%if 0%{?fedora}
%{_kf5_qtplugindir}/org.kde.kdecoration2/oxygendecoration.so
%{_kf5_datadir}/kservices5/oxygendecorationconfig.desktop
%endif
%{_kf5_datadir}/kservices5/oxygenstyleconfig.desktop
%{_kf5_datadir}/kstyle/themes/oxygen.themerc
%{_kf5_datadir}/icons/hicolor/*/apps/oxygen-settings.*

%if 0%{?fedora}
%files -n   oxygen-cursor-themes
%{_datadir}/icons/KDE_Classic/
%{_datadir}/icons/Oxygen_Black/
%{_datadir}/icons/Oxygen_Blue/
%{_datadir}/icons/Oxygen_White/
%{_datadir}/icons/Oxygen_Yellow/
%{_datadir}/icons/Oxygen_Zion/
%endif

%files -n   oxygen-sound-theme
%{_datadir}/sounds/Oxygen-*


%changelog
* Sun Apr 28 2019 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.15.4-1
- 5.15.4

* Tue Feb 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.14.5-1
- 5.14.5

* Tue Nov 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-1
- 5.14.4

* Thu Nov 08 2018 Martin Kyral <martin.kyral@gmail.com> - 5.14.3-1
- 5.14.3

* Wed Oct 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Tue Oct 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.1-1
- 5.14.1

* Tue Oct 09 2018 Rex Dieter <rdieter@fedoraproject.org> 5.14.0-2
- provide oxygen-sound-theme on epel7 (#1637460)

* Sat Oct 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-1
- 5.14.0

* Fri Sep 14 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.90-1
- 5.13.90

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.5-1
- 5.13.5

* Thu Aug 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.4-1
- 5.13.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.3-1
- 5.13.3

* Mon Jul 09 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.2-1
- 5.13.2

* Tue Jun 19 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1-1
- 5.13.1

* Sat Jun 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-1
- 5.13.0

* Fri May 18 2018 Martin Kyral <martin.kyral@gmail.com> - 5.12.90-1
- 5.12.90

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Tue Mar 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Wed Feb 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.2-1
- 5.12.2

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.1-1
- 5.12.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.0-1
- 5.12.0

* Mon Jan 15 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.95-1
- 5.11.95

* Tue Jan 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.5-1
- 5.11.5

* Thu Nov 30 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.4-1
- 5.11.4

* Wed Nov 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Wed Oct 25 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.2-1
- 5.11.2

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Wed Oct 11 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.0-1
- 5.11.0

* Thu Aug 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-1
- 5.10.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.4-1
- 5.10.4

* Tue Jun 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-1
- 5.10.3

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-1
- 5.10.2

* Tue Jun 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Thu Mar 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-2
- rebuild

* Wed Mar 01 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Tue Feb 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-1
- 5.8.6

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org - 5.8.5-2
- filter plugin provides

* Wed Dec 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-1
- 5.8.5

* Tue Nov 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-1
- 5.8.4

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-1
- 5.8.3

* Tue Oct 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- 5.8.2

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- 5.8.1

* Mon Oct 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-2
- move look-and-feel to main pkg
- provide qt5-style-oxygen for epel (#1381197)
- BR: kf5-kwayland

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Thu Sep 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-1
- 5.7.95

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-1
- 5.7.5

* Tue Aug 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-1
- 5.7.4

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-1
- 5.7.3

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-1
- 5.7.2

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-1
- 5.7.1

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-1
- 5.7.0

* Sat Jun 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-1
- 5.6.95

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-1
- 5.6.5

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-1
- 5.6.4

* Wed Apr 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-2
- rebuild (qt)

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-1
- 5.6.3

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-3
- rebuild (qt)

* Sat Apr 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-1
- 5.6.2

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1
- 5.6.1

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Tue Jan 27 2015 Daniel Vrátil <dvratil2redhat.com> - 5.2.0-2
- fix Requires: kwin-devel (unversioned)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1
- Plasma 5.1.95 Beta
- removed kwin-oxygen subpackage, as Oxygen does not provide KDecoration1-based windecos as of 5.1.95

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Wed Nov 19 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.1.1-9
- Move kstyle_oxygen_config.so from kwin-oxygen to qt5-style-oxygen

* Wed Nov 19 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-8
- Remove Conflicts kde-style-oxygen from kwin-oxygen
- Remove Requires themes from qt{4,5}-style-oxygen
- Fixed scriptlets

* Thu Nov 13 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-7
- Fix Obsoletes issue when updating

* Wed Nov 12 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- change subpackages, merge with plasma-oxygen-kde4

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Does not conflict with kde-style-oxygen 4

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515git9651288
- Intial snapshot