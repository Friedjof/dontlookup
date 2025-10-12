# GSE Packet Parsers (`gse_variants`)

This directory contains multiple Kaitai Struct definitions (`.ksy` files) and their auto-generated Python parsing code for various GSE (Generic Stream Encapsulation) packet variants. These parsers are designed to handle different structures of GSE packets, as defined primarily by ETSI documentation.

## Overview of GSE Variants

This directory contains schemas for the following GSE packet variants, each with specific characteristics:

* **`gse_standard.ksy`**:
    * **Description:** Implemented directly from ETSI documentation. This is likely the base or standard GSE format.
* **`gse_standard_split.ksy`**:
    * **Description:** A variation of the standard GSE where the `fragment_id` field has been logically divided into a 6-bit `fragment_id` and a 2-bit `continuity_counter`. This allows for more granular tracking of fragment continuity.
* **`gse_hdrlen.ksy`**:
    * **Description:** Differs from the standard in how length is interpreted. The `gse_length` field specifies the size of the following PDU (Protocol Data Unit) *only*, rather than the size of the whole GSE packet (including its header).
* **`gse_hdrlen_unsafe.ksy`**:
    * **Description:** Builds upon `gse_hdrlen.ksy` with two major changes: the `gse_length` field again refers to the PDU size, and it explicitly ignores the label type indicator. This makes it more "failsafe" or permissive, accepting some GSE packets that might otherwise be discarded due to label type mismatches.
* **`gse_hdrlen_split.ksy`**:
    * **Description:** Combines features from `gse_hdrlen.ksy` and `gse_standard_split.ksy`. Here, the `gse_length` field denotes PDU size, and the `fragment_id` field is split into a 6-bit `fragment_id` and a 2-bit `continuity_counter`.


## Sanity Checks and Validation Rules

To ensure parsed GSE data adheres to its specific variant's protocol specification, **validation rules** are (or can be) embedded directly into the `.ksy` definitions using the `valid` attribute. If a parsed field violates these rules, a `ValidationExprError` (or equivalent in other target languages) will be raised during parsing, indicating a malformed or unexpected packet.

**Note:** The precise `valid` expressions depend on the detailed `seq` definitions within each specific `.ksy` file. Below are common types of sanity checks applicable to GSE packets:

### Fixed Header Fields / Type Identifiers

* **Potential Rule Type:** `valid: 0xXX`
* **Description:** Many GSE variants might start with a fixed byte or bit pattern (e.g., a specific protocol type, version, or label type indicator) to uniquely identify that particular variant or its characteristics. Validation ensures this initial identifier matches the expected value for the schema being used.

### Length Fields (e.g., `gse_length`, `pdu_length`, `payload_length`)

* **Potential Rule Type:** `valid: _ >= minimum_expected_value` or `valid: _ <= maximum_allowed_value`
* **Description:** Critical for preventing buffer overruns and ensuring data integrity.
    * Validation ensures the reported length of the PDU or payload is always greater than or equal to any fixed header components following the length field.
    * It might also enforce a maximum size constraint based on the typical MTU or theoretical limits.
    * For `gse_hdrlen` and `gse_hdrlen_split` variants, the `gse_length` is explicitly stated to refer to the PDU size, and validation should account for this interpretation.

### Flags / Control Bits (e.g., Start/End of PDU, Last Fragment)

* **Potential Rule Type:** `valid: _ == 0bXXXX` or `valid: (_field_a and not _field_b)`
* **Description:** GSE relies heavily on flags (like SOP - Start of PDU, EOP - End of PDU) to delineate PDUs fragmented across multiple GSE packets. Validation can ensure:
    * Mutually exclusive flags are not simultaneously set (e.g., SOP and EOP flags are consistent for middle fragments).
    * Expected flag combinations for specific PDU types (e.g., a "Whole PDU" variant must have both SOP and EOP set).

### Checksums / CRCs (e.g., `crc32`, `crc32mpeg2`)

* **Description:** GSE often includes a CRC or checksum field (like `crc32mpeg2`) for error detection. While Kaitai Struct parses this field, the actual validation involves recalculating the checksum over the relevant data (e.g., the entire GSE packet including header and payload, up to the CRC field) and comparing it to the parsed value. This complex calculation is typically performed in the post-parsing Python code using a dedicated utility function (like one from `parser_utils.py`).


## Recompiling the Parsers

If you make changes to any of the `.ksy` definitions within this directory (e.g., adding more validation rules, modifying field definitions, or defining new types), you'll need to recompile the corresponding Python parser(s) to reflect those changes.

To recompile a specific Python parser from its `.ksy` definition, ensure you are in this directory (`parsers/gse/`) in your terminal and run the following command for each `.ksy` file you've modified:

```bash
# Example for gse_standard.ksy:
kaitai-struct-compiler -t python gse_standard.ksy

# Example for gse_standard_split.ksy:
kaitai-struct-compiler -t python gse_standard_split.ksy

# ... and so on for gse_hdrlen.ksy, gse_hdrlen_unsafe.ksy, gse_hdrlen_split.ksy