%define module	HTML-Mason

# useless stuff pulled by ./eg/MyApp/MasonWithSession.pm
%define _requires_exceptions perl(MasonX::Request::PlusApacheSession)
%define _provides_exceptions perl(My

Summary:	Powerful Perl-based web site development and delivery engine
Name:		mason
Version:	1.33
Release:	%mkrel 6
License:	GPL/Artistic
Group:		Networking/WWW
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://masonhq.com/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/HTML/%{module}-%{version}.tar.bz2 
Patch0:		HTML-Mason-1.32-netdisco.diff
Requires:	apache-mod_perl
Requires:	perl-HTML-Parser
Requires:	perl-libapreq2
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16
Requires(postun):	rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
BuildRequires:	perl-libapreq2
BuildRequires:	apache-mod_perl
BuildRequires:	perl(Cache::Cache) >= 1.0
BuildRequires:	perl-CGI >= 1:3.08
BuildRequires:	perl(Class::Container) >= 0.07
BuildRequires:	perl(Exception::Class) >= 1.15
BuildRequires:	perl(File::Spec) >= 0.8
BuildRequires:	perl(HTML::Entities)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Params::Validate) >= 0.70
BuildRequires:	perl(Scalar::Util) >= 1.01
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::Builder)
BuildArch:	noarch
Provides:	perl-HTML-Mason = %{version}-%{release}
Obsoletes:	perl-HTML-Mason

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

%setup -q -n %{module}-%{version}
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

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
<IfModule mod_perl.c>

    # Make sure to preload as much code as we can in the parent process.
    PerlModule HTML::Mason::ApacheHandler

    # Apache args method with Mason
    PerlOptions +GlobalRequest
    PerlModule Apache2::Request
    PerlSetVar MasonArgsMethod mod_perl

    # component root
    PerlSetVar MasonCompRoot "/var/www/mason"

    # data directory
    PerlSetVar MasonDataDir "/var/cache/mason"


    # Serve these requests through Mason.
    <LocationMatch "^/mason.*(\.html|\.pl|\.txt)$">
        SetHandler perl-script
        PerlResponseHandler HTML::Mason::ApacheHandler
    </LocationMatch>

    # Hide private components from users.
    <LocationMatch "^/mason.*(dhandler|autohandler|\.m(html|txt|pl))$">
        SetHandler perl-script
        PerlInitHandler Apache::Constants::NOT_FOUND
    </LocationMatch>
</ifModule>
EOF

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CREDITS UPGRADE Changes eg htdocs samples
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{perl_vendorlib}/Apache
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/HTML
%attr(-,apache,apache) /var/cache/%{name}
/var/www/%{name}
%{_mandir}/man*/*
