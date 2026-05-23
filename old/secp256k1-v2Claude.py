#!/usr/bin/env python3

import platform
import os
import sys
import ctypes
import math
import pickle


# CONSTANTS
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
ZERO_POINT = b'\x04' + (b'\x00' * 64)


# DLL LOADING
def _load_dll():
	system = platform.system().lower()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	
	if system.startswith('win'):
		dll_path = os.path.join(dir_path, 'ice_secp256k1.dll')
	elif system.startswith('lin'):
		dll_path = os.path.join(dir_path, 'ice_secp256k1.so')
	else:
		print('[-] Unsupported platform. Windows and Linux only.')
		sys.exit(1)
	
	if not os.path.isfile(dll_path):
		print(f'[-] DLL not found: {dll_path}')
		sys.exit(1)
	
	return ctypes.CDLL(os.path.realpath(dll_path))


ice = _load_dll()


# COIN TYPES
COIN_BTC   = 0
COIN_BSV   = 1
COIN_BTCD  = 2
COIN_ARG   = 3
COIN_AXE   = 4
COIN_BC    = 5
COIN_BCH   = 6
COIN_BSD   = 7
COIN_BTDX  = 8
COIN_BTG   = 9
COIN_BTX   = 10
COIN_CHA   = 11
COIN_DASH  = 12
COIN_DCR   = 13
COIN_DFC   = 14
COIN_DGB   = 15
COIN_DOGE  = 16
COIN_FAI   = 17
COIN_FTC   = 18
COIN_GRS   = 19
COIN_JBS   = 20
COIN_LTC   = 21
COIN_MEC   = 22
COIN_MONA  = 23
COIN_MZC   = 24
COIN_PIVX  = 25
COIN_POLIS = 26
COIN_RIC   = 27
COIN_STRAT = 28
COIN_SMART = 29
COIN_VIA   = 30
COIN_XMY   = 31
COIN_ZEC   = 32
COIN_ZCL   = 33
COIN_ZERO  = 34
COIN_ZEN   = 35
COIN_TENT  = 36
COIN_ZEIT  = 37
COIN_VTC   = 38
COIN_UNO   = 39
COIN_SKC   = 40
COIN_RVN   = 41
COIN_PPC   = 42
COIN_OMC   = 43
COIN_OK    = 44
COIN_NMC   = 45
COIN_NLG   = 46
COIN_LBRY  = 47
COIN_DNR   = 48
COIN_BWK   = 49


# CTYPES FUNCTION SIGNATURES
# Scalar operations
ice.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.scalar_multiplications.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

# Point operations
ice.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_doubling.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_loop_subtraction.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_loop_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_vector_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_increment_P2.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_increment_P2_mcpu.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.point_sequential_increment.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_decrement.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]

# Coordinate operations
ice.get_x_to_y.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]

# Address generation (pubkey/hash to address)
ice.pubkey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.pubkey_to_address.restype = ctypes.c_void_p
ice.hash_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.hash_to_address.restype = ctypes.c_void_p
ice.pubkey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]

# Address generation (privatekey)
ice.privatekey_to_coinaddress.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.privatekey_to_coinaddress.restype = ctypes.c_void_p
ice.privatekey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.privatekey_to_address.restype = ctypes.c_void_p
ice.privatekey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_loop_h160.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_loop_h160_sse.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]

# Ethereum operations
ice.pubkeyxy_to_ETH_address.argtypes = [ctypes.c_char_p]
ice.pubkeyxy_to_ETH_address.restype = ctypes.c_void_p
ice.pubkeyxy_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_to_ETH_address.argtypes = [ctypes.c_char_p]
ice.privatekey_to_ETH_address.restype = ctypes.c_void_p
ice.privatekey_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_group_to_ETH_address.argtypes = [ctypes.c_char_p, ctypes.c_int]
ice.privatekey_group_to_ETH_address.restype = ctypes.c_void_p
ice.privatekey_group_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

# Endomorphism operations
ice.pub_endo1.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.pub_endo2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

