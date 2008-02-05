#
# Conditional build:
%bcond_without	source		# don't build kernel-source package

%bcond_with	verbose		# verbose build (V=1)
%bcond_with	pae		# build PAE (HIGHMEM64G) support on uniprocessor
%bcond_with	preempt-nort	# build preemptable no realtime kernel

%{?debug:%define with_verbose 1}

%ifnarch %{ix86}
%undefine	with_pae
%endif

%ifarch %{ix86} ppc
%define		have_isa	1
%else
%define		have_isa	0
%endif

%define		have_pcmcia	1
%define		have_oss	1
%define		have_sound	1

%define		alt_kernel	vanilla

%define		_basever	2.6.24
%define		_postver	%{nil}
%define		_rel		0.4

# for rc kernels basever is the version patch (source1) should be applied to
#%define		_ver		2.6.20
#%define		_rc			rc4
# for non rc-kernels these should be %{nil}
%define		_ver		%{nil}
%define		_rc			%{nil}

Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{alt_kernel}
Version:	%{?_ver:%{_ver}}%{_basever}%{_postver}
Release:	%{?_rc:%{_rc}}%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	3f23ad4b69d0a552042d1ed0f4399857
%if "%{_postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{_basever}%{_postver}.bz2
# Source1-md5:	8dc6d14fb270d13e8ef670d23387b418
%endif
%if "%{_ver}" != "%{nil}"
Source10:	http://www.kernel.org/pub/linux/kernel/v2.6/testing/patch-%{_ver}-%{_rc}.bz2
# Source10-md5:	9b325c6086ad2a3fcde643f01a4c4640
%endif

Source2:	kernel-vanilla-module-build.pl
Source3:	kernel-vanilla-config.h
Source6:	kernel-config.py
Source7:	kernel-config-update.py
Source8:	kernel-multiarch.make

Source19:	kernel-vanilla-multiarch.conf

Source40:	kernel-vanilla-preempt-nort.config
Source41:	kernel-vanilla-no-preempt-nort.config

URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.14.90.0.7
%ifarch sparc sparc64
BuildRequires:	elftoaout
%endif
BuildRequires:	gcc >= 5:3.2
BuildRequires:	module-init-tools
# for hostname command
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
Autoreqprov:	no
Requires:	coreutils
Requires:	geninitrd >= 2.57
Requires:	module-init-tools >= 0.9.9
Conflicts:	e2fsprogs < 1.29
Conflicts:	isdn4k-utils < 3.1pre1
Conflicts:	jfsutils < 1.1.3
Conflicts:	module-init-tool < 0.9.10
Conflicts:	nfs-utils < 1.0.5
Conflicts:	oprofile < 0.9
Conflicts:	ppp < 1:2.4.0
Conflicts:	procps < 3.2.0
Conflicts:	quota-tools < 3.09
Conflicts:	reiserfsprogs < 3.6.3
Conflicts:	udev < 1:071
Conflicts:	util-linux < 2.10o
Conflicts:	xfsprogs < 2.6.0
ExclusiveArch:	%{ix86} %{x8664} ppc alpha sparc
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86} %{x8664}
%define		target_arch_dir		x86
%else
%define		target_arch_dir		%{_target_base_arch}
%endif

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	.*%{_kernelsrcdir}/.*
%define		_noautochrpath	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}smp
# _localversion is just that without version for "> localversion"
%define		_localversion %{release}smp
%define		kernel_release %{version}_%{alt_kernel}-%{_localversion}
%define		_kernelsrcdir	/usr/src/linux-%{version}_%{alt_kernel}

%define		topdir	%{_builddir}/%{name}-%{version}
%define		srcdir	%{topdir}/linux-%{_basever}
%define		objdir	%{topdir}/o

%define	CommonOpts	HOSTCC="%{__cc}" HOSTCFLAGS="-Wall -Wstrict-prototypes %{rpmcflags} -fomit-frame-pointer" O=%{objdir}
%if "%{_target_base_arch}" != "%{_arch}"
	%define	MakeOpts %{CommonOpts} ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	MakeOpts %{CommonOpts} CC="%{__cc}" ARCH=%{_target_base_arch}
	%define	DepMod /sbin/depmod
	%endif

