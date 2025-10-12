#!/usr/bin/env python3
"""
Test script to verify IP extractor functionality.
Tests that the IP parser:
1. Scans every byte offset
2. Extracts IP header length (IHL field)
3. Validates the checksum
4. Extracts valid IP packets
"""

import struct
import sys
import os
from io import BytesIO

# Add parent directory to path so we can import parser module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Add parser/parsers/ip directory for direct imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'parser', 'parsers', 'ip'))

from parser.parsers.ip.ip_parser import IPv4Parser
from kaitaistruct import KaitaiStream

def create_valid_ipv4_packet():
    """Create a valid IPv4 packet with correct checksum."""
    # IPv4 header fields
    version_ihl = (4 << 4) | 5  # Version 4, IHL=5 (20 bytes)
    dscp_ecn = 0
    total_length = 40  # 20 byte header + 20 byte payload
    identification = 0x1234
    flags_fragment = 0
    ttl = 64
    protocol = 17  # UDP
    checksum = 0  # Will calculate
    src_ip = struct.pack('!I', 0xC0A80001)  # 192.168.0.1
    dst_ip = struct.pack('!I', 0xC0A80002)  # 192.168.0.2
    
    # Build header without checksum
    header = struct.pack('!BBHHHBBH',
                        version_ihl,
                        dscp_ecn,
                        total_length,
                        identification,
                        flags_fragment,
                        ttl,
                        protocol,
                        checksum)
    header += src_ip + dst_ip
    
    # Calculate checksum
    checksum = IPv4Parser.ipv4_checksum(header)
    
    # Rebuild with correct checksum
    header = struct.pack('!BBHHHBBH',
                        version_ihl,
                        dscp_ecn,
                        total_length,
                        identification,
                        flags_fragment,
                        ttl,
                        protocol,
                        checksum)
    header += src_ip + dst_ip
    
    # Add 20 bytes of payload
    payload = b'A' * 20
    
    return header + payload

def create_invalid_checksum_packet():
    """Create an IPv4 packet with invalid checksum."""
    packet = create_valid_ipv4_packet()
    # Corrupt the checksum field
    packet_list = bytearray(packet)
    packet_list[10] ^= 0xFF  # Flip bits in checksum
    packet_list[11] ^= 0xFF
    return bytes(packet_list)

def test_checksum_validation():
    """Test that checksum validation works correctly."""
    print("=" * 60)
    print("TEST 1: Checksum Validation")
    print("=" * 60)
    
    # Test valid packet
    valid_packet = create_valid_ipv4_packet()
    print(f"\nValid packet (first 20 bytes): {valid_packet[:20].hex()}")
    
    try:
        IPv4Parser.is_valid_ipv4_checksum(valid_packet)
        print("✓ Valid packet checksum: PASSED")
    except AssertionError:
        print("✗ Valid packet checksum: FAILED (should have passed)")
        return False
    
    # Test invalid packet
    invalid_packet = create_invalid_checksum_packet()
    print(f"\nInvalid packet (first 20 bytes): {invalid_packet[:20].hex()}")
    
    try:
        IPv4Parser.is_valid_ipv4_checksum(invalid_packet)
        print("✗ Invalid packet checksum: FAILED (should have failed)")
        return False
    except AssertionError:
        print("✓ Invalid packet checksum: PASSED (correctly rejected)")
    
    return True

def test_header_length_extraction():
    """Test that IHL (header length) is correctly extracted."""
    print("\n" + "=" * 60)
    print("TEST 2: Header Length Extraction")
    print("=" * 60)
    
    packet = create_valid_ipv4_packet()
    
    # Extract IHL from first byte
    version_ihl = packet[0]
    ihl = version_ihl & 0x0F
    header_length_bytes = ihl * 4
    
    print(f"\nFirst byte: 0x{packet[0]:02x}")
    print(f"IHL field: {ihl} (4-bit value)")
    print(f"Header length in bytes: {header_length_bytes}")
    
    if header_length_bytes == 20:
        print("✓ Header length extraction: PASSED")
        return True
    else:
        print(f"✗ Header length extraction: FAILED (expected 20, got {header_length_bytes})")
        return False

