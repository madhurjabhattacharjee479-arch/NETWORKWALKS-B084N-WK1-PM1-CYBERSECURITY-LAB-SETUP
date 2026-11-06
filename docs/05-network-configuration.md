# 05 — Network Configuration

## 1. Network Design

The lab uses a VirtualBox NAT Network.

| Parameter | Configuration |
|---|---|
| Network name | NetworkWalks-NAT |
| Network address | 10.0.0.0/24 |
| Gateway | 10.0.0.1 |
| Kali address | 10.0.0.2/24 |
| DHCP | Disabled |
| DNS | 8.8.8.8 |

## 2. NAT Network Creation

The NAT Network was created from the Windows host using VBoxManage:

```powershell
& $VBox natnetwork add `
    --netname "NetworkWalks-NAT" `
    --network "10.0.0.0/24" `
    --enable `
    --dhcp off
```

The network configuration was inspected with:

```powershell
& $VBox natnetwork list
```

The network was configured with DHCP disabled.

## 3. Kali Static IPv4 Configuration

The Kali network connection was configured using NetworkManager:

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

## 4. Interface Verification

Command:

```bash
ip -br addr
```

Recorded interface configuration:

```text
eth0    UNKNOWN    10.0.0.2/24
```

## 5. Routing Verification

Command:

```bash
ip route
```

Recorded routes:

```text
default via 10.0.0.1 dev eth0 proto static metric 100
10.0.0.0/24 dev eth0 proto kernel scope link src 10.0.0.2 metric 100
```

## 6. Gateway Connectivity

Command:

```bash
ping -c 4 10.0.0.1
```

Result:

- 4 packets transmitted.
- 4 packets received.
- 0% packet loss.
- Average round-trip time: approximately 0.752 ms.

## 7. External Connectivity

Command:

```bash
ping -c 4 8.8.8.8
```

Result:

- 4 packets transmitted.
- 4 packets received.
- 0% packet loss.
- Average round-trip time: approximately 45.137 ms.

## 8. DNS Resolution

Command:

```bash
nslookup google.com
```

The configured DNS server was `8.8.8.8`.

The lookup returned IPv4 and IPv6 address records.

## 9. Network Security Note

A VirtualBox NAT Network provides guest networking through NAT and allows connected VMs to communicate according to their network configuration.

It should not be described as a complete isolation or security boundary. Host firewall configuration and the behavior of connected guests remain relevant.
