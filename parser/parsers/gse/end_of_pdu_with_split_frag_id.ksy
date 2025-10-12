meta:
  id: end_of_pdu_with_split_frag_id
  file-extension: end_of_pdu_with_split_frag_id
  endian: be
  
seq: 
  - id: frag_id
    type: b6
  - id: counter
    type: b2
  - id: data
    size: _io.size-5
  - id: crc
    size: 4