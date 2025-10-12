meta:
  id: tls_1_2_server_certificate
  endian: be
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
    - id: handshake_message
      # type: handshake_message
      size: handshake_message_length
types: 
  handshake_message: 
    seq: 
      - id: handshake_header
        type: handshake_header
      - id: certificate_list_length
        type: u3
      - id: certificate_data_length
        type: u3
      - id: certificate_data
        size-eos: true
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
        - 0x0b
      - id: certificate_message_length
        type: u3
  u3:
    seq:
      - id: high_byte
        type: u1
      - id: low_word
        type: u2
    instances:
      value:
        value: '(high_byte << 16) | low_word'