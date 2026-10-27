Name:           chrome-remote-desktop-fedora
Version:        157.0.8103.19
Release:        1%{?dist}
Summary:        Chrome Remote Desktop kustom untuk Fedora XFCE

License:        Google Chrome Terms of Service
URL:            https://google.com
Source0:        chrome-remote-desktop-data.tar.xz

Requires:       python3-psutil, python3-pip, xorg-x11-server-Xvfb

%description
Chrome Remote Desktop kustom untuk Fedora XFCE

%prep
%setup -q -c -T
tar -xf %{SOURCE0}

%build
echo "Build step - biner sudah matang"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * %{buildroot}/

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
%defattr(-,root,root,-)
/*

%changelog
* Tue Oct 27 2026 Builder <builder@localhost> - 157.0.8103.19-1
- Initial build for Fedora XFCE
