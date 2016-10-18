# TODO: liblam (MPI) or MPE
Summary:	Prolog Compiler
Summary(pl.UTF-8):	Kompilator Prologu
Name:		Yap
Version:	6.2.2
Release:	4
License:	Artistic
Group:		Development/Languages
#Source0Download: http://www.dcc.fc.up.pt/~vsc/Yap/downloads.html
Source0:	http://www.dcc.fc.up.pt/~vsc/Yap/yap-%{version}.tar.gz
# Source0-md5:	95eaa54978e4811ff6e504e7dca9e835
Patch0:		%{name}-acdirs.patch
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}-info.patch
URL:		http://www.dcc.fc.up.pt/~vsc/Yap/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	indent
BuildRequires:	mysql-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary(pl.UTF-8):	Statyczna biblioteka dla kompilatora Prologu YAP
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description static
Static library for YAP prolog.

%description static -l pl.UTF-8
Statyczna biblioteka dla kompilatora prologu YAP.

%prep
%setup -q -n yap-%{version}
%undos configure.in
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	--enable-coroutining \
	%{?debug:--enable-debug-yap} \
	--enable-depth-limit \
	--enable-low-level-tracer

%{__make}

%{__make} info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_examplesdir}/%{name}-%{version},%{_libdir}/%{name}}

%{__make} install install_info \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/Yap/clpbn/examples \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/clpbn

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/web/css
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/Yap

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README* changes*.html docs/yap.tex
%attr(755,root,root) %{_bindir}/yap
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/startup.yss
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_infodir}/pillow_doc.info*
%{_infodir}/yap.info*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libYap.a
