# TODO: ds9, topcat (for Suggests)
#	https://sites.google.com/cfa.harvard.edu/saoimageds9
#	http://www.star.bris.ac.uk/~mbt/topcat/
#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	GNU Astronomy Utilities
Summary(pl.UTF-8):	Narzędzia astronomiczne GNU
Name:		gnuastro
Version:	0.23
Release:	2
License:	GPL v3+
Group:		Applications/Science
Source0:	https://ftp.gnu.org/gnu/gnuastro/%{name}-%{version}.tar.lz
# Source0-md5:	e117816ffd8503f95c92cfc461073fba
Patch0:		%{name}-info.patch
Patch1:		ac.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-numpy.patch
URL:		http://www.gnu.org/software/gnuastro/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cfitsio-devel >= 3.30
BuildRequires:	curl-devel
BuildRequires:	ghostscript >= 9.10
BuildRequires:	gsl-devel >= 2.0
BuildRequires:	help2man
BuildRequires:	libgit2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	lzip
BuildRequires:	make-devel
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	wcslib-devel >= 7.5
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Suggests:	ghostscript >= 9.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# gmk_add_function defined in make executable
%define		skip_post_check_so	libgnuastro_make.so.*

%description
GNU Astronomy Utilities (Gnuastro) is an official GNU package of
programs and a library functions for astronomical data manipulation
and analysis. The programs are run on the operating system's
command-line enabling easy and efficient operation combined with other
installed programs in shell scripts or Makefiles. The libraries are
also usable in C and C++ programs.

%description -l pl.UTF-8
GNU Astronomy Utilities (Gnuastro) to oficjalny pakiet GNU zawierający
programy i funkcje biblioteczne do obróbki i analiz danych
astronomicznych. Programy są uruchamiane z wiersza poleceń systemu
operacyjnego, co pozwala na łatwe i wydajne operowanie w połączeniu z
innymi zainstalowanymi programami lub z poziomu plików Makefile.
Biblioteki mogą być używane w programach w C i C++.

%package devel
Summary:	Header files for Gnuastro library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Gnuastro
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cfitsio-devel
Requires:	gsl-devel
Requires:	libgit2-devel
Requires:	libjpeg-devel
Requires:	libtiff-devel >= 4
Requires:	wcslib-devel >= 7.5
Requires:	xz-devel

%description devel
Header files for Gnuastro library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Gnuastro.

%package static
Summary:	Static Gnuastro library
Summary(pl.UTF-8):	Statyczna biblioteka Gnuastro
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Gnuastro library.

%description static -l pl.UTF-8
Statyczna biblioteka Gnuastro.

%package -n bash-completion-gnuastro
Summary:	Bash completion for gnuastro commands
Summary(pl.UTF-8):	Bashowe uzupełnianie składni poleceń gnuastro
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-gnuastro
Bash completion for gnuastro commands.

%description -n bash-completion-gnuastro -l pl.UTF-8
Bashowe uzupełnianie składni poleceń gnuastro.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
# regenerate for as-needed to work
%{__libtoolize}
%{__aclocal} -I bootstrapped/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnuastro*.la
%if %{with static_libs}
# make plugin
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnuastro_make.a
%endif
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/gnuastro/README

install -d $RPM_BUILD_ROOT%{bash_compdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/gnuastro/completion.bash $RPM_BUILD_ROOT%{bash_compdir}/gnuastro

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/astarithmetic
%attr(755,root,root) %{_bindir}/astbuildprog
%attr(755,root,root) %{_bindir}/astconvertt
%attr(755,root,root) %{_bindir}/astconvolve
%attr(755,root,root) %{_bindir}/astcosmiccal
%attr(755,root,root) %{_bindir}/astcrop
%attr(755,root,root) %{_bindir}/astfits
%attr(755,root,root) %{_bindir}/astmatch
%attr(755,root,root) %{_bindir}/astmkcatalog
%attr(755,root,root) %{_bindir}/astmkprof
%attr(755,root,root) %{_bindir}/astnoisechisel
%attr(755,root,root) %{_bindir}/astquery
%attr(755,root,root) %{_bindir}/astscript-color-faint-gray
%attr(755,root,root) %{_bindir}/astscript-ds9-region
%attr(755,root,root) %{_bindir}/astscript-fits-view
%attr(755,root,root) %{_bindir}/astscript-psf-scale-factor
%attr(755,root,root) %{_bindir}/astscript-psf-select-stars
%attr(755,root,root) %{_bindir}/astscript-psf-stamp
%attr(755,root,root) %{_bindir}/astscript-psf-subtract
%attr(755,root,root) %{_bindir}/astscript-psf-unite
%attr(755,root,root) %{_bindir}/astscript-pointing-simulate
%attr(755,root,root) %{_bindir}/astscript-radial-profile
%attr(755,root,root) %{_bindir}/astscript-sort-by-night
%attr(755,root,root) %{_bindir}/astscript-zeropoint
%attr(755,root,root) %{_bindir}/astsegment
%attr(755,root,root) %{_bindir}/aststatistics
%attr(755,root,root) %{_bindir}/asttable
%attr(755,root,root) %{_bindir}/astwarp
%attr(755,root,root) %{_libdir}/libgnuastro.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuastro.so.21
%attr(755,root,root) %{_libdir}/libgnuastro_make.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuastro_make.so.21
%attr(755,root,root) %{_libdir}/libgnuastro_make.so
%dir %{_sysconfdir}/gnuastro
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuastro/ast*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuastro/gnuastro.conf
%{_datadir}/gnuastro
%{_infodir}/gnuastro.info*
%{_infodir}/gnuastro-figures
%{_mandir}/man1/astarithmetic.1*
%{_mandir}/man1/astbuildprog.1*
%{_mandir}/man1/astconvertt.1*
%{_mandir}/man1/astconvolve.1*
%{_mandir}/man1/astcosmiccal.1*
%{_mandir}/man1/astcrop.1*
%{_mandir}/man1/astfits.1*
%{_mandir}/man1/astmatch.1*
%{_mandir}/man1/astmkcatalog.1*
%{_mandir}/man1/astmkprof.1*
%{_mandir}/man1/astnoisechisel.1*
%{_mandir}/man1/astquery.1*
%{_mandir}/man1/astscript-ds9-region.1*
%{_mandir}/man1/astscript-fits-view.1*
%{_mandir}/man1/astscript-pointing-simulate.1*
%{_mandir}/man1/astscript-psf-scale-factor.1*
%{_mandir}/man1/astscript-psf-select-stars.1*
%{_mandir}/man1/astscript-psf-stamp.1*
%{_mandir}/man1/astscript-psf-subtract.1*
%{_mandir}/man1/astscript-psf-unite.1*
%{_mandir}/man1/astscript-radial-profile.1*
%{_mandir}/man1/astscript-sort-by-night.1*
%{_mandir}/man1/astscript-zeropoint.1*
%{_mandir}/man1/astsegment.1*
%{_mandir}/man1/aststatistics.1*
%{_mandir}/man1/asttable.1*
%{_mandir}/man1/astwarp.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnuastro.so
%{_includedir}/gnuastro
%{_pkgconfigdir}/gnuastro.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgnuastro.a
%endif

%files -n bash-completion-gnuastro
%defattr(644,root,root,755)
%{bash_compdir}/gnuastro
