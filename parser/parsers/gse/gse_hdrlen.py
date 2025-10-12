# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import end_of_pdu
import whole_pdu
import start_of_pdu
import middle_of_pdu
class GseHdrlen(KaitaiStruct):

    class Se(Enum):
        middle = 0
        end = 1
        start = 2
        whole = 3
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.start_and_end_indicators = KaitaiStream.resolve_enum(GseHdrlen.Se, self._io.read_bits_int_be(2))
        self.label_type_indicator = self._io.read_bits_int_be(2)
        self.gse_length = self._io.read_bits_int_be(12)
        self._io.align_to_byte()
        if not (self.is_padding):
            _on = self.start_and_end_indicators
            if _on == GseHdrlen.Se.end:
                self._raw_payload = self._io.read_bytes((self.gse_length - 2))
                _io__raw_payload = KaitaiStream(BytesIO(self._raw_payload))
                self.payload = end_of_pdu.EndOfPdu(_io__raw_payload)
            elif _on == GseHdrlen.Se.start:
                self._raw_payload = self._io.read_bytes((self.gse_length - 2))
                _io__raw_payload = KaitaiStream(BytesIO(self._raw_payload))
                self.payload = start_of_pdu.StartOfPdu(self.label_type_indicator, _io__raw_payload)
            elif _on == GseHdrlen.Se.whole:
                self._raw_payload = self._io.read_bytes((self.gse_length - 2))
                _io__raw_payload = KaitaiStream(BytesIO(self._raw_payload))
                self.payload = whole_pdu.WholePdu(self.label_type_indicator, _io__raw_payload)
            elif _on == GseHdrlen.Se.middle:
                self._raw_payload = self._io.read_bytes((self.gse_length - 2))
                _io__raw_payload = KaitaiStream(BytesIO(self._raw_payload))
                self.payload = middle_of_pdu.MiddleOfPdu(_io__raw_payload)
            else:
                self.payload = self._io.read_bytes((self.gse_length - 2))


    @property
    def is_whole(self):
        if hasattr(self, '_m_is_whole'):
            return self._m_is_whole

        self._m_is_whole = self.start_and_end_indicators == GseHdrlen.Se.whole
        return getattr(self, '_m_is_whole', None)

    @property
    def is_middle(self):
        if hasattr(self, '_m_is_middle'):
            return self._m_is_middle

        self._m_is_middle = self.start_and_end_indicators == GseHdrlen.Se.middle
        return getattr(self, '_m_is_middle', None)

    @property
    def is_padding(self):
        if hasattr(self, '_m_is_padding'):
            return self._m_is_padding

        self._m_is_padding =  ((self.start_and_end_indicators == GseHdrlen.Se.middle) and (self.label_type_indicator == 0) and (self.gse_length == 0)) 
        return getattr(self, '_m_is_padding', None)

    @property
    def is_end(self):
        if hasattr(self, '_m_is_end'):
            return self._m_is_end

        self._m_is_end = self.start_and_end_indicators == GseHdrlen.Se.end
        return getattr(self, '_m_is_end', None)

    @property
    def is_start(self):
        if hasattr(self, '_m_is_start'):
            return self._m_is_start

        self._m_is_start = self.start_and_end_indicators == GseHdrlen.Se.start
        return getattr(self, '_m_is_start', None)


