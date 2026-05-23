#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os
import sys
import ctypes
import math
import pickle
import base64

# ============================================================================
# CONSTANTS
# ============================================================================

N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Zero = b'\x04' + b'\x00' * 64

# Coin types
COIN_BTC = 0
COIN_BSV = 1
COIN_BTCD = 2
COIN_ARG = 3
COIN_AXE = 4
COIN_BC = 5
COIN_BCH = 6
COIN_BSD = 7
COIN_BTDX = 8
COIN_BTG = 9
COIN_BTX = 10
COIN_CHA = 11
COIN_DASH = 12
COIN_DCR = 13
COIN_DFC = 14
COIN_DGB = 15
COIN_DOGE = 16
COIN_FAI = 17
COIN_FTC = 18
COIN_GRS = 19
COIN_JBS = 20
COIN_LTC = 21
COIN_MEC = 22
COIN_MONA = 23
COIN_MZC = 24
COIN_PIVX = 25
COIN_POLIS = 26
COIN_RIC = 27
COIN_STRAT = 28
COIN_SMART = 29
COIN_VIA = 30
COIN_XMY = 31
COIN_ZEC = 32
COIN_ZCL = 33
COIN_ZERO = 34
COIN_ZEN = 35
COIN_TENT = 36
COIN_ZEIT = 37
COIN_VTC = 38
COIN_UNO = 39
COIN_SKC = 40
COIN_RVN = 41
COIN_PPC = 42
COIN_OMC = 43
COIN_OK = 44
COIN_NMC = 45
COIN_NLG = 46
COIN_LBRY = 47
COIN_DNR = 48
COIN_BWK = 49

# Mnemonic languages
MNEM_EN = 0
MNEM_JP = 1
MNEM_KR = 2
MNEM_SP = 3
MNEM_CS = 4
MNEM_CT = 5
MNEM_FR = 6
MNEM_IT = 7
MNEM_CZ = 8
MNEM_PT = 9

# ============================================================================
# DLL/SO LOADING
# ============================================================================

dir_path = os.path.dirname(os.path.realpath(__file__))

if platform.system().lower().startswith('win'):
	dllfile = dir_path + '/ice_secp256k1.dll'
	if os.path.isfile(dllfile):
		pathdll = os.path.realpath(dllfile)
		ice = ctypes.CDLL(pathdll)
	else:
		print('File {} not found'.format(dllfile))
		sys.exit()

elif platform.system().lower().startswith('lin'):
	dllfile = dir_path + '/ice_secp256k1.so'
	if os.path.isfile(dllfile):
		pathdll = os.path.realpath(dllfile)
		ice = ctypes.CDLL(pathdll)
	else:
		print('File {} not found'.format(dllfile))
		sys.exit()

else:
	print('[-] Unsupported Platform: Windows and Linux only')
	sys.exit()

# ============================================================================
# CTYPES FUNCTION SIGNATURES
# ============================================================================

# Scalar operations
ice.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.scalar_multiplications.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

# Point arithmetic
ice.get_x_to_y.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]
ice.point_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_doubling.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_loop_subtraction.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_loop_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_vector_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_increment.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_increment_P2.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]
ice.point_sequential_increment_P2_mcpu.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.point_sequential_increment_P2X_mcpu.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.point_sequential_decrement.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]

# Address generation
ice.privatekey_to_coinaddress.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.privatekey_to_coinaddress.restype = ctypes.c_void_p
ice.pubkey_to_coinaddress.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.pubkey_to_coinaddress.restype = ctypes.c_void_p
ice.privatekey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.privatekey_to_address.restype = ctypes.c_void_p
ice.pubkey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.pubkey_to_address.restype = ctypes.c_void_p
ice.hash_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
ice.hash_to_address.restype = ctypes.c_void_p
ice.pubkey_to_p2wsh_address.argtypes = [ctypes.c_char_p]
ice.pubkey_to_p2wsh_address.restype = ctypes.c_void_p

# Hash160 operations
ice.privatekey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_loop_h160.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_loop_h160_sse.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]
ice.pubkey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]

