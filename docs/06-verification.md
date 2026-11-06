# 06 — Verification and Evidence

## 1. Purpose

This document records the checks performed after configuring the Kali Linux virtual machine and its network environment.

Results below reflect the observed lab configuration and command outputs.

## 2. Verification Summary

| No. | Verification | Result |
|---:|---|---|
| 1 | VirtualBox version | Verified |
| 2 | NAT Network | Verified |
| 3 | Kali motherboard settings | Verified |
| 4 | Kali processor settings | Verified |
| 5 | Kali display settings | Verified |
| 6 | Network adapter | Verified |
| 7 | Clipboard and drag-and-drop settings | Enabled |
| 8 | Shared-folder configuration | Verified |
| 9 | Static IP configuration | Verified |
| 10 | IP routing and interface status | Verified |
| 11 | Gateway and external connectivity | Passed |
| 12 | DNS resolution | Passed |
| 13 | Shared-folder file access | Passed |
| 14 | Baseline snapshot | Created |

## 3. Network Test Results

### 3.1 Interface Address

Command:

```bash
ip -br addr
```

Observed IPv4 address:

`10.0.0.2/24`

Interface:

`eth0`

### 3.2 Routing Table

Command:

```bash
ip route
```

Observed default route:

`default via 10.0.0.1 dev eth0`

### 3.3 Gateway Ping

Command:

```bash
ping -c 4 10.0.0.1
```

Result:

- 4/4 packets received.
- 0% packet loss.

### 3.4 External IP Ping

Command:

```bash
ping -c 4 8.8.8.8
```

Result:

- 4/4 packets received.
- 0% packet loss.

### 3.5 DNS Resolution

Command:

```bash
nslookup google.com
```

Result:

- DNS server: 8.8.8.8.
- DNS lookup successful.
- IPv4 and IPv6 records returned.

## 4. Shared Folder Verification

The Windows host test file:

`shared-folder-test.txt`

was visible inside Kali under:

`/downloads`

The file content was successfully read:

```text
NetworkWalks shared-folder test
```

The `vboxsf` module and group membership were also checked.

## 5. Integration Settings

The VirtualBox shared clipboard and drag-and-drop options were configured as Bidirectional.

A separate end-to-end transfer test was not recorded. Therefore, only the configuration is marked verified.

## 6. Snapshot Verification

Snapshot:

`NetworkWalks-Kali-Base-Setup`

The snapshot was created after the base configuration and verification steps.

## 7. Screenshot Evidence Inventory

Location:

`evidence/screenshots/kali/`

| Evidence ID | Filename | Description |
|---|---|---|
| K01 | K01-virtualbox-version.jpeg | VirtualBox version |
| K02 | K02-nat-network.png | NAT Network settings |
| K03a | K03a-kali-motherboard.jpeg | VM motherboard settings |
| K03b | K03b-kali-processor.png | VM processor settings |
| K03c | K03c-kali-display.png | VM display settings |
| K04 | K04-kali-network-adapter.png | Kali network adapter |
| K05 | K05-clipboard-dragdrop.jpeg | Clipboard and drag-and-drop settings |
| K06 | K06-shared-folder-configuration.png | Shared-folder configuration |
| K07 | K07-static-ip-configuration.png | Static IP configuration |
| K08 | K08-ip-route-device-status.png | Interface and routing status |
| K09-K10 | K09-K10-connectivity-tests.png | Gateway and external connectivity |
| K11 | K11-dns-resolution.png | DNS resolution |
| K12 | K12-shared-folder-access.png | Shared-folder access |
| K13 | K13-kali-base-snapshot.png | Baseline snapshot |

The evidence set contains 14 image files because K03 is represented by three screenshots and K09/K10 share one combined screenshot.

## 8. Pending Verification

The following activities are outside the completed Kali base setup:

- Android-x86 deployment and connectivity.
- Windows 10 deployment and connectivity.
- Inter-VM communication.
- Wireshark practical exercises.

These will be documented after the corresponding tests are completed.
