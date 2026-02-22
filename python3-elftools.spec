#
# Conditional build:
%bcond_with	tests	# test suite (requires some specific version of binutils)

%define 	module	elftools
Summary:	Pure-Python library for parsing and analyzing ELF files
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do analizy plików ELF
Name:		python3-%{module}
Version:	0.32
Release:	1
License:	public domain
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyelftools/
Source0:	https://files.pythonhosted.org/packages/source/p/pyelftools/pyelftools-%{version}.tar.gz
# Source0-md5:	240cf39dc5dad992f25cb5a4e4244f88
URL:		https://github.com/eliben/pyelftools
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools >= 1:46.4.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
# readelf
BuildRequires:	binutils
# llvm-dwarfdump
BuildRequires:	llvm
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyelftools is a pure-Python library for parsing and analyzing ELF
files and DWARF debugging information.

%description -l pl.UTF-8
pyelftools to czysto pythonowa biblioteka do analizy plików ELF oraz
informacji dla debuggera DWARF.

%prep
%setup -q -n pyelftools-%{version}

# prebuilt x86_64 binaries
%{__rm} test/external_tools/{readelf,llvm-dwarfdump}
%if %{with tests}
ln -sf /usr/bin/readelf test/external_tools/readelf
ln -sf /usr/bin/llvm-dwarfdump test/external_tools/llvm-dwarfdump
%endif

%build
%py3_build

%if %{with tests}
%{__python3} ./test/all_tests.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# readelf clone example
%{__rm} $RPM_BUILD_ROOT%{_bindir}/readelf.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/pyelftools-%{version}-py*.egg-info
