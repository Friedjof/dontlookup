meta:
  id: tls_1_3_wrapped_record
  endian: be
seq:
  - id: record_header
    type: record_header
types: 
  record_header:
    seq: 
      - id: application_data_record
        contents: 
        - 0x17
      - id: protocol_version
        contents: 
        - 0x03
        - 0x03
      - id: wrapped_data_length
        type: u2
      - id: payload
        size: wrapped_data_length
        