# Base58 encoding/decoding
ice.b58_encode.argtypes = [ctypes.c_char_p]
ice.b58_encode.restype = ctypes.c_void_p
ice.b58_decode.argtypes = [ctypes.c_char_p]
ice.b58_decode.restype = ctypes.c_void_p

# Bech32 operations
ice.bech32_address_decode.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]

# Hashing
ice.get_sha256.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]

# Bloom filter operations
ice.bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.bloom_check_add.restype = ctypes.c_int
ice.bloom_batch_add.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.bloom_check_add_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.test_bit_set_bit.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_int]
ice.create_bsgs_bloom_mcpu.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]

# BSGS operations
ice.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p]
ice.bsgs_2nd_check_prepare.argtypes = [ctypes.c_ulonglong]
ice.bsgs_2nd_check.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_char_p]
ice.bsgs_2nd_check.restype = ctypes.c_bool

# P2 group operations
ice.init_P2_Group.argtypes = [ctypes.c_char_p]

# Key derivation
ice.pbkdf2_hmac_sha512_dll.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
ice.pbkdf2_hmac_sha512_list.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_ulonglong]

# Memory/collision operations
ice.free_memory.argtypes = [ctypes.c_void_p]
ice.Load_data_to_memory.argtypes = [ctypes.c_char_p, ctypes.c_bool]
ice.check_collision.argtypes = [ctypes.c_char_p]
ice.check_collision.restype = ctypes.c_bool

ice.init_secp256_lib()


# UTILITY FUNCTIONS
def fl(val):
	return format(val, '064x')


def version():
	ice.version()


# SCALAR OPERATIONS
def _scalar_multiplication(pvk_int):
	res = (b'\x00') * 65
	pass_int_value = fl(pvk_int).encode('utf8')
	ice.scalar_multiplication(pass_int_value, res)
	return res

