Name:           chrome-remote-desktop
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
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * %{buildroot}/
rm -rf %{buildroot}/lib
rm -rf %{buildroot}/usr/lib
rm -rf %{buildroot}/usr/lib64

mkdir -p %{buildroot}/etc/X11/Xsession.d
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/etc/pam.d

find %{_builddir} -name "chrome-remote-desktop@.service" -exec cp -f {} %{buildroot}/usr/lib/systemd/system/ \; 2>&1 || true
find %{_builddir} -path "*etc/pam.d/chrome-remote-desktop" -exec cp -f {} %{buildroot}/etc/pam.d/ \; 2>&1 || true

mkdir -p %{buildroot}/opt/google/chrome-remote-desktop/
cat << 'EOF2' > %{buildroot}/opt/google/chrome-remote-desktop/crd-fedora-launcher.sh
#!/bin/bash
# Capture username from systemd argument dynamically
TARGET_USER=$1
if [ -z "$TARGET_USER" ]; then
    TARGET_USER=$(whoami)
fi

export USER=$TARGET_USER
export HOME=/home/$TARGET_USER

# Auto-detect X11 display
export DISPLAY=$(ls /tmp/.X11-unix/X* 2>/dev/null | head -n 1 | sed 's|.*X|:|')
[ -z "$DISPLAY" ] && export DISPLAY=:0
export XAUTHORITY=/home/$TARGET_USER/.Xauthority

# Find host config JSON for active user
HOST_CONFIG=$(ls /home/$TARGET_USER/.config/chrome-remote-desktop/host#*.json 2>/dev/null | head -n 1)

if [ -z "$HOST_CONFIG" ]; then
    echo "Error: Host config not found for user $TARGET_USER" >&2
    exit 1
fi

exec /opt/google/chrome-remote-desktop/chrome-remote-desktop-host --host-config="$HOST_CONFIG" --min-port=15465 --max-port=15475
EOF2
chmod +x %{buildroot}/opt/google/chrome-remote-desktop/crd-fedora-launcher.sh

mkdir -p %{buildroot}/usr/lib/systemd/system/chrome-remote-desktop@.service.d/
cat << 'EOF3' > %{buildroot}/usr/lib/systemd/system/chrome-remote-desktop@.service.d/override.conf
[Service]
ExecStart=
ExecStart=/opt/google/chrome-remote-desktop/crd-fedora-launcher.sh %i
EOF3

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
/opt/google/chrome-remote-desktop/crd-fedora-launcher.sh
/usr/lib/systemd/system/chrome-remote-desktop@.service.d/override.conf
/usr/lib/systemd/system/chrome-remote-desktop@.service
/etc/X11/Xsession.d/
%config(noreplace) /etc/pam.d/chrome-remote-desktop

%changelog
* Tue Oct 27 2026 Builder <builder@localhost> - 157.0.8103.19-2
- Initial build for Fedora XFCE
