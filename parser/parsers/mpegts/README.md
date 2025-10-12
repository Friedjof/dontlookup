# MPEG-TS Packet Parsers (`mpegts_variants`)

This directory contains the Kaitai Struct definition (`mp2t.ksy`) for the base MPEG Transport Stream (MPEG-TS) protocol, along with Python parsing code for different stream types.

## Overview

### `mpegts_parser.py` (Standard MPEG-TS)
This parser uses `mp2t.ksy` and expects a **`0x47` sync byte** at the start of every 188-byte packet.

### `crc_parser.py` (DVB-S2 Compatible MPEG-TS)
This specialized parser also uses `mp2t.ksy` but handles an alternate MPEG-TS format. Here, the traditional `0x47` sync byte position is **repurposed for a CRC** (Cyclic Redundancy Check) over the 187 bytes of the *previous* MPEG-TS frame. This implementation is designed to support specific DVB-S2 DVB-S compatibility modes (see **Section 5.1.4 of ETSI EN 302 307-1 V1.4.1**).

**Important Note for `crc_parser.py`:** Be extremely careful when using this parser. It will only perform as expected if the start of the user packet stream is **not exactly aligned** with the beginning of the provided capture.

### `newtec_crc_parser.py` (MPEG-TS over DVB-S2)
This is a specialized parser that matches the Newtec MDM2510 implementation DVB-S2 and DVB-S compatability. See **Section 5.1.4 of ETSI EN 302 307-1 V1.4.1**
## Validation & Sanity Checks

While `mp2t.ksy` handles basic structural validation, specific sync byte and checksum validation is managed within the Python parsers:

* **`mpegts_parser.py`:** Explicitly checks for a **`0x47` sync byte**.
* **`crc_parser.py`:** Computes and validates the **CRC** in the sync byte position.

Violations result in parsing errors, indicating malformed packets.

## Recompiling the Parser

If you change `mp2t.ksy`, you'll need to recompile the Python parser. Ensure you're in this directory (`parsers/mpegts_variants/`) and run:

```bash
kaitai-struct-compiler -t python mp2t.ksy
```