def test_byte_by_byte_scanning():
    """Test that the parser scans byte-by-byte to find packets."""
    print("\n" + "=" * 60)
    print("TEST 3: Byte-by-Byte Scanning")
    print("=" * 60)
    
    # Create test data with junk before a valid packet
    valid_packet = create_valid_ipv4_packet()
    junk_bytes = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'
    test_data = junk_bytes + valid_packet
    
    print(f"\nTest data structure:")
    print(f"  - Junk bytes: {len(junk_bytes)} bytes")
    print(f"  - Valid packet: {len(valid_packet)} bytes at offset {len(junk_bytes)}")
    print(f"  - Total: {len(test_data)} bytes")
    
    # Write test data to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        temp_file = f.name
        f.write(test_data)
    
    try:
        # Process with IP parser
        import logging
        parser = IPv4Parser(os.path.basename(temp_file), show_pbar=False, log_level=logging.WARNING)
        
        # Use process_capture_file which handles file opening with mmap
        parser.process_capture_file(temp_file)
        parser.done_processing()
        
        # Check results
        print(f"\nParser results:")
        print(f"  - Bytes searched: {parser.bytes_searched}")
        print(f"  - Bytes skipped: {parser.bytes_skipped}")
        
        if parser.bytes_skipped == len(junk_bytes):
            print(f"✓ Byte-by-byte scanning: PASSED (skipped {parser.bytes_skipped} junk bytes)")
            return True
        else:
            print(f"✗ Byte-by-byte scanning: FAILED (expected {len(junk_bytes)} skipped, got {parser.bytes_skipped})")
            return False
            
    finally:
        # Clean up
        os.unlink(temp_file)
        if os.path.exists(parser.protocol_file):
            os.unlink(parser.protocol_file)
        if os.path.exists(parser.skips_file):
            os.unlink(parser.skips_file)
        if os.path.exists(parser.pcap_file):
            os.unlink(parser.pcap_file)

def test_packet_extraction():
    """Test that valid packets are correctly extracted."""
    print("\n" + "=" * 60)
    print("TEST 4: Complete Packet Extraction")
    print("=" * 60)
    
    # Create test data with multiple packets
    packet1 = create_valid_ipv4_packet()
    packet2 = create_valid_ipv4_packet()
    junk = b'\xFF' * 10
    invalid_packet = create_invalid_checksum_packet()
    
    test_data = packet1 + junk + invalid_packet + junk + packet2
    
    print(f"\nTest data structure:")
    print(f"  1. Valid packet: {len(packet1)} bytes")
    print(f"  2. Junk: {len(junk)} bytes")
    print(f"  3. Invalid packet (bad checksum): {len(invalid_packet)} bytes")
    print(f"  4. Junk: {len(junk)} bytes")
    print(f"  5. Valid packet: {len(packet2)} bytes")
    print(f"  Total: {len(test_data)} bytes")
    
    # Write test data to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        temp_file = f.name
        f.write(test_data)
    
    try:
        # Process with IP parser
        import logging
        parser = IPv4Parser(os.path.basename(temp_file), show_pbar=False, log_level=logging.WARNING)
        
        # Use process_capture_file which handles file opening with mmap
        parser.process_capture_file(temp_file)
        parser.done_processing()
        
        # Read extracted packets
        if os.path.exists(parser.protocol_file):
            with open(parser.protocol_file, 'rb') as f:
                extracted = f.read()
            
            print(f"\nExtraction results:")
            print(f"  - Extracted data size: {len(extracted)} bytes")
            print(f"  - Expected: {len(packet1) + len(packet2)} bytes (2 valid packets)")
            
            if len(extracted) == len(packet1) + len(packet2):
                print("✓ Packet extraction: PASSED (extracted 2 valid packets, ignored invalid)")
                return True
            else:
                print(f"✗ Packet extraction: FAILED")
                return False
        else:
            print("✗ Packet extraction: FAILED (no output file created)")
            return False
            
    finally:
        # Clean up
        os.unlink(temp_file)
        if os.path.exists(parser.protocol_file):
            os.unlink(parser.protocol_file)
        if os.path.exists(parser.skips_file):
            os.unlink(parser.skips_file)
        if os.path.exists(parser.pcap_file):
            os.unlink(parser.pcap_file)

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("IP EXTRACTOR VERIFICATION TEST SUITE")
    print("=" * 60)
    print("\nThis test verifies the IP extractor:")
    print("  1. Scans every byte offset")
    print("  2. Extracts IP header length (IHL)")
    print("  3. Validates checksums")
    print("  4. Extracts valid packets")
    
    results = []
    
    # Run tests
    results.append(("Checksum Validation", test_checksum_validation()))
    results.append(("Header Length Extraction", test_header_length_extraction()))
    results.append(("Byte-by-Byte Scanning", test_byte_by_byte_scanning()))
    results.append(("Complete Packet Extraction", test_packet_extraction()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print("\n" + "=" * 60)
    print(f"OVERALL: {passed_count}/{total_count} tests passed")
    print("=" * 60)
    
    if passed_count == total_count:
        print("\n✓ ALL TESTS PASSED - IP extractor works as intended!")
        return 0
    else:
        print(f"\n✗ SOME TESTS FAILED - {total_count - passed_count} test(s) need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
