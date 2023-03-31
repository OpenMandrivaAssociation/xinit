Name:		xinit
Version:	1.4.2
Release:	2
Summary:	Initialize an X session
License:	MIT
Group:		System/X11
URL:		http://cgit.freedesktop.org/xorg/app/xinit
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.xz

# Fedora specific patches
# (fc) prevent freeze from applications trying to read stdin (Fedora bug #214649)
Patch1:		xinit-1.0.2-client-session.patch
# A few fixes submitted upstream, rhbz#1177513, rhbz#1203780
Patch5:		0003-startx-Make-startx-auto-display-select-work-with-per.patch

# (fc) 1.0.2-2mdv read modifications for startx (argument parsing)
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
Patch50:	xinit-1.3.4-startx-arguments.patch

# (fc) unset XDG_SESSION_COOKIE in startx (Fedora bug #489999)
Patch53:	xinit-1.0.9-unset.patch

# (pz) this patch was taken from the old startx.patch
Patch54:	xinit-1.3.4-replace-xterm-for-xvt.patch

BuildRequires:	pkgconfig(x11) >= 1.0.0
BuildRequires:	pkgconfig(xorg-macros)
Requires:	xinitrc
Requires:	xauth

%description
The xinit program is used to start the X Window System server and a first
client program on systems that cannot start X directly from /etc/init or in
environments that use multiple window systems. When this first client exits,
xinit will kill the X server and then terminate.

%prep
%autosetup -p1

%build
%configure
%make_build XINITDIR=/etc/X11/xinit

%install
%make_install

#don't use xorg xinitrc file, use our own, provided by xinitrc package
rm -fr %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc

%files
%{_bindir}/xinit
%{_bindir}/startx
%doc %{_mandir}/man1/startx.1*
%doc %{_mandir}/man1/xinit.1*
