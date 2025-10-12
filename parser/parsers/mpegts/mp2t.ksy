meta:
  id: mp2t
  file-extension: mp2t
  endian: be
doc: |
  This version of MPEG-TS is implemented directly from ETSI documentation. 
seq:
  - id: transport_packet
    type: transport_packet
    size: 188
types:
  program_association_section:
    seq:
      - id: table_id
        type: b8
      - id: section_syntax_indicator
        type: b1
      - id: zero
        type: b1
      - id: reserved
        type: b2
      - id: section_length
        type: b12
      - id: transport_stream_id
        type: b16
      - id: version_number
        type: b5
      - id: current_next_indicator
        type: b1
      - id: section_number
        type: b8
      - id: last_section_number
        type: b8
      - id: program_number
        type: b16
      - id: program_number_reserved
        type: b3
  transport_packet:
    seq:
      - id: sync_byte
        contents:
        - 0x47
      - id: transport_error_indicator
        type: b1
      - id: payload_unit_start_indicator
        type: b1
      - id: transport_priority
        type: b1
      - id: pid
        type: b13
      - id: transport_scrambling_control
        type: b2
        enum: transport_scrambling_control
      - id: adaptation_field_control
        type: b2
      - id: continuity_counter
        type: b4
      - id: adaptation_field
        type: adaptation_field
        if: adaptation_field_control == 0b11 or adaptation_field_control == 0b10
      - id: program_association_section
        type: program_association_section
        if: pid == 0
      - id: payload
        size-eos: true 
    enums:
      transport_scrambling_control:
        0: no_scrambling
        1: reserved_for_future_use
        2: ts_packet_scrambled_with_even_key
        3: ts_packet_scrambled_with_odd_key
      pes_scrambling_control:
        0: no_scrambling
        1: reserved_for_future_use
        2: pes_packet_scrambled_with_even_key 
        3: pes_packet_scrambled_with_odd_key
      
  adaptation_field: 
    seq: 
      - id: adaptation_field_length
        type: b8
      - id: adaptation_field_entries
        size: adaptation_field_length
  adaptation_field_entries: 
    seq: 
      - id: discontinuity_indicator
        type: b1
      - id: random_access_indicator
        type: b1
      - id: stream_indicator
        type: b1
      - id: pcr_flag
        type: b1
      - id: opcr_flag
        type: b1
      - id: splicing_point_flag
        type: b1
      - id: transport_private_data_flag
        type: b1
      - id: adaptation_field_extension_flag
        type: b1
      - id: stuffing
        size-eos: true
  scrambling_descriptor:
    seq:
      - id: descriptor_tag
        type: b8
      - id: descriptor_length
        type: b8
      - id: scrambling_mode
        type: b8
        enum: scrambling_mode
    enums:
      scrambling_mode:
        0: reserved_for_future_use
        1: dvb_csa_v1
        2: dvb_csa_v2
        3: dvb_csa_v3_standard_mode
        4: dvb_csa_v3_minimally_enhanced_mode
        5: dvb_csa_v3_fully_enhanced_mode
        