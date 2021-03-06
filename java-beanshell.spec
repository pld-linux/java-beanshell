#
# Conditional build:
%bcond_without	bsf	# without BSF support
#
%define		srcname	beanshell
Summary:	BeanShell - Lightweight Scripting for Java
Summary(pl.UTF-8):	BeanShell - lekkie skrypty dla Javy
Name:		java-beanshell
Version:	2.0
%define		subver	b4
Release:	0.%{subver}.4
License:	Sun Public License v1.0 or LGPL
Group:		Development/Languages/Java
Source0:	http://www.beanshell.org/bsh-%{version}%{subver}-src.jar
# Source0-md5:	49c9cc9872f26d562bffb1e5ec8aa377
Source1:	%{name}.sh
URL:		http://www.beanshell.org/
BuildRequires:	ant >= 1.3
BuildRequires:	antlr
%{?with_bsf:BuildRequires:	java-bsf}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BeanShell is a small, free, embeddable Java source interpreter with
object scripting language features, written in Java. BeanShell
dynamically executes standard Java syntax and extends it with common
scripting conveniences such as loose types, commands, and method
closures like those in Perl and JavaScript.

%description -l pl.UTF-8
BeanShell to mały, darmowy, osadzalny interpreter kodu źródłowego Javy
z cechami obiektowych języków skryptowych, napisany w Javie. BeanShell
dynamicznie wykonuje standardową składnię Javy i rozszerza ją o
popularne wygodne elementy skryptowe, takie jak luźne typy, polecenia
i dopełnienia metod podobnie jak Perl czy JavaScript.

%package javadoc
Summary:	BeanShell API documentation
Summary(pl.UTF-8):	Dokumentacja API BeanShell
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
BeanShell API documentation.

%description javadoc -l pl.UTF-8
Dokumentacja API BeanShell.

%package -n beanshell
Summary:	BeanShell shell startup script
Summary(pl.UTF-8):	Skrypt uruchamiający BeanShell
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description -n beanshell
Shell script that runs beanshell as standalone application.

%description -n beanshell -l pl.UTF-8
Skrypt powłoki uruchamiający beanshell jako niezależną aplikację.

%prep
%setup -q -n BeanShell-%{version}%{subver}

%build
required_jars="%{?with_bsf:bsf}"
export CLASSPATH=$(build-classpath $required_jars)
# javadoc calls shell via this variable
export SHELL=/bin/sh

%ant jarall javadoc \
	%{!?with_bsf:-Dexclude-bsf='bsh/util/BeanShellBSFEngine.java,TestBshBSF.java'}

cp -R docs/manual/html manual

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir},%{_javadocdir}/%{name}-%{version}}

# jars
install dist/bsh-%{version}%{subver}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf bsh-%{version}%{subver}.jar $RPM_BUILD_ROOT%{_javadir}/bsh.jar

cp -a javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

install %SOURCE1 $RPM_BUILD_ROOT%{_bindir}/beanshell

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc asm/README-asm.txt bsf/README src/{*.html,*.txt} docs/{faq/faq.html,images,manual}
%{_javadir}/bsh-%{version}%{subver}.jar
%{_javadir}/bsh.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files -n beanshell
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/beanshell
