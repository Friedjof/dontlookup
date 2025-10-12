meta:
  id: ipv4_packet
  title: IPv4 network packet
  endian: be
seq:
  - id: version 
    type: b4
    valid: 0x04
  - id: ihl
    type: b4
    valid: 
      expr: _ >= 5
  - id: dscp
    type: b6
  - id: ecn
    type: b2
  - id: total_length
    type: u2
    valid: 
      expr: _ >= ihl_bytes
  - id: identification
    type: u2
  - id: flags
    type: b3
  - id: fragment_offset
    type: b13
  - id: ttl
    type: b8
  - id: protocol
    type: b8
  - id: header_checksum
    type: b16
  - id: src_address
    size: 4
  - id: dst_address
    size: 4
  - id: options
    size: ihl_bytes-20
  - id: body
    size: total_length-ihl_bytes
instances: 
  ihl_bytes:
    value: ihl*4