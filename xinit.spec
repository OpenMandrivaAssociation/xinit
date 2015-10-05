Name:		xinit
Version:	1.3.4
Release:	5
Summary:	Initialize an X session
License:	MIT
Group:		System/X11
URL:		http://cgit.freedesktop.org/xorg/app/xinit
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2

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
# (tpg) prolly not needed these days
#Patch0:		xinit-1.3.4-startx-arguments.patch

# (fc) prevent freeze from applications trying to read stdin (Fedora bug #214649)
Patch2:		xinit-1.0.2-client-session.patch

# (fc) unset XDG_SESSION_COOKIE in startx (Fedora bug #489999)
Patch3:		xinit-1.0.9-unset.patch

# (pz) this patch was taken from the old startx.patch
Patch4:		xinit-1.2.0-replace-xterm-for-xvt.patch

# (tpg) git patches
Patch6:		0000-xinit-startx-Pass-keeptty.patch
Patch7:		0001-startx-Don-t-use-GNU-expr-extensions.patch
Patch8:		0002-Remove-SCO-support-for-SHELL_CMD-and-startx-man-page.patch
Patch9:		0003-Remove-support-for-ancient-A-UX-3.0-support.patch
Patch10:	0004-Remove-left-over-launchagents_DATA-in-CLEANFILES.patch
Patch11:	0005-startx-fix-comment-typo.patch
Patch12:	0006-startx-Fix-startx-picking-an-already-used-display-nu.patch
Patch13:	0007-startx-don-t-init-defaultdisplay-to-0.patch
Patch14:	0008-remove-bogus-escapes.patch

BuildRequires:	pkgconfig(x11) >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
Requires:	xinitrc
Requires:	xauth
Requires:	which

%description
The xinit program is used to start the X Window System server and a first
client program on systems that cannot start X directly from /etc/init or in
environments that use multiple window systems. When this first client exits,
xinit will kill the X server and then terminate.

%prep
%setup -q -n %{name}-%{version}
%apply_patches

%build
%configure
%make XINITDIR=/etc/X11/xinit

%install
%makeinstall_std

#don't use xorg xinitrc file, use our own, provided by xinitrc package
rm -fr %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc

%files
%{_bindir}/xinit
%{_bindir}/startx
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*
