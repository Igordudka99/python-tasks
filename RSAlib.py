import rsa_funcs
from json import dumps as str_dmp
from json import loads as str_load

class RSAKey:
	def __init__(self, power = None, mod = None):
		try:
			if mod != None and mod <= 0: raise Exception("NegModError")
			if power != None and power <= 0: raise Exception("NegPowError")
			if power != None and mod != None and mod <= power: raise Exception("ModPowError")
			else: 
				self._power = power
				self._mod = mod
		except Exception as e:
			print(str(e))
		return	
	
	@property
	def power(self):
		return self._power
		
	@property
	def mod(self):
		return self._mod
		
	@mod.setter
	def mod(self, new_mod):
		try:
			if new_mod <= 0: raise Exception("NegModError")
			if self._power == None: 
				self._mod = new_mod	
			else:
				if new_mod <= self._power: raise Exception("ModPowError")
				else: self._mod = new_mod
		except Exception as e:
			print(str(e))
		return	
	
	@power.setter
	def power(self, new_power):
		try:
			if new_power <= 0: raise Exception("NegPowError")
			if self._mod == None: 
				self._power = new_power	
			else:
				if new_power >= self._mod: raise Exception("ModPowError")
				else: self._power = new_power
		except Exception as e:
			print(str(e))
		return
		
	def __repr__(self):
		str_1 = "RSAKey(power = "
		val = str(self._power)
		if len(val) > 8:
			str_1 = str_1 + val[:8] + "<..%d..>" % (len(val) - 8)
		else:
			str_1 = str_1 + val
		str_1 += ", module = "	
		val = str(self._mod)
		if len(val) > 8:
			str_1 = str_1 + val[:8] + "<..%d..>)" % (len(val) - 8)
		else:
			str_1 = str_1 + val + ")"
		return str_1

	def __str__(self):
		d = {'power' : self._power, 'module' : self._mod}
		return str_dmp(d)
		
	def dump(self, filename = None):
		with open(filename, "w") as f:
			f.write(str(self))
		return	
	
	def load(self, filename = None):
		with open(filename, "r") as f:
			str_1 = f.readline()
		d = str_load(str_1)
		self._power, self._mod = d['power'], d['module']
		return

class RSAPubKey(RSAKey):
	def dump(self, filename = 'rsa.pub'):
		with open(filename, "w") as f:
			f.write(str(self))
		return
	
	def load(self, filename = 'rsa.pub'):
		with open(filename, "r") as f:
			str_1 = f.readline()
		d = str_load(str_1)
		self._power, self._mod = d['power'], d['module']
		return
		
		
class RSASecKey(RSAKey):
	def dump(self, filename = 'rsa.key'):
		with open(filename, "w") as f:
			f.write(str(self))
		return
	
	def load(self, filename = 'rsa.key'):
		with open(filename, "r") as f:
			str_1 = f.readline()
		d = str_load(str_1)
		self._power, self._mod = d['power'], d['module']
		return
	
class RSACrypto:
	def __init__(self, pub_key, sec_key):
		try:
			if pub_key.mod != sec_key.mod: raise Exception("ModNotEqError")
			else:
				self.pub_key, self.sec_key = pub_key, sec_key
		except Exception as e:
			print(str(e))
		return
	
	@property
	def block_len(self):
		return (self.pub_key.mod - 1).bit_length()
	
	def encrypt(self, block):
		return rsa_funcs.powermod(block, self.pub_key._power, self.pub_key._mod)
	
	def decrypt(self, block):
		return rsa_funcs.powermod(block, self.sec_key._power, self.sec_key._mod)
	
	def encrypts(self, message):
		n = self.block_len >> 3
		parts = [message[i:i+n] for i in range(0, len(message), n)]
		res = ''
		for i in parts:
			s = int.from_bytes(bytes(i, 'ascii'), 'big')
			res += hex(self.encrypt(s)) + '\t'
		return res
		
	def decrypts(self, ciphertext):
		res = ''
		ct = ciphertext.split('\t')
		ct.remove('')
		for i in ct:
			s = int(i, 16)
			s = self.decrypt(s)
			tmp = s.to_bytes((s.bit_length() >> 3) + 1, 'big').decode('ascii')
			res += tmp
		return res
	
	def encryptb(self, message):
		n = self.block_len >> 3
		parts = [message[i:i+n] for i in range(0, len(message), n)]
		res = ''
		for i in parts:
			s = int.from_bytes(i, 'big')
			res += hex(self.encrypt(s)) + '\t'
		return res
	
	def decryptb(self, ciphertext):
		res = None
		ct = ciphertext.split('\t')
		ct.remove('')
		for i in ct:
			s = int(i, 16)
			s = self.decrypt(s)
			if s.bit_length() % 8 != 0: tmp = s.to_bytes((s.bit_length() >> 3) + 1, 'big')
			else: tmp = s.to_bytes((s.bit_length() >> 3), 'big')
			if res == None: res = tmp
			else: res += tmp
		return res
		
def gen_keys(half_len = 256):
	p, q = 4, 4
	a, b = 1 << half_len - 1, (1 << half_len) - 1
	p = rsa_funcs.get_next_prime(rsa_funcs.rand(a, b))
	q = rsa_funcs.get_next_prime(rsa_funcs.rand(a, b))
	while  p == q or (p*q).bit_length() != 2 * half_len:
		q = rsa_funcs.get_next_prime(rsa_funcs.rand(a, b))
	N, phi = p*q, (p-1)*(q-1)
	e = rsa_funcs.rand(2, phi)
	while rsa_funcs.gcd(e, phi) != 1:
		e = rsa_funcs.rand(2, phi)
	d = rsa_funcs.inv_elem(e, phi)
	sec_key, pub_key = RSASecKey(d, N), RSAPubKey(e, N)
	return RSACrypto(pub_key, sec_key)