# Ethereum
ice.pubkeyxy_to_ETH_address.argtypes = [ctypes.c_char_p]
ice.pubkeyxy_to_ETH_address.restype = ctypes.c_void_p
ice.pubkeyxy_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_to_ETH_address.argtypes = [ctypes.c_char_p]
ice.privatekey_to_ETH_address.restype = ctypes.c_void_p
ice.privatekey_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.privatekey_group_to_ETH_address.argtypes = [ctypes.c_char_p, ctypes.c_int]
ice.privatekey_group_to_ETH_address.restype = ctypes.c_void_p
ice.privatekey_group_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

# Hash functions
ice.get_hmac_sha512.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.get_sha512.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.get_sha256.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
ice.get_sha256_iter.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulonglong]
ice.rmd160.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
ice.hash160.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

# Encoding
ice.b58_encode.argtypes = [ctypes.c_char_p]
ice.b58_encode.restype = ctypes.c_void_p
ice.b58_decode.argtypes = [ctypes.c_char_p]
ice.b58_decode.restype = ctypes.c_void_p
ice.bech32_address_decode.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]

# Key operations
ice.pubkey_isvalid.argtypes = [ctypes.c_char_p]
ice.pubkey_isvalid.restype = ctypes.c_bool
ice.pub_endo1.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.pub_endo2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ice.init_P2_Group.argtypes = [ctypes.c_char_p]

# Mnemonics
ice.mnem_to_masternode.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
ice.create_valid_mnemonics.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
ice.create_valid_mnemonics.restype = ctypes.c_void_p
ice.pbkdf2_hmac_sha512_dll.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
ice.pbkdf2_hmac_sha512_list.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_ulonglong]

# Baby step giant step
ice.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p]

# Bloom filter
ice.bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.bloom_check_add.restype = ctypes.c_int
ice.bloom_batch_add.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.bloom_check_add_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]
ice.test_bit_set_bit.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_int]
ice.create_bsgs_bloom_mcpu.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ubyte, ctypes.c_char_p]

# BSGS
ice.bsgs_2nd_check_prepare.argtypes = [ctypes.c_ulonglong]
ice.dump_bsgs_state.argtypes = [ctypes.c_char_p, ctypes.c_bool]
ice.load_bsgs_state.argtypes = [ctypes.c_char_p, ctypes.c_bool]
ice.bsgs_2nd_check.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
ice.bsgs_2nd_check.restype = ctypes.c_bool
ice.bsgs_2nd_check_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

# Collision detection
ice.Load_data_to_memory.argtypes = [ctypes.c_char_p, ctypes.c_bool]
ice.check_collision.argtypes = [ctypes.c_char_p]
ice.check_collision.restype = ctypes.c_bool
ice.check_collision_mcpu.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]

# XOR filter
ice.xor_filter_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint64, ctypes.c_uint8, ctypes.c_char_p]
ice.xor_filter_check.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint64, ctypes.c_uint8, ctypes.c_char_p]
ice.xor_filter_check.restype = ctypes.c_int
ice.xor_filter_check_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_uint8, ctypes.c_char_p, ctypes.c_char_p]
ice.bsgs_xor_create_mcpu.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_uint64, ctypes.c_uint8, ctypes.c_char_p]

# Utilities
ice.free_memory.argtypes = [ctypes.c_void_p]

ice.init_secp256_lib()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def fl(i):
	'''Format integer to hex string'''
	return hex(i)[2:].zfill(64)

def version():
	ice.version()

# ============================================================================
# SCALAR OPERATIONS
# ============================================================================

def _scalar_multiplication(pvk_int):
	res = (b'\x00') * 65
	pass_int_value = fl(pvk_int).encode('utf8')
	ice.scalar_multiplication(pass_int_value, res)
	return res

def scalar_multiplication(pvk_int):
	res = _scalar_multiplication(pvk_int)
	return bytes(bytearray(res))

def _scalar_multiplications(pvk_int_list):
	pvk_int_list = [bytes.fromhex(fl(N+i)) if i < 0 else bytes.fromhex(fl(i)) for i in pvk_int_list]
	bigbuff = b''.join(pvk_int_list)
	res = (b'\x00') * (65 * len(pvk_int_list))
	ice.scalar_multiplications(bigbuff, len(pvk_int_list), res)
	return res

