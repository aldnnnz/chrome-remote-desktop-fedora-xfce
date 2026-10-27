Name:           chrome-remote-desktop-fedora
Version:        157.0.8103.19
Release:        2%{?dist}
Summary:        Custom Chrome Remote Desktop for Fedora XFCE

License:        Google Chrome Terms of Service
URL:            https://google.com
Source0:        chrome-remote-desktop-data.tar.xz

Requires:       python3-psutil, python3-pip, xorg-x11-server-Xvfb

%description
Custom Chrome Remote Desktop build for Fedora XFCE

%prep
%setup -q -c -T
tar -xf %{SOURCE0}

%build
echo "Build step - binaries already built"

%install
mkdir -p %{buildroot}
cp -a * %{buildroot}/
rm -rf %{buildroot}/lib
rm -rf %{buildroot}/usr/lib

mkdir -p %{buildroot}/etc/X11/Xsession.d
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}/etc/pam.d

SRC=%{_builddir}/chrome-remote-desktop-fedora-157.0.8103.19-build/%{name}-%{version}
cp -f $SRC/lib/systemd/system/chrome-remote-desktop@.service %{buildroot}/usr/lib/systemd/system/ 2>&1 || true
cp -f $SRC/lib/systemd/system/chrome-remote-desktop@.service %{buildroot}/lib/systemd/system/ 2>&1 || true
cp -f $SRC/etc/pam.d/chrome-remote-desktop %{buildroot}/etc/pam.d/ 2>&1 || true

%post
ln -sf /usr/bin/python3 /usr/bin/python
sed -i '1s|.*|#!/usr/bin/python3|' /opt/google/chrome-remote-desktop/chrome-remote-desktop || true
cat << 'PAMEOF' > /etc/pam.d/chrome-remote-desktop
#%PAM-1.0
auth       include      password-auth
account    include      password-auth
session    include      password-auth
PAMEOF
chcon -R -t bin_t /opt/google/chrome-remote-desktop/ || true

%files
/opt/google/chrome-remote-desktop/
/etc/X11/Xsession.d/
/usr/lib/systemd/system/chrome-remote-desktop@.service
%config(noreplace) /etc/pam.d/chrome-remote-desktop

%changelog
* Tue Oct 27 2026 Builder <builder@localhost> - 157.0.8103.19-2
- Initial build for Fedora XFCE
