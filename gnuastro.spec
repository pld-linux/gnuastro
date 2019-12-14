#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	GNU Astronomy Utilities
Summary(pl.UTF-8):	Narzędzia astronomiczne GNU
Name:		gnuastro
Version:	0.11
Release:	2
License:	GPL v3+
Group:		Applications/Science
Source0:	https://ftp.gnu.org/gnu/gnuastro/%{name}-%{version}.tar.lz
# Source0-md5:	5fcb6f89710d9047dabeaec6fe054b43
Patch0:		%{name}-info.patch
Patch1:		ac.patch
URL:		http://www.gnu.org/software/gnuastro/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	cfitsio-devel
BuildRequires:	curl-devel
BuildRequires:	ghostscript >= 9.10
BuildRequires:	gsl-devel >= 2.0
BuildRequires:	help2man
BuildRequires:	libgit2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	lzip
BuildRequires:	tar >= 1:1.22
BuildRequires:	wcslib-devel
BuildRequires:	xz-devel
Suggests:	ghostscript >= 9.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	wcslib-devel
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# regenerate for as-needed to work
%{__libtoolize}
%{__aclocal} -I bootstrapped/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--sysconfdir=%{_sysconfdir}/gnuastro \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnuastro.la
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/gnuastro/README

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
%attr(755,root,root) %{_bindir}/astmknoise
%attr(755,root,root) %{_bindir}/astmkprof
%attr(755,root,root) %{_bindir}/astnoisechisel
%attr(755,root,root) %{_bindir}/astscript-sort-by-night
%attr(755,root,root) %{_bindir}/astsegment
%attr(755,root,root) %{_bindir}/aststatistics
%attr(755,root,root) %{_bindir}/asttable
%attr(755,root,root) %{_bindir}/astwarp
%attr(755,root,root) %{_libdir}/libgnuastro.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuastro.so.9
%dir %{_sysconfdir}/gnuastro
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuastro/ast*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuastro/gnuastro.conf
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
%{_mandir}/man1/astmknoise.1*
%{_mandir}/man1/astmkprof.1*
%{_mandir}/man1/astnoisechisel.1*
%{_mandir}/man1/astscript-sort-by-night.1*
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
