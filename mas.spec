%define name	mas
%define version 0.6.3
%define release %mkrel 4

%define major 	1
%define libname %mklibname %name %major

Name: %{name}
Summary: XFree Media Application Server
Version: %{version}
Release: %{release}

Source:		%{name}-%{version}.tar.bz2
Source1:	%{name}-devtools-%{version}.tar.bz2
Source2:	%{name}-control-apps-%{version}.tar.bz2
Source3: 	%{name}48.png
Source4: 	%{name}32.png
Source5: 	%{name}16.png
Patch:		mas-0.6.3-logdir.patch.bz2
Patch1:		mas-0.6.2-fftw.patch.bz2
Patch2:		mas-0.6.3-pinit.patch.bz2
URL:		http://www.mediaapplicationserver.net/
License:	MIT
Group:		Sound
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	fftw2-devel
BuildRequires:	libgtk+2.0-devel
BuildRequires:	chrpath
BuildRequires:  imake
BuildRequires:  gccmakedep
ExclusiveArch: %ix86 alpha

%description
MAS will provide a complete mechanism for media support, for all pluri-modal
media, for all platforms, for all operating systems, for all window systems.
MAS supports the desktop and, transparently, the network. In particular, MAS
will provide complete support for the X Window System, across the network.
MAS is an open system: the complete core will remain under the original MIT
("X") license, equally supporting open and proprietary use and development.
MAS provides mechanisms for structured extension, and will be supported by
dedicated testing and certification processes.

%package devtools
Summary: Developer's Toolkit for MAS
Group:	 Sound
Requires: %name

%description devtools
This is a set of utilities mainly for testing and debuggins a MAS
client-server setup.

mascodectest is a command-line CODEC testing application that inserts two
back-to-back CODECs into a simple audio assemblage. Sample rate and channel
conversion are performed optionally.
masget is a command-line interface to the standard mas_get queries supported
by the core set of devices and the server. Use it to query device parameters
during runtime.
massink takes 16-bit, little-endian, signed, linear, 44.1kHz stereo audio
from standard input and plays it using the default anx assemblage.
masloopback is a command-line anx device testing application that wraps the
recorded output from the anx device back into the mix device of the default
anx assemblage.
masnetstat causes the net device to dump its state information to the server
log file.
masset is a command-line interface to the standard mas_set actions supported
by the core set of devices and the server. Use it to dynamically adjust
device parameters.
massource records 16-bit, little-endian, signed, linear, 44.1kHz stereo audio
from the default anx assemblage and echoes it to standard output.

%package control-apps
Summary: Graphical Interface to MAS
Group:	 Sound
Requires: %name

%description control-apps
This package includes graphical tools to control the Media Application Server.

masconf_gui is a peer-to-peer Internet conferencing application that features
a GTK+ 2.0 graphical user interface.
masmix is a network-transparent volume control that features a GTK+ 2.0
graphical user interface.
masplayer is a network-transparent MP3 player that works with the X Window
System and features a GTK+ 2.0 graphical user interface. It preserves the
compressed MP3 format for network transmission, decoding it on the user's
local system. NOTE: this application requires the separately distributed
codec_mp1a_mad device.
massignal is a network-transparent audio function generator. It can generate
sine, triangle, and square waves, as well as both white and pink filtered
noise signals.

%package -n %{libname}
Summary: Main library for %name
Group: System/Libraries
Provides: %{name} = %{version}-%{release}
Requires: %name >= %version


%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %name.

%package -n %{libname}-devel
Summary: Headers for developing programs that will use %name
Group: Development/C++
Requires: %{libname} = %{version}
#gw for imake: 
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use libraries from %name.

%prep
%setup -q -b 1 -b 2
%patch -p1 -b .logdir
%patch1 -p1 -b .fftw
%patch2 -p1 -b .init

%build