def scalar_multiplications(pvk_int_list):
	res = _scalar_multiplications(pvk_int_list)
	return bytes(bytearray(res))

# ============================================================================
# POINT ARITHMETIC
# ============================================================================

def _point_multiplication(pubkey_bytes, kk):
	res = (b'\x00') * 65
	bytes_value = bytes.fromhex(hex(kk)[2:].zfill(64))
	ice.point_multiplication(pubkey_bytes, bytes_value, res)
	return res

def point_multiplication(P, k):
	if type(P) == int: k, P = P, k
	res = _point_multiplication(P, k)
	return bytes(bytearray(res))

def point_division(P, k):
	kk = inv(k)
	res = point_multiplication(P, kk)
	return bytes(bytearray(res))

def _get_x_to_y(x_hex, is_even):
	res = (b'\x00') * 32
	ice.get_x_to_y(x_hex.encode('utf8'), is_even, res)
	return res

def get_x_to_y(x_hex, is_even):
	res = _get_x_to_y(x_hex, is_even)
	return bytes(bytearray(res))

def _point_increment(pubkey_bytes):
	res = (b'\x00') * 65
	ice.point_increment(pubkey_bytes, res)
	return res

def point_increment(pubkey_bytes):
	res = _point_increment(pubkey_bytes)
	return bytes(bytearray(res))

def _point_negation(pubkey_bytes):
	res = (b'\x00') * 65
	ice.point_negation(pubkey_bytes, res)
	return res

def point_negation(pubkey_bytes):
	res = _point_negation(pubkey_bytes)
	return bytes(bytearray(res))

def _point_doubling(pubkey_bytes):
	res = (b'\x00') * 65
	ice.point_doubling(pubkey_bytes, res)
	return res

def point_doubling(pubkey_bytes):
	res = _point_doubling(pubkey_bytes)
	return bytes(bytearray(res))

def _point_addition(pubkey1_bytes, pubkey2_bytes):
	res = (b'\x00') * 65
	ice.point_addition(pubkey1_bytes, pubkey2_bytes, res)
	return res

def point_addition(P1, P2):
	res = _point_addition(P1, P2)
	return bytes(bytearray(res))

def _point_subtraction(pubkey1_bytes, pubkey2_bytes):
	res = (b'\x00') * 65
	ice.point_subtraction(pubkey1_bytes, pubkey2_bytes, res)
	return res

def point_subtraction(P1, P2):
	res = _point_subtraction(P1, P2)
	return bytes(bytearray(res))

def point_loop_subtraction(k, pubkey1_bytes, pubkey2_bytes):
	res = (b'\x00') * 65
	ice.point_loop_subtraction(k, pubkey1_bytes, pubkey2_bytes, res)
	return bytes(bytearray(res))

def point_loop_addition(k, pubkey1_bytes, pubkey2_bytes):
	res = (b'\x00') * 65
	ice.point_loop_addition(k, pubkey1_bytes, pubkey2_bytes, res)
	return bytes(bytearray(res))

def point_vector_addition(pubkeys1_bytes, pubkeys2_bytes, num_points):
	res = (b'\x00') * (65 * num_points)
	ice.point_vector_addition(num_points, pubkeys1_bytes, pubkeys2_bytes, res)
	return bytes(bytearray(res))

def point_sequential_increment(pubkey_bytes, num):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment(num, pubkey_bytes, res)
	return bytes(bytearray(res))

def point_sequential_increment_P2(pubkey_bytes, num):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment_P2(num, pubkey_bytes, res)
	return bytes(bytearray(res))

def point_sequential_increment_P2_mcpu(pubkey_bytes, num, mcpu=os.cpu_count()):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_increment_P2_mcpu(num, pubkey_bytes, mcpu, res)
	return bytes(bytearray(res))

def point_sequential_increment_P2X_mcpu(pubkey_bytes, num, mcpu=os.cpu_count()):
	res = (b'\x00') * (32 * num)
	ice.point_sequential_increment_P2X_mcpu(num, pubkey_bytes, mcpu, res)
	return bytes(bytearray(res))

def point_sequential_decrement(pubkey_bytes, num):
	res = (b'\x00') * (65 * num)
	ice.point_sequential_decrement(num, pubkey_bytes, res)
	return bytes(bytearray(res))

