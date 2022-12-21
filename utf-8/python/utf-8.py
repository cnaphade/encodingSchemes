import argparse
import re

def test(text, decoded_codepoints):
	native_func_codepoints = ""
	for i in range(len(text)):
		native_func_codepoints += str(hex(ord(text[i]))) + " "
	
	print(native_func_codepoints)

	if native_func_codepoints == decoded_codepoints:
		print("Algorithm Works!")
	else:
		print("Failure!")

def binary_to_hex(binary_char):
	hexadecimal = ""
	mapping = {}
	for i in range(16):
		if i < 10:
			mapping[i] = str(i)
		else:
			mapping[i] = chr(ord('a') + (i - 10))

	nibbles = re.findall('....?',binary_char[::-1])

	for i in range(len(nibbles)):
		decimal = 0
		for j in range(len(nibbles[i])):
			decimal += int(nibbles[i][j]) * (2 ** j)
		hexadecimal = mapping[decimal] + hexadecimal
	
	idx = 0
	while(hexadecimal[idx] == '0'):
		idx += 1
	return hexadecimal[idx:]	

def utf_8_decode(text):
	octet = 8
	decoded_codepoints = ""

	for i in range(len(text)):
		binary_char = ""
		encoded_char_bytes = bin(int.from_bytes(text[i].encode('utf8'), byteorder='big'))[2:]
		num_bytes = len(encoded_char_bytes) // 8

		if num_bytes < 2:
			binary_char = '0' + encoded_char_bytes
		elif num_bytes > 1:
			binary_char += encoded_char_bytes[num_bytes + 1: octet]
			for j in range(1, num_bytes + 1):
				binary_char += encoded_char_bytes[(octet * j) + 2 : octet * (j + 1)]
				
		decoded_codepoints += "0x" + binary_to_hex(binary_char) + " "

	print(decoded_codepoints)	
	test(text, decoded_codepoints)
	return decoded_codepoints

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--in_file')
	args = parser.parse_args()

	file = open(args.in_file, 'r', encoding='utf-8')
	text = file.read()
	file.close()

	utf_8_decode(text)
	
main()