meta:
  id: tls_1_2_server_key_exchange
  endian: be
seq:
  - id: record_header
    type: record_header
  - id: handshake_header
    type: handshake_header
  - id: curve_info 
    type: curve_info
  - id: public_key_length
    contents:
    - 0x20
  - id: public_key
    size: public_key_length
    
types: 
  record_header:
    seq: 
      - id: handshake_record
        contents: 
        - 0x16
      - id: protocol_version
        contents: 
        - 0x03
        - 0x03
      - id: handshake_message_length
        type: u2
  handshake_header:
    seq:
      - id: handshake_message_type
        contents: 
        - 0x0c
      - id: server_key_exchange_length
        type: u3
  curve_info:
    seq:
      - id: named_curve
        contents:
        - 0x03
      - id: curve
        type: u1
  u3:
    seq:
      - id: high_byte
        type: u1
      - id: low_word
        type: u2
    instances:
      value:
        value: '(high_byte << 16) | low_word'