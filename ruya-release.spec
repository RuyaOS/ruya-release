%global release_name The Start
%global dist_version 0.1
%global fedora_equal 36
%global fedora_rel 100

Summary:	Ruya release files
Name:		ruya-release
Version:	%{dist_version}
Release:	1
License:	GPLv3

URL: https://ruya.parmg.sa/

Source0:	LICENSE

Source2:	README.Ruya-Release-Notes
Source3:	Ruya-Legal-README.txt

Source6:	85-display-manager.preset
Source7:	90-default.preset
Source8:	90-default-user.preset
Source9:	99-default-disable.preset


Source25:       plasma-desktop.conf

#Source26:       80-kde.preset
Source27:       81-desktop.preset



BuildArch: noarch

Provides: ruya-release = %{version}-%{release}
Provides: ruya-release-variant = %{version}-%{release}
Provides: ruya-release-identity = %{version}-%{release}
Requires: ruya-release-common = %{version}-%{release}
Requires: ruya-dnf


Conflicts: system-release
Provides: system-release
Provides: system-release(%{version})


Conflicts:	fedora-release
Conflicts: fedora-release-variant
Conflicts:	fedora-release-identity


Provides: fedora-release = %{fedora_equal}-%{fedora_rel}
Provides: fedora-release-variant = %{fedora_equal}-%{fedora_rel}
Provides: fedora-release-identity = %{fedora_equal}-%{fedora_rel}

Obsoletes: system-release
Obsoletes: fedora-release


%description
RuyaOS release files


%package common
Summary: Ruya release files

Requires:   ruya-release-variant = %{version}-%{release}
Suggests:   ruya-release

Obsoletes:  generic-release < 30-0.1
Obsoletes:  convert-to-edition < 30-0.7


Requires: ruya-repo
Requires:   fedora-repos(%{fedora_equal})
Conflicts: fedora-release-common
Provides: ruya-release-identity = %{version}-%{release}


%description common
RuyaOS release files




%package notes
Summary:	Release Notes
License:	GPLv3
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
Ruya release notes


%prep

%build
#Nothing to build

%install
install -d %{buildroot}%{_prefix}/lib

echo "Ruya release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:parmg:ruya:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/ruya-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME=Ruya
VERSION="%{dist_version} (%{release_name})"
ID=ruya
ID_LIKE=fedora
VERSION_ID=%{dist_version}
PLATFORM_ID="platform:f%{fedora_equal}"
PRETTY_NAME="Ruya %{dist_version} (%{release_name})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:parmg:ruya:%{dist_version}"
HOME_URL="https://ruya.parmg.sa/"
SUPPORT_URL="https://ruya.parmg.sa/"
DOCUMENTATION_URL="https://ruya.parmg.sa/"
BUG_REPORT_URL="https://ruya.parmg.sa/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{fedora_equal}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{fedora_equal}
PRIVACY_POLICY_URL="https://parmg.sa/privacy"
VARIANT="KDE Plasma"
VARIANT_ID=kde
EOF

# Create the common /etc/issue
echo "\S - (\l)" > %{buildroot}%{_prefix}/lib/issue
echo "PROJECT of PARMG.SA" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S - (\l)" > %{buildroot}%{_prefix}/lib/issue.net
echo "PROJECT of PARMG.SA" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create os-release and issue files for the different editions here
# There are no separate editions for generic-release

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release



install -Dm0644 %{SOURCE25} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/




# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%%fedora                %{fedora_equal}
%%dist                %%{?distprefix}.fc%{fedora_equal}%%{?with_bootstrap:~bootstrap}
%%fc%{fedora_equal}                1
EOF

# Install readme
mkdir -p readme
install -pm 0644 %{SOURCE3} readme/

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE0} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/Ruya-Legal-README.txt

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

# Default system wide
install -Dm0644 %{SOURCE6} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE7} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE8} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/
install -Dm0644 %{SOURCE9} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE9} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/

install -Dm0644 %{SOURCE27} -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%files common
%license licenses/LICENSE licenses/Ruya-Legal-README.txt
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%{_sysconfdir}/ruya-release
#%{_prefix}/lib/systemd/system-preset/80-kde.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%{_sysconfdir}/dnf/protected.d/plasma-desktop.conf

%files
%{_prefix}/lib/os-release


%files notes
%doc readme/*


%changelog
* Sat Oct 8 2022 Mosaab Alzoubi <mosaab[AT]parmg[DOT]sa> - 0.1-1
- Initial build, forked from Fedora.
