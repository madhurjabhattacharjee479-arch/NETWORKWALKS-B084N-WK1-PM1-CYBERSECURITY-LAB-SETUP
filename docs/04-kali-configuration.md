# 04 — Kali Linux Configuration

## 1. Guest Operating System

The configured guest operating system is Kali Linux 2026.3.

The VirtualBox VM name retains the downloaded image's older 2026.1 naming convention.

## 2. VM Hardware

| Component | Configuration |
|---|---|
| Base memory | 2048 MB |
| Virtual CPUs | 2 |
| Video memory | 128 MB |
| 3D acceleration | Disabled |
| Network adapter | PCnet-FAST III |
| Network mode | NAT Network |

## 3. Network Interface

The primary network interface is:

`eth0`

The static IPv4 address assigned to the interface is:

`10.0.0.2/24`

The connection profile used is:

`Wired connection 1`

## 4. Static Network Configuration

The following NetworkManager commands were used:

```bash
sudo nmcli connection modify "Wired connection 1" \
  ipv4.method manual \
  ipv4.addresses 10.0.0.2/24 \
  ipv4.gateway 10.0.0.1 \
  ipv4.dns 8.8.8.8
```

The connection was restarted:

```bash
sudo nmcli connection down "Wired connection 1"
sudo nmcli connection up "Wired connection 1"
```

## 5. Shared Folder Integration

The host shared folder is mounted at:

`/downloads`

The guest was checked for the VirtualBox shared-folder module:

```bash
lsmod | grep vboxsf
```

The user group membership was checked with:

```bash
groups
```

The `vboxsf` group was present.

A test file created on the Windows host was accessible from Kali:

```bash
ls -la /downloads
cat /downloads/shared-folder-test.txt
```

Expected test-file content:

```text
NetworkWalks shared-folder test
```

The content was successfully read from the guest.

## 6. Clipboard and Drag-and-Drop

VirtualBox General > Advanced settings:

| Feature | Setting |
|---|---|
| Shared clipboard | Bidirectional |
| Drag and drop | Bidirectional |

These settings were enabled. No separate end-to-end transfer test is claimed.

## 7. Snapshot

The following baseline snapshot was created:

`NetworkWalks-Kali-Base-Setup`

This provides a recovery point before additional lab changes.
