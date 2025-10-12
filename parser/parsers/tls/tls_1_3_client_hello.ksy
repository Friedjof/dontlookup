meta:
  id: tls_1_3_client_hello
  endian: be
seq:
  - id: record_header
    type: record_header
  - id: handshake_header
    type: handshake_header
  - id: client_version
    contents: 
    - 0x03
    - 0x03
  - id: client_random
    size: 32
  - id: session_id
    size: 1
  - id: cipher_suites
    type: cipher_suites
  - id: compression_methods
    type: compression_methods
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
        - 0x01
      - id: handshake_message_length
        type: u2
  handshake_header:
    seq:
      - id: client_hello
        contents:
        - 0x01
        - 0x00
        - 0x00
        - 0xa1
  cipher_suites:
    seq:
      - id: cipher_suite_length
        type: u2
      - id: cipher_suites_list
        size: cipher_suite_length
  compression_methods:
    seq:
      - id: compression_method_length
        type: u1
      - id: compression_methods_list
        size: compression_method_length