%else
	%define MakeOpts %{CommonOpts} CC="%{__cc}"
	%define	DepMod /sbin/depmod
%endif

%define __features Enabled features:\
%{?debug: - DEBUG}\
%define Features %(echo "%{__features}
%{?with_pae: - PAE (HIGHMEM64G) support}" | sed '/^$/d')
# vim: "

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%{Features}

%description -l de.UTF-8
Das Kernel-Packet enthält den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist für grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Prozeß-Management, Geräte Ein- und Ausgaben, usw.

%{Features}

%description -l fr.UTF-8
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un système d'exploitation Linux. Le noyau traite les
fonctions basiques d'un système d'exploitation: allocation mémoire,
allocation de process, entrée/sortie de peripheriques, etc.

%{Features}

%description -l pl.UTF-8
Pakiet zawiera jądro Linuksa niezbędne do prawidłowego działania
Twojego komputera. Zawiera w sobie sterowniki do sprzętu znajdującego
się w komputerze, takiego jak sterowniki dysków itp.

%{Features}

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de.UTF-8):	vmlinux - dekompressiertes Kernel Bild
Summary(pl.UTF-8):	vmlinux - rozpakowany obraz jądra
Group:		Base/Kernel

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de.UTF-8
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl.UTF-8
vmlinux - rozpakowany obraz jądra.

%package drm
Summary:	DRM kernel modules
Summary(de.UTF-8):	DRM Kernel Treiber
Summary(pl.UTF-8):	Sterowniki DRM
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description drm
DRM kernel modules

%description drm -l de.UTF-8
DRM Kernel Treiber

%description drm -l pl.UTF-8
Sterowniki DRM

%package pcmcia
Summary:	PCMCIA modules
Summary(de.UTF-8):	PCMCIA Module
Summary(pl.UTF-8):	Moduły PCMCIA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	pcmcia-cs < 3.1.21
Conflicts:	pcmciautils < 004
Autoreqprov:	no

%description pcmcia
PCMCIA modules

%description pcmcia -l de.UTF-8
PCMCIA Module

%description pcmcia -l pl.UTF-8
Moduły PCMCIA

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de.UTF-8):	ALSA Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku ALSA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-alsa
ALSA (Advanced Linux Sound Architecture) sound drivers.

%description sound-alsa -l de.UTF-8
ALSA (Advanced Linux Sound Architecture) Sound-Treiber.

%description sound-alsa -l pl.UTF-8
Sterowniki dźwięku ALSA (Advanced Linux Sound Architecture).

%package sound-oss
Summary:	OSS kernel modules
Summary(de.UTF-8):	OSS Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku OSS
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de.UTF-8
OSS (Open Sound System) Treiber.

%description sound-oss -l pl.UTF-8
Sterowniki dźwięku OSS (Open Sound System).

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Autoreqprov:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten die beim rekompilieren des Kernels
oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package source
Summary:	Kernel source tree
Summary(de.UTF-8):	Der Kernel Quelltext
Summary(pl.UTF-8):	Kod źródłowy jądra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. It is required to build
most C programs as they depend on constants defined in here. You can
also build a custom kernel that is better tuned to your particular
hardware.

%description source -l de.UTF-8
Das Kernel-Source-Packet enthält den source code (C/Assembler-Code)
des Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zurückgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien können auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr.UTF-8
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont nécessaires pour compiler la plupart des
programmes C, car il dépend de constantes définies dans le code
source. Les sources peuvent être aussi utilisée pour compiler un noyau
personnalisé pour avoir de meilleures performances sur des matériels
particuliers.

%description source -l pl.UTF-8
Pakiet zawiera kod źródłowy jądra systemu.

%package doc
Summary:	Kernel documentation
Summary(de.UTF-8):	Kernel Dokumentation
Summary(pl.UTF-8):	Dokumentacja do jądra Linuksa
Group:		Documentation
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
Documentation.

%prep
%setup -qc
install -d o/scripts
ln -s %{SOURCE6} o/scripts/kernel-config.py
ln -s %{SOURCE7} o/scripts/kernel-config-update.py
ln -s %{SOURCE2} o/scripts/kernel-module-build.pl
ln -s %{SOURCE8} Makefile

