# Chrome Remote Desktop for Fedora XFCE

Custom RPM package for Google Chrome Remote Desktop, built specifically for Fedora Linux with the XFCE desktop environment. This package resolves common Fedora-specific issues including Python interpreter paths, PAM modules, SELinux restrictions, and enables seamless multi-user support.

## Key Features

- **Clean Package Name**: Built as `chrome-remote-desktop` without unnecessary suffixes.
- **Dynamic Multi-User Support**: Automatically detects the active user's home directory, X11 display, and `.Xauthority` file. Works for any user without hardcoded paths.
- **Systemd Integration**: Provides proper `systemctl enable/start` support for persistent background hosting.
- **Fedora Compatibility**: Fixes Python shebangs, applies Fedora-compliant PAM policies, and adjusts SELinux contexts automatically.
- **Custom Launcher**: Includes a dynamic wrapper script with systemd drop-in override for flexible per-user deployment.

## Installation & Usage

| Step | Command / Action | Description |
| :-- | :-- | :-- |
| 1. Download the RPM | Download the latest `.rpm` from the [Releases](https://github.com/aldnnnz/chrome-remote-desktop-fedora-xfce/releases) page. | Get the prebuilt package. |
| 2. Install the package | `sudo dnf install -y ./chrome-remote-desktop-*.rpm` | Install with dependencies using DNF. |
| 3. Authorize the host | Open [google.com/chrome-remote-desktop](https://remotedesktop.google.com/), copy the Linux authorization command (`DISPLAY=...`), paste it in your terminal, and set a 6-digit PIN. | Link this machine to your Google account. |
| 4. Enable the service | `sudo systemctl daemon-reload`<br>`sudo systemctl enable chrome-remote-desktop@YOUR_USERNAME --now` | Start and enable the host service in the background. Replace `YOUR_USERNAME` with your active Fedora username. |

## Build from Source

If you'd like to build the RPM yourself, see the [spec file](./specs/chrome-remote-desktop-fedora.spec) in the `specs/` directory for the full build configuration.

## Notes

- After installation, the package applies Fedora-specific fixes via the `%post` script automatically.
- The service must be enabled per user using `chrome-remote-desktop@<username>`.
