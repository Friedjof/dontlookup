# DVB-S2 Baseband Frame Parser (`dvbs2_parser`)

This directory contains the Kaitai Struct definition (`dvbs2.ksy`) and Python parsing code for DVB-S2 Baseband (BB) frames, based on **ETSI EN 302 307-1 V1.4.1**. The Baseband Header is defined in **Section 5.1.6**.

## Validation Rules

`dvbs2.ksy` includes `valid` attributes to ensure parsed data adheres to the DVB-S2 standard. Violations will raise a `ValidationExprError`.

* **`UPL` (User Packet Length):** Must be a multiple of 8 (`upl % 8 == 0`).
* **`DFL` (Data Field Length):** Must be greater than 0, less than or equal to 58112, and a multiple of 8 (`dfl > 0 and dfl <= 58112 and dfl % 8 == 0`).

## Recompiling the Parser

If you change `dvbs2.ksy`, recompile the Python parser from this directory (`parsers/dvbs2/`):

```bash
kaitai-struct-compiler -t python dvbs2.ksy
```