cd linux-%{_basever}
%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif
%if "%{_ver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE10} | %{__patch} -p1 -s
%endif

# if we really want to have vanilla kernel we should create copy from Makefile
#cp Makefile{,.vanilla}

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}_%{alt_kernel}#g' Makefile

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%build
cat > multiarch.make <<'EOF'
# generated by %{name}.spec
srctree		:= %{_builddir}/%{name}-%{version}/linux-%{_basever}
objtree		:= %{objdir}
SRCARCH		:= %{target_arch_dir}
ARCH		:= %{_target_base_arch}
Q			:= %{!?with_verbose:@}
MAKE_OPTS	:= %{MakeOpts}

CONFIGS += %{_sourcedir}/kernel-vanilla-multiarch.conf
%if %{with preempt-nort}
CONFIGS += %{_sourcedir}/kernel-vanilla-preempt-nort.config
%else
CONFIGS += %{_sourcedir}/kernel-vanilla-no-preempt-nort.config
%endif

# config where we ignore timestamps
CONFIG_NODEP += %{objdir}/pykconfig.conf
EOF

# update config at spec time
# if you have config file, add it to above Makefile
pykconfig() {
	set -x
	echo '# %{name}.spec overrides'
	echo 'LOCALVERSION="-%{_localversion}"'

	echo '# debug options'
	%{?debug:echo 'DEBUG_SLAB=y'}
	%{?debug:echo 'DEBUG_PREEMPT=y'}
	%{?debug:echo 'RT_DEADLOCK_DETECT=y'}

%ifarch %{ix86}
	echo '# x86 tuneup'
	%ifnarch i386
	echo 'M386=n'
	%endif
	%ifarch i486
	echo 'M486=y'
	%endif
	%ifarch i586
	echo 'M586=y'
	%endif
	%ifarch i686
	echo 'M686=y'
	%endif
	%ifarch pentium3
	echo 'MPENTIUMIII=y'
	%endif
	%ifarch pentium4
	echo 'MPENTIUM4=y'
	%endif
	%ifarch athlon
	echo 'MK7=y'
	%endif
	%ifarch i686 athlon pentium3 pentium4
	%if %{with pae}
		echo 'HIGHMEM4G=n'
		echo 'HIGHMEM64G=y'
		echo 'X86_PAE=y'
	%endif
	echo 'MATH_EMULATION=n'
	%endif
%endif

awk '{printf("%s=\n", $NF)}' >/dev/null <<'EOF'
.config:3:warning: trying to assign nonexistent symbol GENERIC_TIME
.config:4:warning: trying to assign nonexistent symbol GENERIC_CMOS_UPDATE
.config:5:warning: trying to assign nonexistent symbol GENERIC_CLOCKEVENTS
.config:19:warning: trying to assign nonexistent symbol GENERIC_TIME_VSYSCALL
.config:21:warning: trying to assign nonexistent symbol ARCH_POPULATES_NODE_MAP
.config:108:warning: trying to assign nonexistent symbol GENERIC_CLOCKEVENTS_BUILD
.config:110:warning: trying to assign nonexistent symbol SCHED_NO_NO_OMIT_FRAME_POINTER
.config:112:warning: trying to assign nonexistent symbol NODES_SHIFT
.config:131:warning: trying to assign nonexistent symbol HZ_100
.config:132:warning: trying to assign nonexistent symbol HZ_250
.config:133:warning: trying to assign nonexistent symbol HZ_300
.config:134:warning: trying to assign nonexistent symbol HZ_1000
.config:135:warning: trying to assign nonexistent symbol HZ
.config:138:warning: trying to assign nonexistent symbol PM_LEGACY
.config:139:warning: trying to assign nonexistent symbol PM_DEBUG
.config:140:warning: trying to assign nonexistent symbol PM_SLEEP_SMP
.config:141:warning: trying to assign nonexistent symbol PM_SLEEP
.config:142:warning: trying to assign nonexistent symbol SUSPEND_SMP_POSSIBLE
.config:143:warning: trying to assign nonexistent symbol SUSPEND
.config:144:warning: trying to assign nonexistent symbol HIBERNATION_SMP_POSSIBLE
.config:146:warning: trying to assign nonexistent symbol PM_STD_PARTITION
.config:147:warning: trying to assign nonexistent symbol CPU_FREQ_DEFAULT_GOV_ONDEMAND
.config:148:warning: trying to assign nonexistent symbol CPU_FREQ_DEFAULT_GOV_CONSERVATIVE
.config:150:warning: trying to assign nonexistent symbol PCIEPORTBUS
.config:151:warning: trying to assign nonexistent symbol HOTPLUG_PCI_PCIE
.config:158:warning: trying to assign nonexistent symbol PCCARD
.config:159:warning: trying to assign nonexistent symbol PCMCIA_DEBUG
.config:161:warning: trying to assign nonexistent symbol PCMCIA_LOAD_CIS
.config:162:warning: trying to assign nonexistent symbol PCMCIA_IOCTL
.config:164:warning: trying to assign nonexistent symbol YENTA
.config:165:warning: trying to assign nonexistent symbol YENTA_O2
.config:166:warning: trying to assign nonexistent symbol YENTA_RICOH
.config:167:warning: trying to assign nonexistent symbol YENTA_TI
.config:168:warning: trying to assign nonexistent symbol YENTA_ENE_TUNE
.config:169:warning: trying to assign nonexistent symbol YENTA_TOSHIBA
.config:170:warning: trying to assign nonexistent symbol PD6729
.config:171:warning: trying to assign nonexistent symbol I82092
.config:172:warning: trying to assign nonexistent symbol I82365
.config:173:warning: trying to assign nonexistent symbol TCIC
.config:174:warning: trying to assign nonexistent symbol PCMCIA_PROBE
.config:175:warning: trying to assign nonexistent symbol PCCARD_NONSTATIC
.config:176:warning: trying to assign nonexistent symbol HOTPLUG_PCI
.config:177:warning: trying to assign nonexistent symbol HOTPLUG_PCI_FAKE
.config:178:warning: trying to assign nonexistent symbol HOTPLUG_PCI_COMPAQ
.config:179:warning: trying to assign nonexistent symbol HOTPLUG_PCI_COMPAQ_NVRAM
.config:180:warning: trying to assign nonexistent symbol HOTPLUG_PCI_IBM
.config:181:warning: trying to assign nonexistent symbol HOTPLUG_PCI_ACPI
.config:182:warning: trying to assign nonexistent symbol HOTPLUG_PCI_ACPI_IBM
.config:183:warning: trying to assign nonexistent symbol HOTPLUG_PCI_CPCI
.config:184:warning: trying to assign nonexistent symbol HOTPLUG_PCI_CPCI_ZT5550
.config:185:warning: trying to assign nonexistent symbol HOTPLUG_PCI_CPCI_GENERIC
.config:186:warning: trying to assign nonexistent symbol HOTPLUG_PCI_SHPC
.config:3179:warning: trying to assign nonexistent symbol RELAYFS_FS
.config:3181:warning: trying to assign nonexistent symbol INPUT_TSDEV
.config:3183:warning: trying to assign nonexistent symbol NET_SCH_ESFQ
.config:3185:warning: trying to assign nonexistent symbol IMQ_BEHAVIOR_BA
.config:3186:warning: trying to assign nonexistent symbol MTD_OBSOLETE_CHIPS
.config:3187:warning: trying to assign nonexistent symbol TIPAR
.config:3188:warning: trying to assign nonexistent symbol IP_ROUTE_FWMARK
.config:3190:warning: trying to assign nonexistent symbol NET_DIVERT
.config:3191:warning: trying to assign nonexistent symbol CC_ALIGN_LOOPS
.config:3192:warning: trying to assign nonexistent symbol IMQ
.config:3193:warning: trying to assign nonexistent symbol ATM_DD
.config:3194:warning: trying to assign nonexistent symbol IP_DCCP_UNLOAD_HACK
.config:3196:warning: trying to assign nonexistent symbol RAMFS
.config:3197:warning: trying to assign nonexistent symbol INPUT_TSDEV_SCREEN_Y
.config:3198:warning: trying to assign nonexistent symbol INPUT_TSDEV_SCREEN_X
.config:3200:warning: trying to assign nonexistent symbol DLCI_COUNT
.config:3201:warning: trying to assign nonexistent symbol SOUND_TVMIXER
.config:3202:warning: trying to assign nonexistent symbol SCSI_SATA
.config:3206:warning: trying to assign nonexistent symbol DVB
.config:3207:warning: trying to assign nonexistent symbol CC_ALIGN_FUNCTIONS
.config:3208:warning: trying to assign nonexistent symbol NET_ESTIMATOR
.config:3210:warning: trying to assign nonexistent symbol SENSORS_RTC8564
.config:3211:warning: trying to assign nonexistent symbol JFFS_PROC_FS
.config:3212:warning: trying to assign nonexistent symbol ZISOFS_FS
.config:3220:warning: trying to assign nonexistent symbol NETDEBUG
.config:3221:warning: trying to assign nonexistent symbol REISER4_DEBUG
.config:3222:warning: trying to assign nonexistent symbol BACKLIGHT_DEVICE
.config:3223:warning: trying to assign nonexistent symbol CC_ALIGN_JUMPS
.config:3225:warning: trying to assign nonexistent symbol SYNCLINK_SYNCPPP
.config:3228:warning: trying to assign nonexistent symbol CC_ALIGN_LABELS
.config:3230:warning: trying to assign nonexistent symbol IMQ_NUM_DEVS
.config:3232:warning: trying to assign nonexistent symbol SECURITY_SECLVL
.config:3233:warning: trying to assign nonexistent symbol NETPOLL_RX
.config:3237:warning: trying to assign nonexistent symbol LCD_DEVICE
.config:3238:warning: trying to assign nonexistent symbol SOFTWARE_SUSPEND
.config:3239:warning: trying to assign nonexistent symbol RTC_X1205_I2C
.config:3242:warning: trying to assign nonexistent symbol RXRPC
.config:3245:warning: trying to assign nonexistent symbol JFFS_FS_VERBOSE
.config:3246:warning: trying to assign nonexistent symbol OBSOLETE_MODPARM
.config:3248:warning: trying to assign nonexistent symbol NET_WIRELESS_RTNETLINK
.config:3249:warning: trying to assign nonexistent symbol IMQ_BEHAVIOR_AB
.config:3250:warning: trying to assign nonexistent symbol IMQ_BEHAVIOR_AA
.config:3251:warning: trying to assign nonexistent symbol I2C_ISA
.config:3252:warning: trying to assign nonexistent symbol NET_SCH_CLK_JIFFIES
.config:3254:warning: trying to assign nonexistent symbol NET_SCH_CLK_GETTIMEOFDAY
.config:3256:warning: trying to assign nonexistent symbol DEBUG_RWSEMS
.config:3257:warning: trying to assign nonexistent symbol IP_ROUTE_MULTIPATH_CACHED
.config:3258:warning: trying to assign nonexistent symbol MTD_BLKMTD
.config:3261:warning: trying to assign nonexistent symbol OBSOLETE_INTERMODULE
.config:3264:warning: trying to assign nonexistent symbol JFFS_FS
.config:3269:warning: trying to assign nonexistent symbol IP_ROUTE_MULTIPATH_DRR
.config:3270:warning: trying to assign nonexistent symbol IP_ROUTE_MULTIPATH_RR
.config:3271:warning: trying to assign nonexistent symbol DECNET_ROUTE_FWMARK
.config:3274:warning: trying to assign nonexistent symbol IMQ_BEHAVIOR_BB
.config:3277:warning: trying to assign nonexistent symbol OSS_OBSOLETE_DRIVER
.config:3279:warning: trying to assign nonexistent symbol IP_ROUTE_MULTIPATH_WRANDOM
.config:3280:warning: trying to assign nonexistent symbol IP_ROUTE_MULTIPATH_RANDOM
.config:3282:warning: trying to assign nonexistent symbol REISER4_FS
.config:3284:warning: trying to assign nonexistent symbol FB_SPLASH
.config:3286:warning: trying to assign nonexistent symbol UNWIND_INFO
.config:3288:warning: trying to assign nonexistent symbol NET_RADIO
.config:3289:warning: trying to assign nonexistent symbol NET_SCH_CLK_CPU
.config:3291:warning: trying to assign nonexistent symbol UTS_NS
.config:3292:warning: trying to assign nonexistent symbol IPC_NS
.config:3294:warning: trying to assign nonexistent symbol IPV6_ROUTE_FWMARK
.config:3298:warning: trying to assign nonexistent symbol PREEMPT_NONE
.config:3299:warning: trying to assign nonexistent symbol PREEMPT_VOLUNTARY
.config:3301:warning: trying to assign nonexistent symbol PREEMPT_BKL
EOF
}

