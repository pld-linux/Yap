Summary:	Prolog Compiler
Summary(pl):	Kompilator Prologu
Name:		Yap
Version:	4.4.4
Release:	1
License:	Artistic
Group:		Development/Languages
Source0:	http://www.ncc.up.pt/~vsc/Yap/%{name}-%{version}.tar.gz
# Source0-md5:	7d0f17305c87874dccdad5ce465a164a
# Source0-size:	2970956
Patch0:		%{name}-acdirs.patch
URL:		http://www.ncc.up.pt/~vsc/Yap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel
BuildRequires:	indent
BuildRequires:	gmp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high-performance Prolog compiler developed at LIACC, Universidade do
Porto. The Prolog engine is based in the WAM (Warren Abstract
Machine), with several optimizations for better performance. YAP
follows the Edinburgh tradition, and is largely compatible with the
ISO-Prolog standard and with Quintus and SICStus Prolog.

%description -l pl
Wydajny kompilator Prologu stworzony w LIACC, Universidade do
Porto. Silnik Prologu bazuje na WAM (Warren Abstract Machine), z
ró¿nymi optymalizacjami dla lepszej wydajno¶ci. Zgodnie z tradycj±
Edinburgh jest on wysoce kompatybilny ze standardem ISO-Prolog oraz
z Prologiem Quintus i SICStus.

%package static
Summary:	Static library for YAP Prolog
Summary(pl):	Statyczna biblioteka dla kompilatora Prologu YAP
Group:		Development/Languages
Requires:	%{name} = %{version}

%description static
Static library for YAP prolog.

%description static -l pl
Statyczna biblioteka dla kompilatora prologu YAP.

%prep
%setup -q
%patch0

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	--enable-coroutining \
	--enable-depth-limit \
	--enable-low-level-tracer \
	--enable-depth-limit

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_examplesdir}/%{name}-%{version}}

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
%doc README* INSTALL changes4.3.html docs/yap.tex
%attr(755,root,root) %{_bindir}/yap
%attr(755,root,root) %{_libdir}/Yap/startup
%{_datadir}/Yap
%{_includedir}/Yap
%{_infodir}/*info*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libYap.a
