# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Mp2t(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_transport_packet = self._io.read_bytes(188)
        _io__raw_transport_packet = KaitaiStream(BytesIO(self._raw_transport_packet))
        self.transport_packet = Mp2t.TransportPacket(_io__raw_transport_packet, self, self._root)

    class AdaptationFieldEntries(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.discontinuity_indicator = self._io.read_bits_int_be(1) != 0
            self.random_access_indicator = self._io.read_bits_int_be(1) != 0
            self.stream_indicator = self._io.read_bits_int_be(1) != 0
            self.pcr_flag = self._io.read_bits_int_be(1) != 0
            self.opcr_flag = self._io.read_bits_int_be(1) != 0
            self.splicing_point_flag = self._io.read_bits_int_be(1) != 0
            self.transport_private_data_flag = self._io.read_bits_int_be(1) != 0
            self.adaptation_field_extension_flag = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.stuffing = self._io.read_bytes_full()


    class TransportPacket(KaitaiStruct):

        class TransportScramblingControl(Enum):
            no_scrambling = 0
            reserved_for_future_use = 1
            ts_packet_scrambled_with_even_key = 2
            ts_packet_scrambled_with_odd_key = 3

        class PesScramblingControl(Enum):
            no_scrambling = 0
            reserved_for_future_use = 1
            pes_packet_scrambled_with_even_key = 2
            pes_packet_scrambled_with_odd_key = 3
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sync_byte = self._io.read_bytes(1)
            if not self.sync_byte == b"\x47":
                raise kaitaistruct.ValidationNotEqualError(b"\x47", self.sync_byte, self._io, u"/types/transport_packet/seq/0")
            self.transport_error_indicator = self._io.read_bits_int_be(1) != 0
            self.payload_unit_start_indicator = self._io.read_bits_int_be(1) != 0
            self.transport_priority = self._io.read_bits_int_be(1) != 0
            self.pid = self._io.read_bits_int_be(13)
            self.transport_scrambling_control = KaitaiStream.resolve_enum(Mp2t.TransportPacket.TransportScramblingControl, self._io.read_bits_int_be(2))
            self.adaptation_field_control = self._io.read_bits_int_be(2)
            self.continuity_counter = self._io.read_bits_int_be(4)
            self._io.align_to_byte()
            if  ((self.adaptation_field_control == 3) or (self.adaptation_field_control == 2)) :
                self.adaptation_field = Mp2t.AdaptationField(self._io, self, self._root)

            if self.pid == 0:
                self.program_association_section = Mp2t.ProgramAssociationSection(self._io, self, self._root)

            self.payload = self._io.read_bytes_full()


    class AdaptationField(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.adaptation_field_length = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.adaptation_field_entries = self._io.read_bytes(self.adaptation_field_length)


    class ScramblingDescriptor(KaitaiStruct):

        class ScramblingMode(Enum):
            reserved_for_future_use = 0
            dvb_csa_v1 = 1
            dvb_csa_v2 = 2
            dvb_csa_v3_standard_mode = 3
            dvb_csa_v3_minimally_enhanced_mode = 4
            dvb_csa_v3_fully_enhanced_mode = 5
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.descriptor_tag = self._io.read_bits_int_be(8)
            self.descriptor_length = self._io.read_bits_int_be(8)
            self.scrambling_mode = KaitaiStream.resolve_enum(Mp2t.ScramblingDescriptor.ScramblingMode, self._io.read_bits_int_be(8))


    class ProgramAssociationSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.table_id = self._io.read_bits_int_be(8)
            self.section_syntax_indicator = self._io.read_bits_int_be(1) != 0
            self.zero = self._io.read_bits_int_be(1) != 0
            self.reserved = self._io.read_bits_int_be(2)
            self.section_length = self._io.read_bits_int_be(12)
            self.transport_stream_id = self._io.read_bits_int_be(16)
            self.version_number = self._io.read_bits_int_be(5)
            self.current_next_indicator = self._io.read_bits_int_be(1) != 0
            self.section_number = self._io.read_bits_int_be(8)
            self.last_section_number = self._io.read_bits_int_be(8)
            self.program_number = self._io.read_bits_int_be(16)
            self.program_number_reserved = self._io.read_bits_int_be(3)



