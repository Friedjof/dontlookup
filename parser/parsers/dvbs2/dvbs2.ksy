meta:
  id: dvbs2
  file-extension: dvbs2
  endian: be
  xref: |
    ETSI EN 302 307
seq:
  - id: matype
    type: matype
  - id: upl
    type: u2
    valid: 
      expr: upl % 8 == 0
  - id: dfl
    type: u2
    valid:
      # max: 58112
      expr: dfl > 0 and dfl <= 58112 and dfl % 8 == 0
  - id: sync
    type: u1
  - id: syncd
    type: u2
  - id: crc_8
    type: u1
  - id: data_field
    size: dfl / 8
types:
  matype:
    seq:
      - id: ts_gs
        type: b2
        enum: input_stream_format
      - id: sis_mis
        type: b1
        enum: input_streams
      - id: ccm_acm
        type: b1
        enum: modulation
      - id: issyi
        type: b1
        enum: sync_indicator
      - id: npd
        type: b1
        enum: null_packet_deletion
      - id: ro
        type: b2
        enum: transmission_rolloff_factor
      - id: input_stream_identifier
        type: b8
        if: sis_mis == input_streams::multiple
      - id: reserved
        type: b8
        if: sis_mis == input_streams::single
    enums:
      input_stream_format:
        0: generic_packetized
        1: generic_continuous
        2: reserved 
        3: transport
      input_streams:
        1: single
        0: multiple
      modulation:
        1: ccm
        0: acm
      sync_indicator:
        1: active
        0: inactive
      null_packet_deletion:
        1: active
        0: inactive
      transmission_rolloff_factor:
        0: thirty_five
        1: twenty_five
        2: twenty
        3: reserved
        
        