Name:    layer-shell-qt
Version: 5.22.3
Release: 1%{?dist}
Summary: Library to easily use clients based on wlr-layer-shell

License: LGPLv3+
URL:     https://invent.kde.org/plasma/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires: extra-cmake-modules >= 5.82

BuildRequires: qt5-qtbase-devel
# needs /usr/lib64/libQt5XkbCommonSupport.a
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtbase-static

BuildRequires: cmake(Qt5WaylandClient)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5XkbCommonSupport)

BuildRequires: libxkbcommon-devel
BuildRequires: plasma-wayland-protocols-devel
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel

%description
This component is meant for applications to be able to easily use clients
based on wlr-layer-shell

%package devel
Summary:  Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake(Qt5Gui) >= 5.15.0
%description devel
%{summary}.


%prep
%autosetup


%build
%cmake_kf5

%cmake_build


%install
%cmake_install


%files
%license LICENSES/*
%{_libdir}/libLayerShellQtInterface.so.5*
%{_qt5_plugindir}/wayland-shell-integration/

%files devel
%{_includedir}/LayerShellQt/
%{_libdir}/libLayerShellQtInterface.so
%{_libdir}/cmake/LayerShellQt/


%changelog
* Thu Jul 08 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.22.3-1
- 5.22.3

* Wed Jun 23 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.22.2-1
- 5.22.2

* Tue Jun 15 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.22.1-1
- 5.22.1

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Fri May 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-2
- shorten summary

* Thu May 13 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-1
- first try

