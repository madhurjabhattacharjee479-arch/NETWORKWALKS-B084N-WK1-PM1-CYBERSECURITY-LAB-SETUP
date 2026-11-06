# 03 — VirtualBox Setup

## 1. Hypervisor

Oracle VirtualBox was installed and verified on the Windows 11 host.

**Installed version:** 7.2.8r173730

## 2. Kali VM

The Kali Linux VirtualBox appliance was imported and configured.

| Setting | Configuration |
|---|---|
| VM name | kali-linux-2026.1-virtualbox-amd64 |
| Guest OS | Kali Linux 2026.3 |
| Base memory | 2048 MB |
| Processors | 2 |
| Video memory | 128 MB |
| 3D acceleration | Disabled |

The VM name reflects the downloaded image's older naming convention. The installed guest reports version 2026.3.

## 3. Network Adapter

The first network adapter was configured as follows:

| Parameter | Value |
|---|---|
| Adapter | Adapter 1 |
| Attached to | NAT Network |
| Network name | NetworkWalks-NAT |
| Adapter type | PCnet-FAST III (Am79C973) |
| Promiscuous mode | Deny |
| Cable connected | Enabled |

Other network adapters were disabled.

## 4. Shared Folder

The host directory was configured as a VirtualBox shared folder.

| Setting | Value |
|---|---|
| Host path | <host-shared-folder-directory> |
| Share name | Shared-Files |
| Guest mount point | /downloads |
| Auto-mount | Enabled |
| Permanent | Enabled |

The guest's `vboxsf` module was verified as loaded, and the Kali user was added to the `vboxsf` group.

A host-created test file was successfully read from the guest.

## 5. Integration Settings

The following VirtualBox integration options were enabled:

- Shared clipboard: Bidirectional.
- Drag and drop: Bidirectional.

These are configuration settings. A separate functional clipboard or drag-and-drop transfer test was not recorded.

## 6. Baseline Snapshot

Snapshot name:

`NetworkWalks-Kali-Base-Setup`

The snapshot preserves the configured Kali baseline before additional lab activities.

## 7. Evidence

Relevant screenshots are stored in:

`evidence/screenshots/kali/`

See the evidence inventory in `06-verification.md`.
