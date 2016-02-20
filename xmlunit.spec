%global pkg_name xmlunit
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.4
Release:        6.11%{?dist}
Epoch:          0
Summary:        Provides classes to do asserts on xml
License:        BSD
Source0:        http://downloads.sourceforge.net/project/xmlunit/xmlunit%20for%20Java/XMLUnit%20for%20Java%201.4/xmlunit-1.4-src.zip
Source1:        http://repo1.maven.org/maven2/xmlunit/xmlunit/1.0/xmlunit-1.0.pom
URL:            http://xmlunit.sourceforge.net/
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}ant-junit
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix_java_common}xalan-j2
BuildRequires:  %{?scl_prefix_java_common}xerces-j2
BuildRequires:  %{?scl_prefix_java_common}xml-commons-apis

Requires:       %{?scl_prefix_java_common}junit
Requires:       %{?scl_prefix_java_common}xalan-j2
Requires:       %{?scl_prefix_java_common}xml-commons-apis

BuildArch:      noarch

%description
XMLUnit extends JUnit to simplify unit testing of XML. It compares a control
XML document to a test document or the result of a transformation, validates
documents against a DTD, and (from v0.5) compares the results of XPath
expressions.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
sed -i /java.class.path/d build.xml
# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc

echo "junit.lib=$(build-classpath junit)
xmlxsl.lib=
test.report.dir=test" >build.properties

echo "db5.xsl=%{_root_datadir}/sgml/docbook/xsl-ns-stylesheets" >docbook.properties

#Fix wrong-file-end-of-line-encoding
sed -i 's/\r//g' README.txt LICENSE.txt
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
ant -Dbuild.compiler=modern -Dhaltonfailure=yes jar javadocs
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x

mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 0644 build/lib/%{pkg_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -m 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom

%add_maven_depmap

# Javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{?scl:EOF}

%check
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
ant
%{?scl:EOF}

%files -f .mfiles
%doc README.txt LICENSE.txt userguide/XMLUnit-Java.pdf 

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 0:1.4-6.11
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.4-6.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.4-6.9
- Fix BR/R

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.4-6.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.2
- Rebuild to regenerate auto-requires
- Use docbook from %%{_root_datadir}

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.1
- Avoid nested here-documents

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.4-6
- Mass rebuild 2013-12-27

* Fri Sep 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-5
- Enable test suite
- Resolves: rhbz#987412

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-4
- Remove workaround for rpm bug #646523

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Jun 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-2
- Update to latest packaging guidelines
- Cleanup BuildRequires

* Fri Feb 15 2013 Dr. Tilmann Bubeck <t.bubeck@reinform.de> - 0:1.4-1
- update to upstream's xmlunit-1.4

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-3
- Build javadoc only.

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-2
- BR java 1.6 to prevent gcj failure.

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-1
- Update to new upstream.
- Drop gcj.
- Rebuild docs.

* Thu Mar 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.0-8.3
- Added missing Requires jpackage-utils

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-6.2
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0-6jpp.1
- Autorebuild for GCC 4.3

* Thu Jan 17 2008 Permaine Cheung <pcheung@redhat.com> - 0:1.0-5jpp.1
- Update to the same version as upstream

 Tue Dec 18 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-5jpp
- Add poms and depmap frags
- Make Vendor, Distribution based on macro
- Add gcj_support option

* Mon Mar 12 2007 Permaine Cheung <pcheung@redhat.com> - 0:1.0-4jpp.1
- Add missing BR, patch to build javadoc, and other rpmlint issues

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-4jpp
- First JPP-1.7 release

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-3jpp
- Build with ant-1.6.2

* Wed Dec 17 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.0-2jpp
- Fix license and improved description
- Thanks to Ralph Apel who produced a spec - merged version info

* Wed Dec 17 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.0-1jpp
- Initial Version
