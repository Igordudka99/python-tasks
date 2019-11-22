import argparse
import random
from collections import OrderedDict

def genkey(args):
	lst = [i for i in range(256)]
	random.shuffle(lst)
	with open(args.output_file, "wb") as f:
		f.write(bytes(lst))
	return 0	

def encrypt(args):
	key_lst = []
	with open(args.key, "rb") as f:
		for i in range(256):
			key_lst.append(int(hex(ord((f.read(1)))), 16))	
	with open(args.input_file, "rb") as in_f, open(args.output_file, "wb") as out_f:
		curr_byte = in_f.read(1)
		while curr_byte:
			sym = [key_lst[int(hex(ord(curr_byte)), 16)]]
			out_f.write(bytes(sym))
			curr_byte = in_f.read(1)
	return 0	

def decrypt(args):
	with open(args.key, "rb") as f:
		key_lst = []
		for i in range(256):
			key_lst.append(int(hex(ord((f.read(1)))), 16))
		rev_key_lst = []	
		for i in range(256):
			rev_key_lst.append(key_lst.index(i))
	with open(args.input_file, "rb") as in_f, open(args.output_file, "wb") as out_f:
		curr_byte = in_f.read(1)
		while curr_byte:
			sym = [rev_key_lst[int(hex(ord(curr_byte)), 16)]]
			out_f.write(bytes(sym))
			curr_byte = in_f.read(1)
	return 0		
	
def hack(args):
	lst = [i for i in range(256)]
	model_dict = {i: 0 for i in lst}
	count = 0
	with open(args.model_file, "rb") as model_f:			#подсчёт байтов в файле модели с помощью словаря
		curr_byte = model_f.read(1)							
		while curr_byte:
			count += 1
			model_dict[int(hex(ord(curr_byte)), 16)] += 1
			curr_byte = model_f.read(1)
	for i in model_dict.keys():
		model_dict[i] = model_dict[i] / count				#вычисление частоты вхождения каждого байта
	model_vals = list(model_dict.values())				
	model_vals.sort()
	model_vals.reverse()
	ord_model_dict = OrderedDict()							#построение упорядоченного словаря,
	for i in model_vals:									#отсортированного по значениям (для модели)
		for k, v in model_dict.items():
			if i == v:
				ord_model_dict[k] = v			
	count = 0
	input_dict = {i: 0 for i in lst}
	with open(args.input_file, "rb") as in_f:				#подсчёт байтов во входном файле с помощью словаря
		for i in in_f.read():
			count += 1
			input_dict[i] += 1
	for i in input_dict.keys():
		input_dict[i] = input_dict[i] / count				#вычисление частоты вхождения каждого байта
	input_vals = list(input_dict.values())
	input_vals.sort()
	input_vals.reverse()
	ord_input_dict = OrderedDict()							#построение упорядоченного словаря,
	for i in input_vals:									#отсортированного по значениям (для входного файла)
		for k, v in input_dict.items():
			if i == v:
				ord_input_dict[k] = v
	model_lst = list(ord_model_dict.keys())
	input_lst = list(ord_input_dict.keys())
	key_lst = []
	for i in range(256):
		key_lst.append(input_lst[model_lst.index(i)])		#создание ключа и последующая запись его в файл
	with open(args.output_file, "wb") as f:
		f.write(bytes(key_lst))
	print("The key is generated!")
	return 0	
		
parser = argparse.ArgumentParser(prog = 'caesar_cipher')
subparsers = parser.add_subparsers(help = 'subparser')

parser_gkey = subparsers.add_parser('genkey', help = 'generate the key')						#парсер генератора
parser_gkey.add_argument(
	'-o', '--output_file', '-file',
	type = str,
	default = 'sec.key',
	help = 'provide a name of file (default: sec.key)'
)
parser_gkey.set_defaults(func = genkey)

parser_enc = subparsers.add_parser('enc', help = 'encrypt a file using a key')					#парсер шифратора
parser_enc.add_argument(
	'-k', '--key',
	type = str,
	default = 'sec.key',
	help = 'provide a name of key file (default: sec.key)'
)
parser_enc.add_argument("input_file")
parser_enc.add_argument(
	'-o', '--output_file',
	type = str,
	default = 'output_file.enc',
	help = 'provide a name of output file (default: input_file.enc)'
)
parser_enc.set_defaults(func = encrypt)

parser_dec = subparsers.add_parser('dec', help = 'decrypt an encrypted file using a key')		#парсер дешифратора
parser_dec.add_argument(
	'-k', '--key',
	type = str,
	default = 'sec.key',
	help = 'provide a name of key file (default: sec.key)'
)
parser_dec.add_argument("input_file")
parser_dec.add_argument(
	'-o', '--output_file',
	type = str,
	default = 'output_file.dec',
	help = 'provide a name of output file (default: output_file.dec)'
)
parser_dec.set_defaults(func = decrypt)

parser_hack = subparsers.add_parser('hack', help = 'decrypt an encrypted file using a model')	#парсер дешифратора с использованием модели
parser_hack.add_argument(
	'-o', '--output_file', '-file',
	type = str,
	default = 'sec.key',
	help = 'provide a name of key file to be generated (default: sec.key)'
)
parser_hack.add_argument("model_file")
parser_hack.add_argument("input_file")
parser_hack.set_defaults(func = hack)

args = parser.parse_args()
args.func(args)