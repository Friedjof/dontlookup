README
Custom protocol, 516 byte packet

Carried over UDP

- 0x0003 “magic bytes”
- 2 byte sequence counter
- 512 byte payload (multiple of 8)

Parser will reassemble payloads in order

```bash
kaitai-struct-compiler -t python udp_516.ksy
```

NOTE: This is probably TFTP with a 512 byte block size. See the Data Format in RFC 1350.