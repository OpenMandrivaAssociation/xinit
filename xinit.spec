Name: xinit
Version: 1.0.2
Release: %mkrel 6
Summary: Initialize an X session
Group: System/X11
Source0: http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
# (fc) 1.0.2-2mdv readd modifications for startx (argument parsing)
# catch sigterm in xinit and startx
Patch0: xinit-1.0.2-startx.patch
# check setuid return value to make sure we drop user privilegies
Patch1: http://xorg.freedesktop.org/releases/X11R7.1/patches/xinit-1.0.2-setuid.diff
License: MIT
BuildRoot: %{_tmppath}/%{name}-root
Requires: xinitrc

BuildRequires: libx11-devel >= 1.0.0
BuildRequires: x11-util-macros >= 1.0.1

%description
The xinit program is used to start the X Window System server and a first
client program on systems that cannot start X directly from /etc/init or in
environments that use multiple window systems. When this first client exits,
xinit will kill the X server and then terminate.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .startx
%patch1 -p0 -b .setuid

%build
%configure2_5x	--x-includes=%{_includedir}\
		--x-libraries=%{_libdir}

%make

%install
rm -rf %{buildroot}
%makeinstall_std

#don't use xorg xinitrc file, use our own, provided by xinitrc package
rm -fr %{buildroot}/%{_libdir}/X11/xinit
ln -s ../../../../%{_sysconfdir}/X11/xinit %{buildroot}/%{_libdir}/X11/xinit

%clean
rm -rf %{buildroot}

%pre
if [ ! -L %{_libdir}/X11/xinit ]; then
 rm -fr %{_libdir}/X11/xinit
fi

%files
%defattr(-,root,root)
%{_bindir}/xinit
%{_bindir}/startx
%{_libdir}/X11/xinit
%{_mandir}/man1/startx.1x.bz2
%{_mandir}/man1/xinit.1x.bz2


