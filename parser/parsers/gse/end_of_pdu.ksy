meta:
  id: end_of_pdu
  file-extension: end_of_pdu
  endian: be
  
seq: 
  - id: frag_id
    type: u1
  - id: data
    size: _io.size-5
  - id: crc
    size: 4