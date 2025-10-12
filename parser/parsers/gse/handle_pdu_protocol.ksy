meta:
  id: handle_pdu_protocol
  file-extension: handle_pdu_protocol
  endian: be
params: 
  - id: protocol_type
    type: b16
seq: 
  - id: protocol
    type: 
      switch-on: protocol_type
      cases:
        2: three_byte_npa
        _: do_nothing

types:
  ule_extension_header:
    seq:
      - id: zero_prefix
        type: b5
        valid: 0b00000
      - id: h_len
        type: b3
      - id: h_type
        type: b8
  bridged_sndu_header_with_npa:
    seq:
      - id: d
        type: b1
      - id: length
        type: b15
      - id: type
        type: b16
        valid: 0x001
      - id: dest_npa
        size: 6
        if: d
      - id: dest_mac
        size: 6
      - id: src_mac
        size: 6
      - id: ethertype_llc_len
        size: 2
      - id: payload
        size: length
      - id: crc
        size: 4
  ts_concat:
    seq: 
      - id: d
        type: b1
      - id: length
        type: b15
      - id: type
        type: b16
        valid: 0x0002
      - id: dest_npa
        size: 6
      - id: payload
        size: length
      - id: crc
        size: 4
  six_byte_npa:
    seq:
      - id: npa
        size: 6
  three_byte_npa:
    seq:
      - id: npa
        size: 3
  do_nothing:
    seq: []