Summary:	Prolog Compiler
Summary(pl.UTF-8):   Kompilator Prologu
Name:		Yap
Version:	4.5.5
Release:	3
License:	Artistic
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/yap/%{name}-%{version}.tar.gz
# Source0-md5:	661e289f4bdac0e6cfc7e59d4421c2a8
Patch0:		%{name}-acdirs.patch
Patch1:		%{name}-port.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-info.patch
URL:		http://www.ncc.up.pt/~vsc/Yap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	indent
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# follow configure
%define		specflags_ia32	-DBP_FREE

%description
A high-performance Prolog compiler developed at LIACC, Universidade do
Porto. The Prolog engine is based in the WAM (Warren Abstract
Machine), with several optimizations for better performance. YAP
follows the Edinburgh tradition, and is largely compatible with the
ISO-Prolog standard and with Quintus and SICStus Prolog.

%description -l pl.UTF-8
Wydajny kompilator Prologu stworzony w LIACC, Universidade do
Porto. Silnik Prologu bazuje na WAM (Warren Abstract Machine), z
różnymi optymalizacjami dla lepszej wydajności. Zgodnie z tradycją
Edinburgh jest on wysoce kompatybilny ze standardem ISO-Prolog oraz
z Prologiem Quintus i SICStus.

%package static
Summary:	Static library for YAP Prolog
Summary(pl.UTF-8):   Statyczna biblioteka dla kompilatora Prologu YAP
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description static
Static library for YAP prolog.

%description static -l pl.UTF-8
Statyczna biblioteka dla kompilatora prologu YAP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
CFLAGS="%{rpmcflags}%{!?debug: -fomit-frame-pointer} -Wall"
%configure \
	C_INTERF_FLAGS="%{rpmcflags} -Wall" \
	C_PARSER_FLAGS="%{rpmcflags} -Wall" \
	--enable-coroutining \
	%{?debug:--enable-debug-yap} \
	--enable-depth-limit \
	--enable-low-level-tracer

%{__make}

%{__make} -C docs info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_examplesdir}/%{name}-%{version},%{_libdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install docs/*info* $RPM_BUILD_ROOT%{_infodir}

for d in chr clpqr; do
	mv -f $RPM_BUILD_ROOT%{_datadir}/Yap/$d/examples \
		$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/$d
done

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* changes4.3.html docs/yap.tex
%attr(755,root,root) %{_bindir}/yap
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/startup
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_infodir}/*info*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libYap.a