def scalar_multiplication(pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	res = _scalar_multiplication(pvk_int)
	return bytes(bytearray(res))

def _scalar_multiplications(pvk_int_list):
	sz = len(pvk_int_list)
	res = (b'\x00') * (65 * sz)
	pvks = b''.join(pvk_int_list)
	ice.scalar_multiplications(pvks, sz, res)
	return res

def scalar_multiplications(pvk_int_list):
	pvk_int_list = [bytes.fromhex(fl(N + i)) if i < 0 else bytes.fromhex(fl(i)) for i in pvk_int_list]
	res = _scalar_multiplications(pvk_int_list)
	return bytes(bytearray(res))


# POINT OPERATIONS
def get_x_to_y(x_hex, even):
	res = (b'\x00') * 32
	ice.get_x_to_y(bytes.fromhex(x_hex), even, res)
	return bytes(bytearray(res))

def point_increment(upub):
	res = (b'\x00') * 65
	ice.point_increment(upub, res)
	return bytes(bytearray(res))

def point_negation(upub):
	res = (b'\x00') * 65
	ice.point_negation(upub, res)
	return bytes(bytearray(res))

def point_doubling(upub):
	res = (b'\x00') * 65
	ice.point_doubling(upub, res)
	return bytes(bytearray(res))

def point_addition(upub1, upub2):
	res = (b'\x00') * 65
	ice.point_addition(upub1, upub2, res)
	return bytes(bytearray(res))

def point_subtraction(upub1, upub2):
	res = (b'\x00') * 65
	ice.point_subtraction(upub1, upub2, res)
	return bytes(bytearray(res))

def point_loop_subtraction(k, upub1, upub2):
	res = (b'\x00') * 65
	hex_k = fl(k).encode('utf8')
	ice.point_loop_subtraction(k, upub1, upub2, res)
	return bytes(bytearray(res))

def point_loop_addition(k, upub1, upub2):
	res = (b'\x00') * 65
	hex_k = fl(k).encode('utf8')
	ice.point_loop_addition(k, upub1, upub2, res)
	return bytes(bytearray(res))

def point_vector_addition(num, upubs1, upubs2):
	res = (b'\x00') * (65 * num)
	ice.point_vector_addition(num, upubs1, upubs2, res)
	return bytes(bytearray(res))

def point_sequential_increment_P2(num, upub1):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment_P2(num, upub1, res)
	return bytes(bytearray(res))

def point_sequential_increment_P2_mcpu(num, upub1, mcpu):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment_P2_mcpu(num, upub1, mcpu, res)
	return bytes(bytearray(res))

def point_sequential_increment(num, upub1):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment(num, upub1, res)
	return bytes(bytearray(res))

def point_sequential_decrement(num, upub1):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_decrement(num, upub1, res)
	return bytes(bytearray(res))

def point_negation_fast(upub):
	res = (b'\x00') * 65
	ice.point_negation_fast(upub, res)
	return bytes(bytearray(res))

def pub_endo1(upub):
	res = (b'\x00') * 65
	ice.pub_endo1(upub, res)
	return bytes(bytearray(res))

def pub_endo2(upub):
	res = (b'\x00') * 65
	ice.pub_endo2(upub, res)
	return bytes(bytearray(res))

def init_P2_Group(upub):
	ice.init_P2_Group(upub)


# ADDRESS GENERATION FROM PUBLICKEY
def _pubkey_to_address(format_type, compressed, pubkey):
	res = ice.pubkey_to_address(format_type, compressed, pubkey)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def pubkey_to_address(format_type, compressed, pubkey):
	return _pubkey_to_address(format_type, compressed, pubkey)

def _hash_to_address(format_type, compressed, h160):
	res = ice.hash_to_address(format_type, compressed, h160)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def hash_to_address(format_type, compressed, h160):
	return _hash_to_address(format_type, compressed, h160)

def pubkey_to_h160(format_type, compressed, pubkey):
	res = (b'\x00') * 20
	ice.pubkey_to_h160(format_type, compressed, pubkey, res)
	return bytes(bytearray(res))


# ADDRESS GENERATION FROM PRIVATEKEY
def _privatekey_to_coinaddress(coin_type, format_type, compressed, pvk_int):
	pvk_hex = fl(pvk_int).encode('utf8')
	res = ice.privatekey_to_coinaddress(coin_type, format_type, compressed, pvk_hex)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def privatekey_to_coinaddress(coin_type, format_type, compressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	return _privatekey_to_coinaddress(coin_type, format_type, compressed, pvk_int)

def _privatekey_to_address(format_type, compressed, pvk_int):
	pvk_hex = fl(pvk_int).encode('utf8')
	res = ice.privatekey_to_address(format_type, compressed, pvk_hex)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def privatekey_to_address(format_type, compressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	return _privatekey_to_address(format_type, compressed, pvk_int)

def privatekey_to_h160(format_type, compressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	res = (b'\x00') * 20
	pvk_hex = fl(pvk_int).encode('utf8')
	ice.privatekey_to_h160(format_type, compressed, pvk_hex, res)
	return bytes(bytearray(res))

def privatekey_loop_h160(num, format_type, compressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	res = (b'\x00') * (20 * num)
	pvk_hex = fl(pvk_int).encode('utf8')
	ice.privatekey_loop_h160(num, format_type, compressed, pvk_hex, res)
	return bytes(bytearray(res))

def privatekey_loop_h160_sse(num, format_type, compressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	res = (b'\x00') * (20 * num)
	pvk_hex = fl(pvk_int).encode('utf8')
	ice.privatekey_loop_h160_sse(num, format_type, compressed, pvk_hex, res)
	return bytes(bytearray(res))


# ETHEREUM OPERATIONS
def _pubkeyxy_to_ETH_address(upub_xy):
	res = ice.pubkeyxy_to_ETH_address(upub_xy)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def pubkeyxy_to_ETH_address(upub_xy):
	return _pubkeyxy_to_ETH_address(upub_xy)

def pubkeyxy_to_ETH_address_bytes(upub_xy):
	res = (b'\x00') * 20
	ice.pubkeyxy_to_ETH_address_bytes(upub_xy, res)
	return bytes(bytearray(res))

def _privatekey_to_ETH_address(pvk_int):
	pvk_hex = fl(pvk_int).encode('utf8')
	res = ice.privatekey_to_ETH_address(pvk_hex)
	address = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return address

def privatekey_to_ETH_address(pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	return _privatekey_to_ETH_address(pvk_int)

def privatekey_to_ETH_address_hex(pvk_int):
	addr = privatekey_to_ETH_address(pvk_int)
	return '0x' + addr

def _privatekey_to_ETH_address_bytes(pvk_hex):
	res = (b'\x00') * 20
	ice.privatekey_to_ETH_address_bytes(pvk_hex, res)
	return res

def privatekey_to_ETH_address_bytes(pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pvk_hex = fl(pvk_int).encode('utf8')
	res = _privatekey_to_ETH_address_bytes(pvk_hex)
	return bytes(bytearray(res))

def privatekey_group_to_ETH_address(pvk_int, m):
	if m <= 0: m = 1
	if pvk_int < 0: pvk_int = N + pvk_int
	pvk_hex = fl(pvk_int).encode('utf8')
	res = ice.privatekey_group_to_ETH_address(pvk_hex, m)
	addrlist = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return addrlist

def _privatekey_group_to_ETH_address_bytes(pvk_hex, m):
	res = (b'\x00') * (20 * m)
	ice.privatekey_group_to_ETH_address_bytes(pvk_hex, m, res)
	return res

def privatekey_group_to_ETH_address_bytes(pvk_int, m):
	if m <= 0: m = 1
	if pvk_int < 0: pvk_int = N + pvk_int
	pvk_hex = fl(pvk_int).encode('utf8')
	res = _privatekey_group_to_ETH_address_bytes(pvk_hex, m)
	return bytes(bytearray(res))


# ENCODING/DECODING
def b58_encode(hash_hex):
	res = ice.b58_encode(hash_hex)
	encoded = ctypes.cast(res, ctypes.c_char_p).value.decode('utf8')
	ice.free_memory(res)
	return encoded

def b58_decode(address):
	res = ice.b58_decode(address)
	decoded = ctypes.cast(res, ctypes.c_char_p).value
	ice.free_memory(res)
	return decoded

def bech32_address_decode(coin_type, address):
	res = (b'\x00') * 20
	ice.bech32_address_decode(coin_type, address, res)
	return bytes(bytearray(res))

def get_sha256(data):
	data_len = len(data)
	res = (b'\x00') * 32
	ice.get_sha256(data, data_len, res)
	return bytes(bytearray(res))


# PUBKEY CONVERSION
def to_cpub(pub_hex):
	if len(pub_hex) > 70:
		is_even = int(pub_hex[66:], 16) % 2 == 0
		return ('02' if is_even else '03') + pub_hex[2:66]
	return pub_hex

def point_to_cpub(pubkey_bytes):
	pub_hex = pubkey_bytes.hex()
	if len(pub_hex) > 70:
		is_even = int(pub_hex[66:], 16) % 2 == 0
		return ('02' if is_even else '03') + pub_hex[2:66]
	return pub_hex

def pub2upub(pub_hex):
	x = pub_hex[2:66]
	if len(pub_hex) < 70:
		is_even = int(pub_hex[:2], 16) % 2 == 0
		y = get_x_to_y(x, is_even).hex()
	else:
		y = pub_hex[66:].zfill(64)
	return bytes.fromhex('04' + x + y)


# BLOOM FILTER OPERATIONS
def bloom_para(items, false_positive_rate=0.000001):
	bits = math.ceil((items * math.log(false_positive_rate)) / math.log(1 / pow(2, math.log(2))))
	if bits % 8: bits = 8 * (1 + (bits // 8))
	hashes = round((bits / items) * math.log(2))
	return bits, hashes

def Fill_in_bloom(inp_list, false_positive_rate=0.000001):
	_bits, _hashes = bloom_para(len(inp_list), false_positive_rate)
	_bf = (b'\x00') * (_bits // 8)
	for line in inp_list:
		tt = line if isinstance(line, bytes) else str(line).encode('utf-8')
		ice.bloom_check_add(tt, len(tt), 1, _bits, _hashes, _bf)
	return _bits, _hashes, _bf, false_positive_rate, len(inp_list)

def dump_bloom_file(output_file, _bits, _hashes, _bf, _fp, _elem):
	with open(output_file, 'wb') as f:
		pickle.dump((_bits, _hashes, _bf, _fp, _elem), f)

def read_bloom_file(bloom_file):
	with open(bloom_file, 'rb') as f:
		return pickle.load(f)

def check_in_bloom(line, _bits, _hashes, _bf):
	tt = line if isinstance(line, bytes) else str(line).encode('utf-8')
	return ice.bloom_check_add(tt, len(tt), 0, _bits, _hashes, _bf) > 0

def bloom_check_add_mcpu(bigbuff, num_items, sz, mcpu, check_add, bloom_bits, bloom_hashes, bloom_filter):
	found_array = (b'\x00') * num_items
	ice.bloom_check_add_mcpu(bigbuff, num_items, found_array, sz, mcpu, check_add, bloom_bits, bloom_hashes, bloom_filter)
	return found_array


# BSGS OPERATIONS
def create_baby_table(start, end):
	res = (b'\x00') * 32
	ice.create_baby_table(start, end, res)
	return bytes(bytearray(res))

def create_bsgs_bloom_mcpu(mcpu, total_entries, false_positive_rate=0.0000001):
	if total_entries % (mcpu * 1000) != 0:
		total_entries = mcpu * 1000 * (total_entries // (mcpu * 1000))
		if total_entries == 0: total_entries = mcpu * 1000
		print(f'[*] Corrected entries to nearest multiple of 1000*mcpu: {total_entries}')
	_bits, _hashes = bloom_para(total_entries, false_positive_rate)
	_bf = bytes(b'\x00') * (_bits // 8)
	print(f'[+] bloom [bits: {_bits}] [hashes: {_hashes}] [size: {_bits//8} B] [fp: {false_positive_rate}]')
	ice.create_bsgs_bloom_mcpu(mcpu, total_entries, _bits, _hashes, _bf)
	return _bits, _hashes, _bf, false_positive_rate, total_entries

def bsgs_2nd_check_prepare(bP_elem=2000000000):
	if bP_elem < 8000000: bP_elem = 8000000
	ice.bsgs_2nd_check_prepare(bP_elem)

def bsgs_2nd_check(pubkey_bytes, z1_int, bP_elem):
	if z1_int < 0: z1_int = N + z1_int
	hex_value = fl(z1_int).encode('utf8')
	res = (b'\x00') * 32
	found = ice.bsgs_2nd_check(pubkey_bytes, hex_value, bP_elem, res)
	return found, res


# FILE OPERATIONS
def prepare_bin_file_work(in_file, out_file, lower=False):
	inp_list = [line.split()[0].lower() if lower else line.split()[0] for line in open(in_file, 'r')]
	use0x = inp_list[0][:2] == '0x'
	
	with open(out_file, 'wb') as f:
		if use0x:
			inp_list = [line[2:] for line in inp_list]
		inp_list.sort()
		for line in inp_list:
			f.write(bytes.fromhex(line))

def prepare_bin_file(in_file, out_file, overwrite=False, lower=False):
	if not os.path.isfile(out_file):
		prepare_bin_file_work(in_file, out_file, lower)
	else:
		if not overwrite:
			print(f'[+] File {out_file} exists, using as-is')
		else:
			print(f'[+] File {out_file} exists, overwriting')
			prepare_bin_file_work(in_file, out_file, lower)

def Load_data_to_memory(input_bin_file, verbose=False):
	ice.Load_data_to_memory(input_bin_file.encode('utf-8'), verbose)

def check_collision(h160):
	return ice.check_collision(h160)
