# 07 — Troubleshooting

## 1. Purpose

This document records useful diagnostic commands and troubleshooting guidance for the Kali Linux VirtualBox lab.

Only issues and solutions actually encountered should be described as completed fixes. The guidance below also includes general diagnostic procedures for future use.

## 2. Network Interface Not Showing Expected IP

Inspect interfaces:

```bash
ip -br addr
```

Inspect connection profiles:

```bash
nmcli connection show
```

Inspect active connections:

```bash
nmcli device status
```

Check the configured profile:

```bash
nmcli connection show "Wired connection 1"
```

If the connection is inactive, restart it:

```bash
sudo nmcli connection down "Wired connection 1"
sudo nmcli connection up "Wired connection 1"
```

## 3. Gateway Connectivity Failure

Check the routing table:

```bash
ip route
```

Check gateway reachability:

```bash
ping -c 4 10.0.0.1
```

Confirm:

- The VM network adapter is enabled.
- The adapter is attached to `NetworkWalks-NAT`.
- The NAT Network is enabled.
- The guest has the correct static IP.
- The default gateway is `10.0.0.1`.

## 4. Internet Connectivity Failure

First test the gateway:

```bash
ping -c 4 10.0.0.1
```

Then test an external IP:

```bash
ping -c 4 8.8.8.8
```

If the gateway works but the external IP does not, inspect the VirtualBox NAT Network configuration and host network connectivity.

## 5. DNS Resolution Failure

Inspect DNS configuration:

```bash
cat /etc/resolv.conf
```

Test DNS resolution:

```bash
nslookup google.com
```

The configured DNS server for this lab is:

`8.8.8.8`

## 6. Shared Folder Not Accessible

Check whether the VirtualBox shared-folder module is loaded:

```bash
lsmod | grep vboxsf
```

Check group membership:

```bash
groups
```

Check the mount directory:

```bash
ls -la /downloads
```

Confirm that the VirtualBox shared folder uses:

- Share name: `Shared-Files`
- Mount point: `/downloads`
- Auto-mount: enabled
- Permanent: enabled

If group membership has just changed, log out and log back in before testing again.

## 7. Clipboard or Drag-and-Drop Not Working

Inspect VirtualBox settings under:

**Settings > General > Advanced**

Check:

- Shared Clipboard: Bidirectional.
- Drag and Drop: Bidirectional.

These settings may depend on Guest Additions compatibility and the running guest session.

Enabling the settings alone does not prove that file transfer or clipboard synchronization works. Perform a separate functional test before claiming it is verified.

## 8. Low Host Memory

The host has 8 GB of RAM.

Running multiple virtual machines simultaneously can cause performance problems.

Recommended precautions:

- Run one resource-intensive guest at a time.
- Close unnecessary applications.
- Monitor host memory usage.
- Avoid increasing VM memory without checking available host resources.

## 9. General Diagnostic Commands

```bash
ip -br addr
ip route
nmcli device status
nmcli connection show
ping -c 4 10.0.0.1
ping -c 4 8.8.8.8
nslookup google.com
lsmod | grep vboxsf
groups
```

## 10. Documentation Practice

For every new issue:

1. Record the observed symptom.
2. Capture the relevant command output.
3. Identify the likely cause.
4. Apply one change at a time.
5. Repeat the relevant verification test.
6. Record the actual result.

Do not document a troubleshooting fix as successful unless the result has been verified.
