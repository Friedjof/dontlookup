# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class HandlePduProtocol(KaitaiStruct):
    def __init__(self, protocol_type, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.protocol_type = protocol_type
        self._read()

    def _read(self):
        _on = self.protocol_type
        if _on == 2:
            self.protocol = HandlePduProtocol.ThreeByteNpa(self._io, self, self._root)
        else:
            self.protocol = HandlePduProtocol.DoNothing(self._io, self, self._root)

    class ThreeByteNpa(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.npa = self._io.read_bytes(3)


    class TsConcat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.d = self._io.read_bits_int_be(1) != 0
            self.length = self._io.read_bits_int_be(15)
            self.type = self._io.read_bits_int_be(16)
            if not self.type == 2:
                raise kaitaistruct.ValidationNotEqualError(2, self.type, self._io, u"/types/ts_concat/seq/2")
            self._io.align_to_byte()
            self.dest_npa = self._io.read_bytes(6)
            self.payload = self._io.read_bytes(self.length)
            self.crc = self._io.read_bytes(4)


    class UleExtensionHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.zero_prefix = self._io.read_bits_int_be(5)
            if not self.zero_prefix == 0:
                raise kaitaistruct.ValidationNotEqualError(0, self.zero_prefix, self._io, u"/types/ule_extension_header/seq/0")
            self.h_len = self._io.read_bits_int_be(3)
            self.h_type = self._io.read_bits_int_be(8)


    class DoNothing(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class SixByteNpa(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.npa = self._io.read_bytes(6)


    class BridgedSnduHeaderWithNpa(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.d = self._io.read_bits_int_be(1) != 0
            self.length = self._io.read_bits_int_be(15)
            self.type = self._io.read_bits_int_be(16)
            if not self.type == 1:
                raise kaitaistruct.ValidationNotEqualError(1, self.type, self._io, u"/types/bridged_sndu_header_with_npa/seq/2")
            self._io.align_to_byte()
            if self.d:
                self.dest_npa = self._io.read_bytes(6)

            self.dest_mac = self._io.read_bytes(6)
            self.src_mac = self._io.read_bytes(6)
            self.ethertype_llc_len = self._io.read_bytes(2)
            self.payload = self._io.read_bytes(self.length)
            self.crc = self._io.read_bytes(4)



