# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class WholePdu(KaitaiStruct):
    def __init__(self, label_type_indicator, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.label_type_indicator = label_type_indicator
        self._read()

    def _read(self):
        self.protocol_type = self._io.read_bits_int_be(16)
        self._io.align_to_byte()
        if self.label_type_indicator == 0:
            self.six_byte_label = self._io.read_bytes(6)

        if self.label_type_indicator == 1:
            self.three_byte_label = self._io.read_bytes(3)

        self.data = self._io.read_bytes_full()