# generate .config and .config.conf
pykconfig > %{objdir}/pykconfig.conf
%{__make} pykconfig

# build kernel
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

# /lib/modules
%{__make} %{MakeOpts} %{!?with_verbose:-s} modules_install \
	-C %{objdir} \
	%{?with_verbose:V=1} \
	DEPMOD=%{DepMod} \
	INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
	KERNELRELEASE=%{kernel_release}

mkdir $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/misc

# /boot
install -d $RPM_BUILD_ROOT/boot
install %{objdir}/System.map $RPM_BUILD_ROOT/boot/System.map-%{kernel_release}
%ifarch %{ix86} %{x8664}
install %{objdir}/arch/%{target_arch_dir}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif
%ifarch ppc
install %{objdir}/vmlinux $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif
install %{objdir}/vmlinux $RPM_BUILD_ROOT/boot/vmlinux-%{kernel_release}

# for initrd
touch $RPM_BUILD_ROOT/boot/initrd-%{kernel_release}.gz

%if "%{_target_base_arch}" != "%{_arch}"
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.dep
%endif

# /etc/modrobe.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

# /usr/src/linux
install -d $RPM_BUILD_ROOT%{_kernelsrcdir}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al %{srcdir}/COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi
cp -a$l %{srcdir}/* $RPM_BUILD_ROOT%{_kernelsrcdir}

ln -nfs %{_kernelsrcdir} $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/build
ln -nfs %{_kernelsrcdir} $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/source

cp -a %{objdir}/Module.symvers $RPM_BUILD_ROOT%{_kernelsrcdir}/Module.symvers-dist
cp -a %{objdir}/.config $RPM_BUILD_ROOT%{_kernelsrcdir}/config-dist
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h

# collect module-build files and directories
# Usage: kernel-module-build.pl $rpmdir $fileoutdir
fileoutdir=$(pwd)
cd $RPM_BUILD_ROOT%{_kernelsrcdir}
%{objdir}/scripts/kernel-module-build.pl %{_kernelsrcdir} $fileoutdir
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz-%{alt_kernel}.old 2> /dev/null > /dev/null
mv -f /boot/System.map-%{alt_kernel} /boot/System.map-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{kernel_release} /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	mv -f /boot/vmlinuz /boot/vmlinuz.old 2> /dev/null > /dev/null
	mv -f /boot/System.map /boot/System.map.old 2> /dev/null > /dev/null
	ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz
	ln -sf System.map-%{alt_kernel} /boot/System.map
	mv -f %{initrd_dir}/initrd %{initrd_dir}/initrd.old 2> /dev/null > /dev/null
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{kernel_release}

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{kernel_release}.gz --install %{kernel_release} --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinux-%{kernel_release} /boot/vmlinux-%{alt_kernel}

%post drm
%depmod %{kernel_release}

%postun drm
%depmod %{kernel_release}

%post pcmcia
%depmod %{kernel_release}

%postun pcmcia
%depmod %{kernel_release}

%post sound-alsa
%depmod %{kernel_release}

%postun sound-alsa
%depmod %{kernel_release}

%post sound-oss
%depmod %{kernel_release}

%postun sound-oss
%depmod %{kernel_release}

%post headers
rm -f %{_prefix}/src/linux-%{alt_kernel}
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux-%{alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux-%{alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux-%{alt_kernel})" = "linux-%{version}_%{alt_kernel}" ]; then
			rm -f %{_prefix}/src/linux-%{alt_kernel}
		fi
	fi
fi

%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{kernel_release}
/boot/System.map-%{kernel_release}
%ghost /boot/initrd-%{kernel_release}.gz
%dir /lib/modules/%{kernel_release}
%dir /lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/kernel/arch
/lib/modules/%{kernel_release}/kernel/crypto
/lib/modules/%{kernel_release}/kernel/drivers
#%if %{have_oss} && %{have_isa}
#%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/radio/miropcm20*.ko*
#%endif
/lib/modules/%{kernel_release}/kernel/fs
/lib/modules/%{kernel_release}/kernel/kernel
/lib/modules/%{kernel_release}/kernel/lib
/lib/modules/%{kernel_release}/kernel/net
%dir /lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%if %{have_sound}
%ifnarch sparc
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/*/*-alsa.ko*
%endif
%endif
%dir /lib/modules/%{kernel_release}/misc
%if %{have_pcmcia}
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
%endif
%ghost /lib/modules/%{kernel_release}/modules.*

