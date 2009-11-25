%define bootstrap 0

# Allow --with[out] bootstrap at rpm command line build
%{?_without_bootstrap: %{expand: %%define bootstrap 0}}
%{?_with_bootstrap: %{expand: %%define bootstrap 1}}

Name: xinit
Version: 1.2.0
Release: %mkrel 3
Summary: Initialize an X session
Group: System/X11
Source0: http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
# (fc) 1.1.0-4mdv allow to init CK easily (Fedora)
Source1: ck-xinit-session.c
# (fc) 1.0.2-2mdv readd modifications for startx (argument parsing)
Patch0: xinit-1.2.0-startx-arguments.patch
# (fc) 1.0.4-2mdv add ConsoleKit support (Fedora)
Patch1: xinit-1.1.0-poke-ck.patch
# (fc) prevent freeze from applications trying to read stdin (Fedora bug #214649)
Patch2: xinit-1.0.4-client-session.patch
# (fc) unset XDG_SESSION_COOKIE in startx (Fedora bug #489999)
Patch3: xinit-1.0.9-unset.patch
# (pz) this patch was taken from the old startx.patch
Patch4: xinit-1.2.0-replace-xterm-for-xvt.patch

License: MIT
BuildRoot: %{_tmppath}/%{name}-root
Requires: xinitrc

BuildRequires: libx11-devel >= 1.0.0
BuildRequires: x11-util-macros >= 1.0.1
%if !%{bootstrap}
BuildRequires: consolekit-devel
BuildRequires: dbus-devel
Requires: consolekit-x11
Requires: which
%endif

%description
The xinit program is used to start the X Window System server and a first
client program on systems that cannot start X directly from /etc/init or in
environments that use multiple window systems. When this first client exits,
xinit will kill the X server and then terminate.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .startx

#if !%{bootstrap}
#patch1 -p1 -b .poke-ck
#endif
%patch2 -p1 -b .client-session
%patch3 -p1 -b .unset
%patch4 -p1 -b .xvt

#needed by patch1
#if !%{bootstrap}
#autoreconf -fi
#endif

%build
%configure2_5x
%make XINITDIR=/etc/X11/xinit

%if !%{bootstrap}
%{__cc} -o ck-xinit-session \
	`pkg-config --cflags ck-connector dbus-1` $RPM_OPT_FLAGS \
	$RPM_SOURCE_DIR/ck-xinit-session.c \
	`pkg-config --libs ck-connector dbus-1`
%endif


%install
rm -rf %{buildroot}
%makeinstall_std
%if !%{bootstrap}
install -m755 ck-xinit-session $RPM_BUILD_ROOT/%{_bindir}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/xinit
%{_bindir}/startx
%if !%{bootstrap}
%{_bindir}/ck-xinit-session
%endif
%{_libdir}/X11/xinit
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*
#don't use xorg xinitrc file, use our own, provided by xinitrc package
%exclude %{_libdir}/X11/xinit
