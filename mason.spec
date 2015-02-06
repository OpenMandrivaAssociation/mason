%define upstream_name    HTML-Mason
%define upstream_version 1.50

%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(MasonX::Request::PlusApacheSession\\)|perl\\(Apache::Request\\)'
%define __noautoprov 'perl\\(MyApp(.*)\\)'
%else
# useless stuff pulled by ./eg/MyApp/MasonWithSession.pm
%define _requires_exceptions perl(MasonX::Request::PlusApacheSession)
%define _provides_exceptions perl(MyApp
%endif

Name:		mason
Version:	%perl_convert_version %{upstream_version}
Release:	2

Summary:	Powerful Perl-based web site development and delivery engine
License:	GPL/Artistic
Group:		Networking/WWW
URL:		http://masonhq.com/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/HTML/%{upstream_name}-%{upstream_version}.tar.gz
Patch0:		HTML-Mason-1.32-netdisco.diff

BuildRequires:	apache-mod_perl
BuildRequires:	perl-libapreq2
BuildRequires:	perl-devel
BuildRequires:	perl(Cache::Cache) >= 1.0
BuildRequires:	perl(CGI)
BuildRequires:	perl(Class::Container) >= 0.07
BuildRequires:	perl(Exception::Class) >= 1.15
BuildRequires:	perl(File::Spec) >= 0.8
BuildRequires:	perl(HTML::Entities)
BuildRequires:	perl(Log::Any)
BuildRequires:	perl(Params::Validate) >= 0.70
BuildRequires:	perl(Scalar::Util) >= 1.01
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Deep)

Requires:	apache-mod_perl
Requires:	perl-HTML-Parser
Requires:	perl-libapreq2
%rename perl-HTML-Mason
BuildArch:	noarch

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
%__perl Makefile.PL INSTALLDIRS=vendor
%make

%check
%make test

%install
%makeinstall_std
rm -rf %{buildroot}%{_bindir}

install -d %{buildroot}/var/cache/%{name}
install -d %{buildroot}/var/www/%{name}

%files
%doc CREDITS Changes INSTALL LICENSE META.json META.yml README UPGRADE eg samples
%{perl_vendorlib}/HTML
%attr(-,apache,apache) /var/cache/%{name}
/var/www/%{name}
%{_mandir}/man*/*


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.450.0-2mdv2011.0
+ Revision: 612818
- the mass rebuild of 2010.1 packages

* Tue Apr 06 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.450.0-1mdv2010.1
+ Revision: 532150
- update to 1.45

* Sun Feb 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.440.0-2mdv2010.1
+ Revision: 509194
- this is not a webapp, but a webapp development kit, don't ship a configuration file

* Tue Jan 05 2010 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.440.0-1mdv2010.1
+ Revision: 486348
- adding missing buildrequires:
- update to 1.44

* Mon Dec 28 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.430.0-1mdv2010.1
+ Revision: 483038
- update to 1.43

* Sun Jul 12 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.420.0-1mdv2010.0
+ Revision: 394974
- update to 1.42
- using %%perl_convert_version

* Thu Dec 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.40-1mdv2009.1
+ Revision: 310000
- 1.40

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 1.33-6mdv2008.1
+ Revision: 168074
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.33-6mdv2008.0
+ Revision: 83812
- rebuild
- Import mason



* Fri Jun 30 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.33-5mdv2007.0
- relax buildrequires versionning

* Mon Jun 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.33-4mdv2007.0
- rebuild with corrected webapp macros

* Tue Jun 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.33-3mdv2007.0
- rename to %%{name}, as it is not a perl library
- configuration file belongs to %%{_webappconfdir}
- truly minimal configuration files, to avoid side-effects
- change group
- use webapp macros
- use its own private cache directory
- use Module::Build-based build

* Tue May 30 2006 Scott Karns <scottk@mandriva.org> 1.33-2mdv2007.0
- Added BuildRequires perl(HTML::Entities) for t/21-escapes.t
- Added Requires perl-HTML-Parser (provides perl(HTML::Entities)

* Sun May 27 2006 Scott Karns <scottk@mandriva.org> 1.33-1mdv2007.0
- Version 1.33

* Tue May 09 2006 Scott Karns <scottk@mandriva.org> 1.32-4mdk
- Corrected _provides_exceptions

* Tue May 09 2006 Scott Karns <scottk@mandriva.org> 1.32-3mdk
- Updated BuildRequires according to HTML-Mason META.yml and
  to comply with Mandriva perl packaging policy
- Updated source URL to meet Mandriva perl packaging policy
- bzip2'd HTML-Mason-1.32-netdisco.diff
- Added patch for fake_apache status 302 test

* Mon Jan 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1.32-2mdk
- fix the apache config to not set global <LocationMatch directories
  per default. this should instead be set per directory, per 
  application needing it. also used the apache config from fedora 
  extras repository.
- set the MasonDataDir to /var/cache/httpd/mason
- fix deps
- filter out some useless provides
- added P0 after skimming the netdisco mailinglists at sourceforge

* Fri Jan 06 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.32-1mdk
- 1.32
- Bump required apache version

* Sun Oct 09 2005 Oden Eriksson <oeriksson@mandriva.com> 1.31-3mdk
- fix deps, %%post, %%postun and config dir

* Sun Oct 09 2005 Michael Scherer <misc@mandriva.org> 1.31-2mdk
- update BuildRequires, for t/06-compiler.t failing for compiler_id_change
- clean spec
- fix unowned directory problem

* Sat Oct 08 2005 Michael Scherer <misc@mandriva.org> 1.31-1mdk
- update to 1.31 ( not 1.3101, as i think it will requires to use Epoch.
  better wait for 1.32 ).
- remove Apache::Request from config file, as it requires mod_perl1

* Thu Sep 29 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.28-3mdk
- Fix buildrequires

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.28-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Wed Feb 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.28-1mdk
- 1.28
- Add Changes in doc

* Sun Aug 29 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.26-2mdk
- fix deps

* Wed Aug 25 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.26-1mdk
- 1.26
- fixed S1

* Wed Mar 12 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.03-4mdk
- fix requires & build

* Tue Sep 04 2001 Florin <florin@mandrakesoft.com> 1.03-3mdk
- add requires on perl-CGI and mod_perl
- update the /etc/httpd/conf/httpd-perl.conf
- restart the apache server in post, postun

* Thu Aug 30 2001 Florin <florin@mandrakesoft.com> 1.03-2mdk
- skip the user questions
- remove the perllocal.pod file as it conflicts with 5 pckgs

* Mon Jul 23 2001 Stefan van der Eijk <stefan@eijk.nu> 1.03-1mdk
- 1.03
- BuildRequires:	perl-devel perl-Params-Validate
- Copyright --> License

* Wed May 02 2001 Stefan van der Eijk <stefan@eijk.nu> 1.02-1mdk
- 1.02

* Wed May 02 2001 Stefan van der Eijk <stefan@eijk.nu> 0.895-2mdk
- perl 5.6.1

* Thu Dec 14 2000  Florin Grad <florin@mandrakesoft.com> 0.895-1mdk
- 0.895

* Fri Oct 13 2000  Florin Grad <florin@mandrakesoft.com> 0.89-3mdk
- change location according to apache-mod_perl
- added the samples section

* Thu Oct 12 2000  Florin Grad <florin@mandrakesoft.com> 0.89-2mdk
- remove some silly requirements (typo :)

* Tue Oct 11 2000  Florin Grad <florin@mandrakesoft.com> 0.89-1mdk
- first attempt
