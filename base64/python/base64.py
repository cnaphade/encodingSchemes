import argparse

def base64mapping():
	mapping = {}
	for i in range(64):
		if i < 26:
			mapping[i] = chr(ord('A') + i)
			mapping[chr(ord('A') + i)] = i
		elif i < 52:
			mapping[i] = chr(ord('a') + i - 26)
			mapping[chr(ord('a') + i - 26)] = i
		elif i < 62:
			mapping[i] = str(i - 52)
			mapping[str(i - 52)] = i
		elif i == 62:
			mapping[i] = '+'
			mapping['+'] = i
		elif i == 63:
			mapping[i] = '/'
			mapping['/'] = i
	return mapping

def base64encode(text, mapping):
	binary = 2
	sextet = 6
	output = ""
	remainder_bits = ""

	for i in range(len(text)):
		current_byte = int.from_bytes(text[i:i+1], byteorder = 'big')
		current_byte = bin(current_byte)[2:].rjust(8, '0')
		
		bits_to_include = max(0, sextet - len(remainder_bits))
		current_bits = remainder_bits + current_byte[:bits_to_include]
		remainder_bits = current_byte[bits_to_include:]
		
		output += mapping[int(current_bits, binary)]
		if(len(remainder_bits) >= sextet):
			output += mapping[int(remainder_bits[:sextet], binary)]
			remainder_bits = remainder_bits[sextet:]

	if (len(remainder_bits) > 0):
		output += mapping[int(remainder_bits.ljust(sextet, '0'), binary)]
	padding_size = len(output) % 4
	output += '=' * padding_size
	return output


def base64decode(text, mapping):
	# remember to use to_bytes() to convert int from binary string back to byte
	return 0

def main(mapping):
	parser = argparse.ArgumentParser()
	parser.add_argument('--choice')
	parser.add_argument('--in_file')
	parser.add_argument('--out_file')
	args = parser.parse_args()

	if args.choice == 'encode':
		file = open(args.in_file, 'rb')
		text = file.read()
		file.close()
		encoded = open(args.out_file, 'w')
		encoded.write(base64encode(text, mapping) + '\n')
		encoded.close()
	elif args.choice == 'decode':
		file = open(args.in_file, 'r')
		text = file.read()
		file.close()
		decoded = open(args.out_file, 'wb')
		decoded.write(base64decode(text, mapping))
		decoded.close()

main(base64mapping())