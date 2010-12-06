%define upstream_name	 HTML-Mason
%define upstream_version 1.45

# useless stuff pulled by ./eg/MyApp/MasonWithSession.pm
%define _requires_exceptions perl(MasonX::Request::PlusApacheSession)
%define _provides_exceptions perl(My

Name:		mason
Version:	%perl_convert_version %{upstream_version}
Release:	%mkrel 2

Summary:	Powerful Perl-based web site development and delivery engine
License:	GPL/Artistic
Group:		Networking/WWW
URL:		http://masonhq.com/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/HTML/%{upstream_name}-%{upstream_version}.tar.gz
Patch0:		HTML-Mason-1.32-netdisco.diff

BuildRequires:	apache-mod_perl
BuildRequires:	perl-libapreq2
BuildRequires:	perl(Cache::Cache) >= 1.0
BuildRequires:	perl-CGI >= 1:3.08
BuildRequires:	perl(Class::Container) >= 0.07
BuildRequires:	perl(Exception::Class) >= 1.15
BuildRequires:	perl(File::Spec) >= 0.8
BuildRequires:	perl(HTML::Entities)
BuildRequires:	perl(Log::Any)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Params::Validate) >= 0.70
BuildRequires:	perl(Scalar::Util) >= 1.01
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Deep)


Requires:	apache-mod_perl
Requires:	perl-HTML-Parser
Requires:	perl-libapreq2
Provides:	perl-HTML-Mason = %{version}-%{release}
Obsoletes:	perl-HTML-Mason
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Mason allows web pages and sites to be constructed from shared, reusable
building blocks called components. Components contain a mix of Perl and HTML,
and can call each other and pass values back and forth like subroutines.
Components increase modularity and eliminate repetitive work: common design
elements (headers, footers, menus, logos) can be extracted into their own
components where they need be changed only once to affect the whole site.

Other Mason features include a graphical site previewing utility, an HTML/data
caching model, and the ability to walk through requests with the Perl debugger.

%prep

%setup -q -n %{upstream_name}-%{upstream_version}
%patch0 -p0

%build
export APACHE=%{_sbindir}/httpd
%{__perl} Build.PL installdirs=vendor
./Build

%check
./Build test

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot}

rm -rf %{buildroot}%{_bindir}

install -d %{buildroot}/var/cache/%{name}
install -d %{buildroot}/var/www/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CREDITS UPGRADE Changes eg htdocs samples
%{perl_vendorlib}/Apache
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/HTML
%attr(-,apache,apache) /var/cache/%{name}
/var/www/%{name}
%{_mandir}/man*/*
