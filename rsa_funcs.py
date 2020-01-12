from random import randint as rand

def gcd(a, b):
	while a != b:
		if a > b: a = a - b
		else: b = b - a
	return a

def powermod(a, b, mod):
	base = a
	p = b
	n = 1
	while p:
		if p & 1:
			n *= base
		p >>= 1
		base *= base
		base %= mod
		n %= mod
	return n
	
def rabin_miller_test(n, log_precision = 128):
	k, s, x = int(log_precision >> 2), 0, n - 1
	while x % 2 == 0:
		s += 1
		x >>= 1
	t = x
	for i in range(k):
		a = rand(2, n-1)
		x = powermod(a, t, n)
		flag = False
		if x == 1 or x == n - 1:
			continue
		for i in range(s-1):
			x = powermod(x, 2, n)
			if x == 1: 
				return False
			if x == n - 1:
				flag = True
				break
		if flag:
			continue
		return False
	return True

def is_prime(n, test_func = rabin_miller_test, func_args = None):
	return test_func(n)

def get_next_prime(edge, test_func = rabin_miller_test, func_args = None):
	i = edge
	while not is_prime(i, test_func):
		i += 1
	return i

def inv_elem(num, mod):
	n, m = num, mod
	x, r = 1, 0
	while m:
		q = n // m
		n, m = m, n % m
		x, r = r, x - r*q
	if x < 0: x += mod
	return x


	
if __name__ == "__main__":
	print("RSA auxiliary functions: is_prime(), rabin_miller_test(), get_next_prime(), gcd(), powermod(), inv_elem()")