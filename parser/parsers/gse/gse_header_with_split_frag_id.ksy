meta:
  id: gse_header_with_split_frag_id
  file-extension: gse_header_with_split_frag_id
  endian: be
  imports:
    - start_of_pdu_with_split_frag_id
    - middle_of_pdu_with_split_frag_id
    - end_of_pdu_with_split_frag_id
    - whole_pdu
seq:
  - id: start_and_end_indicators
    type: b2
    enum: se
  - id: label_type_indicator
    type: b2
  - id: gse_length
    type: b12
  - id: payload
    size: gse_length-2
    if: not is_padding
    type:
      switch-on: start_and_end_indicators
      cases:
        'se::start': start_of_pdu_with_split_frag_id(label_type_indicator)
        'se::middle': middle_of_pdu_with_split_frag_id
        'se::end': end_of_pdu_with_split_frag_id
        'se::whole': whole_pdu(label_type_indicator)
instances:
  is_padding:
    value: start_and_end_indicators == se::middle and (label_type_indicator == 0b00) and (gse_length == 0x000)
enums:
  se:
    0: middle
    1: end
    2: start
    3: whole