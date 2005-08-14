#
# Conditional build:
%bcond_without	bsf	# without BSF support
#
Summary:	BeanShell - Lightweight Scripting for Java
Summary(pl):	BeanShell - lekkie skrypty dla Javy
Name:		beanshell
Version:	2.0
%define	_beta	b2
Release:	0.%{_beta}.2
License:	Sun Public License or LGPL
Group:		Development/Languages/Java
Source0:	http://www.beanshell.org/bsh-%{version}%{_beta}-src.jar
# Source0-md5:	f9c938446e5d97b74fd37f3bdbebf84a
Patch0:		%{name}-jdk1.5.patch
URL:		http://www.beanshell.org/
%{?with_bsf:BuildRequires:	bsf}
BuildRequires:	jakarta-ant >= 1.3
BuildRequires:	jdk >= 1.3
BuildRequires:	unzip
Requires:	jre >= 1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BeanShell is a small, free, embeddable Java source interpreter with
object scripting language features, written in Java. BeanShell
dynamically executes standard Java syntax and extends it with common
scripting conveniences such as loose types, commands, and method
closures like those in Perl and JavaScript.

%description -l pl
BeanShell to ma³y, darmowy, osadzalny interpreter kodu ¼ród³owego Javy
z cechami obiektowych jêzyków skryptowych, napisany w Javie. BeanShell
dynamicznie wykonuje standardow± sk³adniê Javy i rozszerza j± o
popularne wygodne elementy skryptowe, takie jak lu¼ne typy, polecenia
i dope³nienia metod podobnie jak Perl czy JavaScript.

%prep
%setup -q -c
%patch0 -p0

%build
cd BeanShell
ant jarall \
	%{!?with_bsf:-Dexclude-bsf='bsh/util/BeanShellBSFEngine.java,TestBshBSF.java'}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cd BeanShell/dist
install bsh-*.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf bsh-*.jar $RPM_BUILD_ROOT%{_javadir}/bsh.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BeanShell/{asm/README-asm.txt,bsf/README,docs/faq/faq.html,docs/images,docs/manual,src/{*.html,*.txt}}
%{_javadir}/*.jar
