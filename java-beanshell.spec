#
# Conditional build:
%bcond_without	bsf	# without BSF support
#
%define		_beta	b4
%define		_rel	4
%include	/usr/lib/rpm/macros.java
Summary:	BeanShell - Lightweight Scripting for Java
Summary(pl.UTF-8):	BeanShell - lekkie skrypty dla Javy
Name:		beanshell
Version:	2.0
Release:	0.%{_beta}.%{_rel}
License:	Sun Public License or LGPL
Group:		Development/Languages/Java
Source0:	http://www.beanshell.org/bsh-%{version}%{_beta}-src.jar
# Source0-md5:	49c9cc9872f26d562bffb1e5ec8aa377
URL:		http://www.beanshell.org/
BuildRequires:	ant >= 1.3
BuildRequires:	antlr
%{?with_bsf:BuildRequires:	bsf}
BuildRequires:	java-gcj-compat-devel
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servlet
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

%prep
%setup -q -n BeanShell-%{version}%{_beta}

%build
required_jars="%{?with_bsf:bsf} servlet"
export CLASSPATH=$(build-classpath $required_jars)
# javadoc calls shell via this variable
export SHELL=/bin/sh

%ant jarall javadoc \
	-Dbuild.compiler=gcj \
	%{!?with_bsf:-Dexclude-bsf='bsh/util/BeanShellBSFEngine.java,TestBshBSF.java'}

cp -R docs/manual/html manual

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version}}

# jars
install dist/bsh-%{version}%{_beta}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf bsh-%{version}%{_beta}.jar $RPM_BUILD_ROOT%{_javadir}/bsh.jar

cp -a javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc asm/README-asm.txt bsf/README src/{*.html,*.txt}
%doc docs/{faq/faq.html,images,manual}
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
