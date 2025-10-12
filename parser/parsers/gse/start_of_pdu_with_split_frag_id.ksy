meta:
  id: start_of_pdu_with_split_frag_id
  file-extension: start_of_pdu_with_split_frag_id
  endian: be
  imports: 
    - handle_pdu_protocol
params: 
  - id: label_type_indicator
    type: b2
seq: 
  - id: frag_id
    type: b6
  - id: counter
    type: b2
  - id: total_length
    type: u2
  - id: protocol_type
    type: b16
  - id: six_byte_label
    size: 6
    if: label_type_indicator == 0b00
  - id: three_byte_label
    size: 3
    if: label_type_indicator == 0b01
  - id: data_field
    type: handle_pdu_protocol(protocol_type)
  - id: data
    size-eos: true
enums:    
  lti: 
    0: six_byte_label
    1: three_byte_label
    2: broadcast
    3: label_reuse
