%bcond_with	 bootstrap

Name:		xinit
Version:	1.3.3
Release:	5
Summary:	Initialize an X session
License:	MIT
Group:		System/X11
URL:		http://cgit.freedesktop.org/xorg/app/xinit
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2

# (fc) 1.1.0-4mdv allow to init CK easily (Fedora)
Source1:	ck-xinit-session.c

# (fc) 1.0.2-2mdv readd modifications for startx (argument parsing)
# This patch is part of the old "startx" patch.
# We need to check why exactly this patch is needed, but it does these things:
# - it removes the default client and server from the startx arguments, so if
#   nothing is specified the default server or client will be the one chosen by
#   xinit
# - it uses trap to make sure the "cleanup" function will be run
# - it partially undoes upstream commit 9632367abd03108f3636b05e9f2fd92f5c28dabe
# - it enables commands like "startx startxfce4", which don't work in the
#   unpatched version (should be "startx /usr/bin/startxfce4")
#Previous versions of this patch had a bug where xinit would be run twice if some
#macros were defined.
Patch0:		xinit-1.3.2-startx-arguments.patch

# (fc) 1.0.4-2mdv add ConsoleKit support (Fedora)
Patch1:		xinit-1.1.0-poke-ck.patch

# (fc) prevent freeze from applications trying to read stdin (Fedora bug #214649)
Patch2:		xinit-1.0.4-client-session.patch

# (fc) unset XDG_SESSION_COOKIE in startx (Fedora bug #489999)
Patch3:		xinit-1.0.9-unset.patch

# (pz) this patch was taken from the old startx.patch
Patch4:		xinit-1.2.0-replace-xterm-for-xvt.patch

# (cg) use the current vt to maintain the current session status.
Patch5:		xinit-1.3.2-use-current-vt.patch

BuildRequires:	pkgconfig(x11) >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
Requires:	xinitrc
Requires:	xauth

%if !%{with bootstrap}
# (tpg) systemd's login tool has replaced this
%if %mdvver < 201300
BuildRequires:	consolekit-devel
Requires:	consolekit-x11
%else
Requires:	systemd
%endif

BuildRequires:	dbus-devel
Requires:	which
%endif

%description
The xinit program is used to start the X Window System server and a first
client program on systems that cannot start X directly from /etc/init or in
environments that use multiple window systems. When this first client exits,
xinit will kill the X server and then terminate.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .orig

#if !% {with bootstrap}
#patch1 -p1 -b .poke-ck
#endif
%patch2 -p1 -b .client-session
%patch3 -p1 -b .unset
%patch4 -p1 -b .xvt
%patch5 -p1 -b .curvt

#needed by patch1
#if !% {with bootstrap}
#autoreconf -fi
#endif

%build
autoreconf -fi
%configure2_5x
%make XINITDIR=/etc/X11/xinit


%if !%{with bootstrap}
%if %mdvver < 201300
%{__cc} -o ck-xinit-session %ldflags \
        `pkg-config --cflags ck-connector dbus-1` $RPM_OPT_FLAGS \
         %{SOURCE1} \
         `pkg-config --libs ck-connector dbus-1`
%endif
%endif


%install
%makeinstall_std
%if !%{with bootstrap}
%if %mdvver < 201300
install -m755 ck-xinit-session %{buildroot}%{_bindir}
%endif
%endif

#don't use xorg xinitrc file, use our own, provided by xinitrc package
rm -fr %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc

%files
%defattr(-,root,root)
%{_bindir}/xinit
%{_bindir}/startx
%if !%{with bootstrap}
%if %mdvver < 201300
%{_bindir}/ck-xinit-session
%endif
%endif
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*
