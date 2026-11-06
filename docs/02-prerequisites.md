# 02 — Prerequisites

## 1. Host Requirements

The lab was configured on a Windows 11 host.

| Component | Requirement / Actual Configuration |
|---|---|
| Host OS | Windows 11 |
| Hypervisor | Oracle VirtualBox |
| VirtualBox version | 7.2.8r173730 |
| Host memory | 8 GB |
| Virtualization | Hardware virtualization enabled |
| Storage | Sufficient free space for VM files and evidence |

An 8 GB host has limited memory headroom. Avoid running multiple resource-intensive virtual machines simultaneously.

## 2. Software Requirements

- Oracle VirtualBox.
- Kali Linux VirtualBox image.
- Windows PowerShell.
- Git for version control.
- A web browser for downloading official software and accessing documentation.

## 3. Guest VM Requirements

| Setting | Actual Value |
|---|---|
| Guest OS | Kali Linux 2026.3 |
| VM memory | 2048 MB |
| Virtual CPUs | 2 |
| Video memory | 128 MB |
| 3D acceleration | Disabled |
| Network adapter | PCnet-FAST III |
| Network attachment | NAT Network |

The VM's displayed name retains an older 2026.1 image label. The installed guest operating system reports Kali Linux 2026.3.

## 4. Network Requirements

| Parameter | Value |
|---|---|
| NAT Network | NetworkWalks-NAT |
| Subnet | 10.0.0.0/24 |
| Gateway | 10.0.0.1 |
| Kali static IP | 10.0.0.2/24 |
| DNS server | 8.8.8.8 |
| DHCP | Disabled |

## 5. Shared Folder Requirements

Host directory:

`<host-shared-folder-directory>`

VirtualBox shared-folder name:

`Shared-Files`

Guest mount point:

`/downloads`

The shared folder is configured for automatic mounting and permanent availability.

## 6. Evidence Requirements

The project maintains screenshots for:

- VirtualBox version.
- NAT Network configuration.
- VM motherboard, processor, and display settings.
- Network adapter settings.
- Clipboard and drag-and-drop settings.
- Shared-folder configuration.
- Static IP configuration.
- Routing and device status.
- Connectivity tests.
- DNS resolution.
- Shared-folder access.
- Snapshot creation.

## 7. Safety Notes

Use official software sources wherever possible.

Do not expose credentials, private keys, personal files, or sensitive host information in public screenshots or repository commits.
