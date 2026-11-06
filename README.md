# NetworkWalks — Cybersecurity Lab Environment Setup

![Project](https://img.shields.io/badge/NetworkWalks-B084N-blue)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-purple)
![Virtualization](https://img.shields.io/badge/Virtualization-VirtualBox-orange)
![Status](https://img.shields.io/badge/Kali%20Setup-Verified-success)

**Batch ID:** B084N
**Project:** Week 1 — Project Module 1
**Module:** Cybersecurity Lab Environment Setup
**Current scope:** Kali Linux base lab configuration

## 1. Overview

This project documents the setup, configuration, and verification of a cybersecurity practical laboratory using Oracle VirtualBox and Kali Linux.

The objective is to establish a controlled virtual environment that can be used for authorized cybersecurity exercises, network analysis, vulnerability assessment, and further practical lab activities.

The repository includes technical documentation, configuration details, verification results, and screenshot evidence.

## 2. Objectives

- Install and configure Oracle VirtualBox.
- Configure a Kali Linux virtual machine.
- Create a VirtualBox NAT Network.
- Configure a static IPv4 address.
- Verify gateway connectivity and internet access.
- Verify DNS resolution.
- Configure VirtualBox shared-folder integration.
- Enable bidirectional clipboard and drag-and-drop settings.
- Create a clean baseline VM snapshot.
- Maintain reproducible technical documentation and evidence.

## 3. Lab Architecture

| Component | Configuration |
|---|---|
| Host operating system | Windows 11 |
| Hypervisor | Oracle VirtualBox 7.2.8 |
| Guest operating system | Kali Linux 2026.3 |
| VM memory | 2048 MB |
| Virtual CPUs | 2 |
| Video memory | 128 MB |
| Network mode | NAT Network |
| NAT Network name | NetworkWalks-NAT |
| Network subnet | 10.0.0.0/24 |
| Kali IPv4 address | 10.0.0.2/24 |
| Default gateway | 10.0.0.1 |
| DNS server | 8.8.8.8 |
| Shared folder mount | /downloads |

## 4. Network Configuration

The lab uses a VirtualBox NAT Network named `NetworkWalks-NAT`.

| Parameter | Value |
|---|---|
| Network address | 10.0.0.0/24 |
| Gateway | 10.0.0.1 |
| Kali address | 10.0.0.2/24 |
| DHCP | Disabled |
| DNS | 8.8.8.8 |

The static IP configuration allows the Kali VM to retain a predictable address for subsequent lab activities.

The NAT Network provides connectivity through VirtualBox NAT. It should not be treated as a complete security-isolation boundary.

## 5. Repository Structure

```text
NETWORKWALKS-B084N-WK1-PM1-CYBERSECURITY-LAB-SETUP/
│
├── README.md
├── .gitignore
│
├── docs/
│   ├── 01-objectives.md
│   ├── 02-prerequisites.md
│   ├── 03-virtualbox-setup.md
│   ├── 04-kali-configuration.md
│   ├── 05-network-configuration.md
│   ├── 06-verification.md
│   └── 07-troubleshooting.md
│
├── evidence/
│   ├── screenshots/
│   │   └── kali/
│   ├── staging/
│   └── verification-outputs/
│
├── reports/
├── assets/
└── scripts/
```

Raw evidence staging files and local contact sheets are retained locally and excluded from publication.

## 6. Verification Summary

The following checks were completed:

| Test | Result |
|---|---|
| VirtualBox installation | Verified |
| Kali VM configuration | Verified |
| NAT Network configuration | Verified |
| Static IPv4 configuration | Verified |
| Default gateway connectivity | Passed |
| External IP connectivity | Passed |
| DNS resolution | Passed |
| Shared-folder access | Passed |
| Baseline snapshot | Created |
| Clipboard setting | Bidirectional enabled |
| Drag-and-drop setting | Bidirectional enabled |

### Connectivity results

- Gateway: `10.0.0.1` — 4/4 replies.
- External IP: `8.8.8.8` — 4/4 replies.
- Packet loss: 0% in both recorded ping tests.
- DNS lookup for `google.com` completed successfully using `8.8.8.8`.

Clipboard and drag-and-drop were configured as bidirectional settings. A separate functional transfer test was not recorded.

## 7. Evidence

Screenshot evidence for the Kali setup is available under:

`evidence/screenshots/kali/`

The evidence set covers VirtualBox version, NAT Network configuration, VM hardware, network adapter, integration settings, IP configuration, routing, connectivity, DNS, shared-folder access, and snapshot creation.

## 8. Current Project Status

**Kali Linux base setup: completed and verified.**

Additional planned practical modules:

- Android-x86 virtual machine configuration.
- Windows 10 virtual machine configuration.
- Inter-VM connectivity testing.
- Wireshark browser-based practical labs.

These activities will be documented separately after completion. They are not claimed as completed in this repository at this stage.

## 9. Disclaimer

This repository is intended exclusively for educational and authorized cybersecurity lab activities.

All testing must be performed in controlled environments or on systems for which explicit permission has been granted.
