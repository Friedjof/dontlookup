README
Custom protocol, 1028 byte packet

Carried over UDP

- 0x0003 “magic bytes”
- 2 byte sequence counter
- 1024 byte payload (multiple of 8)

Parser will reassemble payloads in order. 

```bash
kaitai-struct-compiler -t python udp_1028.ksy
```

NOTE: This is probably TFTP with a 1024 byte block size. See the Data Format in RFC 1350.  