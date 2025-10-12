# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Ipv4Packet(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.version = self._io.read_bits_int_be(4)
        if not self.version == 4:
            raise kaitaistruct.ValidationNotEqualError(4, self.version, self._io, u"/seq/0")
        self.ihl = self._io.read_bits_int_be(4)
        _ = self.ihl
        if not _ >= 5:
            raise kaitaistruct.ValidationExprError(self.ihl, self._io, u"/seq/1")
        self.dscp = self._io.read_bits_int_be(6)
        self.ecn = self._io.read_bits_int_be(2)
        self._io.align_to_byte()
        self.total_length = self._io.read_u2be()
        _ = self.total_length
        if not _ >= self.ihl_bytes:
            raise kaitaistruct.ValidationExprError(self.total_length, self._io, u"/seq/4")
        self.identification = self._io.read_u2be()
        self.flags = self._io.read_bits_int_be(3)
        self.fragment_offset = self._io.read_bits_int_be(13)
        self.ttl = self._io.read_bits_int_be(8)
        self.protocol = self._io.read_bits_int_be(8)
        self.header_checksum = self._io.read_bits_int_be(16)
        self._io.align_to_byte()
        self.src_address = self._io.read_bytes(4)
        self.dst_address = self._io.read_bytes(4)
        self.options = self._io.read_bytes((self.ihl_bytes - 20))
        self.body = self._io.read_bytes((self.total_length - self.ihl_bytes))

    @property
    def ihl_bytes(self):
        if hasattr(self, '_m_ihl_bytes'):
            return self._m_ihl_bytes

        self._m_ihl_bytes = (self.ihl * 4)
        return getattr(self, '_m_ihl_bytes', None)