%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}

%if %{have_pcmcia}
%files pcmcia
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{kernel_release}/kernel/sound/pcmcia
%endif

%if %{have_sound}
%files sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound
%exclude %dir /lib/modules/%{kernel_release}/kernel/sound
%exclude /lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%if %{have_oss}
%exclude /lib/modules/%{kernel_release}/kernel/sound/oss
%endif
%if %{have_pcmcia}
%exclude /lib/modules/%{kernel_release}/kernel/sound/pcmcia
%endif

%if %{have_oss}
%files sound-oss
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound/oss
#%if %{have_isa}
#/lib/modules/%{kernel_release}/kernel/drivers/media/radio/miropcm20*.ko*
#%endif
%endif			# %{have_oss}
%endif			# %{have_sound}

%files headers
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/include
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist

%files module-build -f aux_files
%defattr(644,root,root,755)
%{_kernelsrcdir}/Kbuild
%{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%{_kernelsrcdir}/arch/*/kernel/sigframe.h
%dir %{_kernelsrcdir}/scripts
%dir %{_kernelsrcdir}/scripts/kconfig
%{_kernelsrcdir}/scripts/Kbuild.include
%{_kernelsrcdir}/scripts/Makefile*
%{_kernelsrcdir}/scripts/basic
%{_kernelsrcdir}/scripts/mkmakefile
%{_kernelsrcdir}/scripts/mod
%{_kernelsrcdir}/scripts/setlocalversion
%{_kernelsrcdir}/scripts/*.c
%{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/scripts/kconfig/*
/lib/modules/%{kernel_release}/build
/lib/modules/%{kernel_release}/source

%files doc
%defattr(644,root,root,755)
%{_kernelsrcdir}/Documentation

%if %{with source}
%files source -f aux_files_exc
%defattr(644,root,root,755)
%{_kernelsrcdir}/arch/*/[!Mk]*
%{_kernelsrcdir}/arch/*/kernel/[!M]*
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets*
%exclude %{_kernelsrcdir}/arch/*/kernel/sigframe.h
%{_kernelsrcdir}/block
%{_kernelsrcdir}/crypto
%{_kernelsrcdir}/drivers
%{_kernelsrcdir}/fs
%if %{with grsec_minimal}
%{_kernelsrcdir}/grsecurity
%endif
%{_kernelsrcdir}/init
%{_kernelsrcdir}/ipc
%{_kernelsrcdir}/kernel
%{_kernelsrcdir}/lib
%{_kernelsrcdir}/mm
%{_kernelsrcdir}/net
%{_kernelsrcdir}/scripts/*
%{_kernelsrcdir}/samples
%exclude %{_kernelsrcdir}/scripts/Kbuild.include
%exclude %{_kernelsrcdir}/scripts/Makefile*
%exclude %{_kernelsrcdir}/scripts/basic
%exclude %{_kernelsrcdir}/scripts/kconfig
%exclude %{_kernelsrcdir}/scripts/mkmakefile
%exclude %{_kernelsrcdir}/scripts/mod
%exclude %{_kernelsrcdir}/scripts/setlocalversion
%exclude %{_kernelsrcdir}/scripts/*.c
%exclude %{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/sound
%{_kernelsrcdir}/security
%{_kernelsrcdir}/usr
%{_kernelsrcdir}/COPYING
%{_kernelsrcdir}/CREDITS
%{_kernelsrcdir}/MAINTAINERS
%{_kernelsrcdir}/README
%{_kernelsrcdir}/REPORTING-BUGS
%endif