#set prefix
perl -p -i -e 's/usr\/local\/mas/usr/g' config/site.def
#of course, the prefix is also hard-coded elsewhere
perl -p -i -e 's/usr\/local\/mas/usr/g' `find control-apps` mas/assembler.c
#and extra fool-proofing
perl -p -i -e 's/usr\/mas\/lib\/mas/usr\/lib/g' mas/assembler.c
#tell it to build devtools and control-apps
perl -p -i -e 's/clients/clients\ devtools\ control-apps/g' Imakefile
#gw -ansi breaks the build
perl -pi -e 's/-ansi//' config/xfree86.cf
imake -I./config
make CXXDEBUGFLAGS="$RPM_OPT_FLAGS" CDEBUGFLAGS="$RPM_OPT_FLAGS" World
#gw fix init script
cd clients/util
sed "s!MASBINDIR!%_bindir!" < redhat_init.d_mas.cpp > redhat_init.d_mas


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
( cd %buildroot%_bindir
for binary in *;do
 if $(fgrep -q ELF $binary); then chrpath -d $binary;fi
done
)
chmod a+r README LICENSE
mkdir -p %buildroot%_var/log/mas
#menu

#XDG menu

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-masconf_gui.desktop <<EOF
[Desktop Entry]
Name=MASConf
Comment=MAS Internet Conferencing
Exec=%{_bindir}/masconf_gui 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Audio;Video;Player;X-MandrivaLinux-Internet-VideoConference;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-masmix.desktop <<EOF
[Desktop Entry]
Name=MASMix
Comment=MAS Mixer
Exec=%{_bindir}/masmix
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Audio;Mixer;X-MandrivaLinux-Multimedia-Sound;
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-masplayer.desktop <<EOF
[Desktop Entry]
Name=MASMix
Comment=MAS Player
Exec=%{_bindir}/masplayer
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Audio;Player;X-MandrivaLinux-Multimedia-Sound;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE4 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE5 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

#fd.o icons
mkdir -p $RPM_BUILD_ROOT/%_iconsdir/hicolor/{16x16,32x32,48x48}/apps
cat %SOURCE3 > $RPM_BUILD_ROOT/%_iconsdir/hicolor/48x48/apps/%name.png
cat %SOURCE4 > $RPM_BUILD_ROOT/%_iconsdir/hicolor/32x32/apps/%name.png
cat %SOURCE5 > $RPM_BUILD_ROOT/%_iconsdir/hicolor/16x16/apps/%name.png

mkdir -p %buildroot%_initrddir
mv %buildroot/%_sysconfdir/init.d/mas %buildroot%_initrddir

mkdir -p %buildroot%_sysconfdir/logrotate.d
cat > %buildroot%_sysconfdir/logrotate.d/%name <<EOF
%_var/log/%name/*.log {
    weekly
    notifempty
    missingok
}
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service  %{name}


%post control-apps
%update_menus		
%update_icon_cache hicolor
%postun control-apps
%clean_menus
%clean_icon_cache hicolor

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENSE
#gw TODO: run mas as another user?
%config(noreplace) %_initrddir/mas
%config(noreplace) %_sysconfdir/logrotate.d/%name
%{_bindir}/maswavplay
%{_bindir}/masbench
%{_bindir}/mastestdev
%{_bindir}/mas
#gw TODO: this has some wrong paths
%{_bindir}/mas-launch
%{_bindir}/maswatchdog
%{_libdir}/%name
%_datadir/pixmaps/*.png
%_var/log/mas

%files devtools
%defattr(-,root,root)
%doc devtools/README
%{_bindir}/mascodectest
%{_bindir}/masget
%{_bindir}/mashost
%{_bindir}/massink
%{_bindir}/masloopback
%{_bindir}/masnetstat
%{_bindir}/masprobe
%{_bindir}/masset
%{_bindir}/massource
%{_bindir}/massource_set

%files control-apps
%defattr(-,root,root)
%doc control-apps/README
%{_bindir}/masconf_gui
%{_bindir}/masmix
%{_bindir}/masmm
%{_bindir}/masplayer
%{_bindir}/massignal
%{_datadir}/applications/mandriva-masplayer.desktop
%{_datadir}/applications/mandriva-masmix.desktop
%{_datadir}/applications/mandriva-masconf_gui.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_iconsdir}/hicolor/48x48/apps/%name.png
%{_iconsdir}/hicolor/32x32/apps/%name.png
%{_iconsdir}/hicolor/16x16/apps/%name.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/masmkmf
%{_bindir}/mas-config
%{_libdir}/*.so
%_libdir/config
%dir %{_includedir}/%name
%{_includedir}/%name/*.h
