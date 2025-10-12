# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dvbs2(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.matype = Dvbs2.Matype(self._io, self, self._root)
        self.upl = self._io.read_u2be()
        _ = self.upl
        if not (self.upl % 8) == 0:
            raise kaitaistruct.ValidationExprError(self.upl, self._io, u"/seq/1")
        self.dfl = self._io.read_u2be()
        _ = self.dfl
        if not  ((self.dfl > 0) and (self.dfl <= 58112) and ((self.dfl % 8) == 0)) :
            raise kaitaistruct.ValidationExprError(self.dfl, self._io, u"/seq/2")
        self.sync = self._io.read_u1()
        self.syncd = self._io.read_u2be()
        self.crc_8 = self._io.read_u1()
        self.data_field = self._io.read_bytes(self.dfl // 8)

    class Matype(KaitaiStruct):

        class TransmissionRolloffFactor(Enum):
            thirty_five = 0
            twenty_five = 1
            twenty = 2
            reserved = 3

        class InputStreams(Enum):
            multiple = 0
            single = 1

        class Modulation(Enum):
            acm = 0
            ccm = 1

        class SyncIndicator(Enum):
            inactive = 0
            active = 1

        class NullPacketDeletion(Enum):
            inactive = 0
            active = 1

        class InputStreamFormat(Enum):
            generic_packetized = 0
            generic_continuous = 1
            reserved = 2
            transport = 3
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ts_gs = KaitaiStream.resolve_enum(Dvbs2.Matype.InputStreamFormat, self._io.read_bits_int_be(2))
            self.sis_mis = KaitaiStream.resolve_enum(Dvbs2.Matype.InputStreams, self._io.read_bits_int_be(1))
            self.ccm_acm = KaitaiStream.resolve_enum(Dvbs2.Matype.Modulation, self._io.read_bits_int_be(1))
            self.issyi = KaitaiStream.resolve_enum(Dvbs2.Matype.SyncIndicator, self._io.read_bits_int_be(1))
            self.npd = KaitaiStream.resolve_enum(Dvbs2.Matype.NullPacketDeletion, self._io.read_bits_int_be(1))
            self.ro = KaitaiStream.resolve_enum(Dvbs2.Matype.TransmissionRolloffFactor, self._io.read_bits_int_be(2))
            if self.sis_mis == Dvbs2.Matype.InputStreams.multiple:
                self.input_stream_identifier = self._io.read_bits_int_be(8)

            if self.sis_mis == Dvbs2.Matype.InputStreams.single:
                self.reserved = self._io.read_bits_int_be(8)