def init_P2_Group(pubkey_bytes):
	ice.init_P2_Group(pubkey_bytes)

# ============================================================================
# ADDRESS GENERATION
# ============================================================================

def privatekey_to_coinaddress(coin_type, addr_type, iscompressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pass_int_value = fl(pvk_int).encode('utf8')
	res = ice.privatekey_to_coinaddress(coin_type, addr_type, iscompressed, pass_int_value)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def pubkey_to_coinaddress(coin_type, addr_type, iscompressed, pubkey_bytes):
	res = ice.pubkey_to_coinaddress(coin_type, addr_type, iscompressed, pubkey_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def privatekey_to_address(addr_type, iscompressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pass_int_value = fl(pvk_int).encode('utf8')
	res = ice.privatekey_to_address(addr_type, iscompressed, pass_int_value)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def pubkey_to_address(addr_type, iscompressed, pubkey_bytes):
	res = ice.pubkey_to_address(addr_type, iscompressed, pubkey_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def hash_to_address(addr_type, iscompressed, hash160_bytes):
	res = ice.hash_to_address(addr_type, iscompressed, hash160_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def pubkey_to_p2wsh_address(pubkey_bytes):
	res = ice.pubkey_to_p2wsh_address(pubkey_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

# ============================================================================
# HASH160 OPERATIONS
# ============================================================================

def _privatekey_to_h160(addr_type, iscompressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pass_int_value = fl(pvk_int).encode('utf8')
	res = (b'\x00') * 20
	ice.privatekey_to_h160(addr_type, iscompressed, pass_int_value, res)
	return res

def privatekey_to_h160(addr_type, iscompressed, pvk_int):
	res = _privatekey_to_h160(addr_type, iscompressed, pvk_int)
	return bytes(bytearray(res))

def _privatekey_loop_h160(num, addr_type, iscompressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pass_int_value = fl(pvk_int).encode('utf8')
	res = (b'\x00') * (20 * num)
	ice.privatekey_loop_h160(num, addr_type, iscompressed, pass_int_value, res)
	return res

def privatekey_loop_h160(num, addr_type, iscompressed, pvk_int):
	res = _privatekey_loop_h160(num, addr_type, iscompressed, pvk_int)
	return bytes(bytearray(res))

def _privatekey_loop_h160_sse(num, addr_type, iscompressed, pvk_int):
	if pvk_int < 0: pvk_int = N + pvk_int
	pass_int_value = fl(pvk_int).encode('utf8')
	res = (b'\x00') * (20 * num)
	ice.privatekey_loop_h160_sse(num, addr_type, iscompressed, pass_int_value, res)
	return res

def privatekey_loop_h160_sse(num, addr_type, iscompressed, pvk_int):
	res = _privatekey_loop_h160_sse(num, addr_type, iscompressed, pvk_int)
	return bytes(bytearray(res))

def _pubkey_to_h160(addr_type, iscompressed, pubkey_bytes):
	res = (b'\x00') * 20
	ice.pubkey_to_h160(addr_type, iscompressed, pubkey_bytes, res)
	return res

def pubkey_to_h160(addr_type, iscompressed, pubkey_bytes):
	res = _pubkey_to_h160(addr_type, iscompressed, pubkey_bytes)
	return bytes(bytearray(res))

# ============================================================================
# ETHEREUM
# ============================================================================

def pubkeyxy_to_ETH_address(pubkey_xy_bytes):
	res = ice.pubkeyxy_to_ETH_address(pubkey_xy_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def _pubkeyxy_to_ETH_address_bytes(pubkey_xy_bytes):
	res = (b'\x00') * 20
	ice.pubkeyxy_to_ETH_address_bytes(pubkey_xy_bytes, res)
	return res

def pubkeyxy_to_ETH_address_bytes(pubkey_xy_bytes):
	res = _pubkeyxy_to_ETH_address_bytes(pubkey_xy_bytes)
	return bytes(bytearray(res))

def privatekey_to_ETH_address(pvk_bytes):
	res = ice.privatekey_to_ETH_address(pvk_bytes)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def _privatekey_to_ETH_address_bytes(pvk_bytes):
	res = (b'\x00') * 20
	ice.privatekey_to_ETH_address_bytes(pvk_bytes, res)
	return res

def privatekey_to_ETH_address_bytes(pvk_bytes):
	res = _privatekey_to_ETH_address_bytes(pvk_bytes)
	return bytes(bytearray(res))

def privatekey_group_to_ETH_address(pvk_bytes, m):
	res = ice.privatekey_group_to_ETH_address(pvk_bytes, m)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def _privatekey_group_to_ETH_address_bytes(pvk_bytes, m):
	res = (b'\x00') * (20 * m)
	ice.privatekey_group_to_ETH_address_bytes(pvk_bytes, m, res)
	return res

def privatekey_group_to_ETH_address_bytes(pvk_bytes, m):
	res = _privatekey_group_to_ETH_address_bytes(pvk_bytes, m)
	return bytes(bytearray(res))

# ============================================================================
# HASH FUNCTIONS
# ============================================================================

def _get_hmac_sha512(key, msg):
	res = (b'\x00') * 64
	ice.get_hmac_sha512(key, len(key), msg, len(msg), res)
	return res

def get_hmac_sha512(key, msg):
	res = _get_hmac_sha512(key, msg)
	return bytes(bytearray(res))

def _get_sha512(data):
	res = (b'\x00') * 64
	ice.get_sha512(data, len(data), res)
	return res

def get_sha512(data):
	res = _get_sha512(data)
	return bytes(bytearray(res))

def _get_sha256(data):
	res = (b'\x00') * 32
	ice.get_sha256(data, len(data), res)
	return res

def get_sha256(data):
	res = _get_sha256(data)
	return bytes(bytearray(res))

def _get_sha256_iter(data, iterations):
	res = (b'\x00') * 32
	ice.get_sha256_iter(data, len(data), res, iterations)
	return res

def get_sha256_iter(data, iterations):
	res = _get_sha256_iter(data, iterations)
	return bytes(bytearray(res))

def _rmd160(data):
	res = (b'\x00') * 20
	ice.rmd160(data, len(data), res)
	return res

def rmd160(data):
	res = _rmd160(data)
	return bytes(bytearray(res))

def _hash160(data):
	res = (b'\x00') * 20
	ice.hash160(data, len(data), res)
	return res

def hash160(data):
	res = _hash160(data)
	return bytes(bytearray(res))

# ============================================================================
# ENCODING
# ============================================================================

def b58_encode(data_hex):
	if type(data_hex) != bytes: data_hex = data_hex.encode('utf-8')
	res = ice.b58_encode(data_hex)
	addr = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return addr

def b58_decode(addr):
	if type(addr) != bytes: addr = addr.encode('utf-8')
	res = ice.b58_decode(addr)
	data_hex = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return data_hex

def bech32_address_decode(coin_type, bech32_addr):
	if type(bech32_addr) != bytes: bech32_addr = bech32_addr.encode('utf-8')
	res = (b'\x00') * 20
	ice.bech32_address_decode(coin_type, bech32_addr, res)
	return bytes(bytearray(res))

# ============================================================================
# KEY OPERATIONS
# ============================================================================

def pubkey_isvalid(pubkey_bytes):
	return ice.pubkey_isvalid(pubkey_bytes)

def _pub_endo1(pubkey_bytes):
	res = (b'\x00') * 33
	ice.pub_endo1(pubkey_bytes, res)
	return res

def pub_endo1(pubkey_bytes):
	res = _pub_endo1(pubkey_bytes)
	return bytes(bytearray(res))

def _pub_endo2(pubkey_bytes):
	res = (b'\x00') * 33
	ice.pub_endo2(pubkey_bytes, res)
	return res

def pub_endo2(pubkey_bytes):
	res = _pub_endo2(pubkey_bytes)
	return bytes(bytearray(res))

# ============================================================================
# MNEMONICS
# ============================================================================

def _mnem_to_masternode(words_bytes, lang):
	res = (b'\x00') * 64
	ice.mnem_to_masternode(words_bytes, len(words_bytes), res)
	return res

def mnem_to_masternode(words_bytes, lang=MNEM_EN):
	res = _mnem_to_masternode(words_bytes, lang)
	return bytes(bytearray(res))

def _create_valid_mnemonics(rbytes, lang):
	res = ice.create_valid_mnemonics(rbytes, len(rbytes), lang)
	mnem = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return mnem

def create_valid_mnemonics(rbytes, lang=MNEM_EN):
	return _create_valid_mnemonics(rbytes, lang)

def pbkdf2_hmac_sha512_dll(words_list):
	bigbuff = b''.join(words_list)
	res = ice.pbkdf2_hmac_sha512_dll(bigbuff, len(words_list))
	mnem = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return mnem

def pbkdf2_hmac_sha512_list(words_list, lang, total):
	bigbuff = b''.join(words_list)
	res = ice.pbkdf2_hmac_sha512_list(bigbuff, len(words_list), len(words_list), lang, total)
	mnem = (ctypes.cast(res, ctypes.c_char_p).value).decode('utf8')
	ice.free_memory(res)
	return mnem

# ============================================================================
# BABY STEP GIANT STEP
# ============================================================================

def create_baby_table(start, end):
	res = (b'\x00') * ((end - start + 1) * 65)
	ice.create_baby_table(start, end, res)
	return bytes(bytearray(res))

# ============================================================================
# BLOOM FILTER
# ============================================================================

def bloom_para(items, fp=0.000001):
	bits = int(-items * math.log(fp) / (math.log(2) ** 2))
	hashes = int((bits / items) * math.log(2))
	return bits, hashes

def fill_in_bloom(inp_list, fp=0.000001):
	bits, hashes = bloom_para(len(inp_list), fp)
	bf = (b'\x00') * (bits // 8)
	for line in inp_list:
		if type(line) != bytes: tt = str(line).encode("utf-8")
		else: tt = line
		ice.bloom_check_add(tt, len(tt), 1, bits, hashes, bf)
	return bits, hashes, bf, fp, len(inp_list)

def dump_bloom_file(output_file, bits, hashes, bf, fp, elem):
	with open(output_file, 'wb') as f:
		pickle.dump((bits, hashes, bf, fp, elem), f)

def read_bloom_file(bloom_file):
	with open(bloom_file, 'rb') as f:
		return pickle.load(f)

def check_in_bloom(line, bits, hashes, bf):
	if type(line) != bytes: tt = str(line).encode("utf-8")
	else: tt = line
	if ice.bloom_check_add(tt, len(tt), 0, bits, hashes, bf) > 0: return True
	else: return False

def create_bsgs_bloom_mcpu(mcpu, total_entries, fp=0.000001):
	if total_entries % (mcpu * 1000) != 0:
		total_entries = mcpu * 1000 * (total_entries // (mcpu * 1000))
		if total_entries == 0: total_entries = mcpu * 1000
		print('[*] Entries adjusted to:', total_entries)
	bits, hashes = bloom_para(total_entries, fp)
	bf = bytes(b'\x00') * (bits // 8)
	print(f'[+] Bloom [bits: {bits}] [hashes: {hashes}] [size: {bits//8} B] [fp: {fp}]')
	ice.create_bsgs_bloom_mcpu(mcpu, total_entries, bits, hashes, bf)
	return bits, hashes, bf, fp, total_entries

# ============================================================================
# BSGS (BABY STEP GIANT STEP)
# ============================================================================

def bsgs_2nd_check_prepare(bP_elem=2000000000):
	if bP_elem < 8000000: bP_elem = 8000000
	ice.bsgs_2nd_check_prepare(bP_elem)

def dump_bsgs_2nd(output_bin_file, verbose=True):
	ice.dump_bsgs_state(output_bin_file.encode("utf-8"), verbose)

def load_bsgs_2nd(input_bin_file, verbose=True):
	ice.load_bsgs_state(input_bin_file.encode("utf-8"), verbose)

def bsgs_2nd_check(pubkey_bytes, z1_int):
	if z1_int < 0: z1_int = N + z1_int
	hex_value = fl(z1_int).encode('utf8')
	res = (b'\x00') * 32
	found = ice.bsgs_2nd_check(pubkey_bytes, hex_value, res)
	return found, res

def bsgs_2nd_check_mcpu(concat_pubkey_bytes, z1_int, mcpu=os.cpu_count()):
	if type(concat_pubkey_bytes) != bytes:
		print("[Error] Input must be bytes")
		return None, None
	num_items = len(concat_pubkey_bytes) // 65
	if z1_int < 0: z1_int = N + z1_int
	hex_value = fl(z1_int).encode('utf8')
	res = (b'\x00') * (32 * num_items)
	found_array = (b'\x00') * num_items
	ice.bsgs_2nd_check_mcpu(concat_pubkey_bytes, num_items, mcpu, hex_value, res, found_array)
	return found_array, res

# ============================================================================
# COLLISION DETECTION
# ============================================================================

def prepare_bin_file_work(in_file, out_file, lower=False):
	use0x = False
	inp_list = [line.split()[0].lower() if lower else line.split()[0] for line in open(in_file, 'r')]
	if inp_list[0][:2] == '0x': use0x = True
	with open(out_file, 'wb') as f:
		if use0x:
			inp_list = [line[2:] for line in inp_list]
		inp_list.sort()
		for line in inp_list:
			f.write(bytes.fromhex(line))

def prepare_bin_file(in_file, out_file, overwrite=False, lower=False):
	if os.path.isfile(out_file) == False:
		prepare_bin_file_work(in_file, out_file, lower)
	else:
		if not overwrite:
			print(f'[+] File {out_file} exists. Using as-is.')
		else:
			print(f'[+] File {out_file} exists. Overwriting...')
			prepare_bin_file_work(in_file, out_file)

def Load_data_to_memory(input_bin_file, verbose=False):
	ice.Load_data_to_memory(input_bin_file.encode("utf-8"), verbose)

def check_collision(h160):
	found = ice.check_collision(h160)
	return found

def check_collision_mcpu(h160_array, num_items=1, mcpu=os.cpu_count()):
	if type(h160_array) == list:
		num_items = len(h160_array)
		h160_array = b''.join(h160_array)
	found_array = (b'\x00') * num_items
	ice.check_collision_mcpu(h160_array, num_items, mcpu, found_array)
	return found_array

# ============================================================================
# XOR FILTER
# ============================================================================

def xor_para(items, fp=0.000001):
	bits = int(-items * math.log(fp) / (math.log(2) ** 2))
	hashes = int((bits / items) * math.log(2))
	return bits, hashes

def fill_in_xor(inp_list, fp=0.000001):
	bits, hashes = xor_para(len(inp_list), fp)
	xf = (b'\x00') * ((bits + 7) // 8)
	for line in inp_list:
		if type(line) != bytes: tt = str(line).encode("utf-8")
		else: tt = line
		res = ice.xor_filter_add(tt, len(tt), bits, hashes, xf)
	del res
	return bits, hashes, xf, fp, len(inp_list)

def dump_xor_file(output_file, bits, hashes, xf, fp, elem):
	with open(output_file, 'wb') as f:
		pickle.dump((bits, hashes, xf, fp, elem), f)

def read_xor_file(xor_file):
	with open(xor_file, 'rb') as f:
		return pickle.load(f)

def check_in_xor(line, bits, hashes, xf):
	if type(line) != bytes: tt = str(line).encode("utf-8")
	else: tt = line
	if ice.xor_filter_check(tt, len(tt), bits, hashes, xf) > 0: return True
	else: return False

def check_in_xor_mcpu(bigbuff, num_items, sz, mcpu, bits, hashes, xf):
	found_array = (b'\x00') * num_items
	ice.xor_filter_check_mcpu(bigbuff, num_items, sz, mcpu, bits, hashes, xf, found_array)
	return found_array

def bsgs_xor_create_mcpu(mcpu, total_entries, fp=0.000001):
	if total_entries % (mcpu * 1000) != 0:
		total_entries = mcpu * 1000 * (total_entries // (mcpu * 1000))
		if total_entries == 0: total_entries = mcpu * 1000
		print('[*] Entries adjusted to:', total_entries)
	bits, hashes = xor_para(total_entries, fp)
	xf = (b'\x00') * ((bits + 7) // 8)
	print(f'[+] XOR [bits: {bits}] [hashes: {hashes}] [size: {len(xf)} B] [fp: {fp}]')
	ice.bsgs_xor_create_mcpu(mcpu, total_entries, bits, hashes, xf)
	return bits, hashes, xf, fp, total_entries
