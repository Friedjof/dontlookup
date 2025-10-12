meta:
  id: tls_1_3_server_hello
  endian: be
seq:
  - id: record_header
    type: record_header
  - id: handshake_header
    type: handshake_header
  - id: server_version
    contents:
     - 0x03
     - 0x03
  - id: server_random
    size: 32
  - id: session_id
    type: session_id
  - id: cipher_suite
    type: u2
  - id: compression_method
    type: u1
  - id: extensions_length
    type: u2
  - id: extensions
    size: extensions_length
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
      - 0x02
    - id: b0
      contents:
      - 0x00
    - id: server_hello_data_len
      type: u2
  session_id:
    seq:
      - id: session_id_length
        contents:
          - 0x20
      - id: session_id_client_hello
        size: 0x20