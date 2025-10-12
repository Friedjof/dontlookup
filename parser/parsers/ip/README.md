# IPv4 Packet Parser (`ip_variants`)



This directory contains the Kaitai Struct definition (`ipv4_packet.ksy`) and the Python parsing code for IPv4 network packets.



## Sanity Checks and Validation Rules



To ensure parsed data strictly adheres to the IPv4 protocol specification (RFC 791), several **validation rules** are embedded directly into the `ipv4_packet.ksy` definition using the `valid` attribute. If a parsed field violates these rules, a `ValidationExprError` (or equivalent in other target languages) will be raised during parsing, indicating a malformed or unexpected packet.



Here are the key sanity checks implemented:



### `version` Field



* **Rule:** `valid: 0x04`

* **Description:** The first 4 bits of the IPv4 header must always be `0x04` (binary `0100`). This value uniquely identifies the packet as an IPv4 packet.



### `ihl` (Internet Header Length) Field



* **Rule:** `valid: _ >= 5`

* **Description:** This 4-bit field specifies the length of the IPv4 header in 32-bit (4-byte) words. It must be greater than or equal to 5 (the minimum length of an IPv4 header is 20 bytes).



### `total_length` Field



* **Rule:** `valid: _ >= ihl_bytes`

* **Description:** This 16-bit field specifies the total length of the IPv4 packet (header + data) in bytes. It must always be greater than or equal to the calculated header length (`ihl_bytes`).



## Recompiling the Parser



If you make changes to the `ipv4_packet.ksy` definition (e.g., adding more validation rules, modifying field definitions, or defining new types), you'll need to recompile the Python parser to reflect those changes.



To recompile `ipv4_packet.py` from `ipv4_packet.ksy`, ensure you are in this directory (`parsers/ip_variants/`) in your terminal and run the following command:



```bash

kaitai-struct-compiler -t python ipv4_packet.ksy

```