meta:
  id: tls_1_3_server_change_server_spec_key
  endian: be
seq:
  - id: record_header
    type: record_header
types: 
  record_header:
    seq: 
      - id: change_cipher_spec_record
        contents: 
        - 0x14
      - id: protocol_version
        contents: 
        - 0x03
        - 0x03
      - id: record_payload_length
        contents:
        - 0x00
        - 0x01
      - id: payload
        contents:
        - 0x01
      