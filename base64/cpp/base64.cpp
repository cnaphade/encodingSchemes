#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <bitset>
using namespace std;

map<int, char> base64emapping() {
	map<int, char> mapping;
	for (int i = 0; i < 64; i++) {
		if (i < 26) {
			mapping.insert(make_pair(i, char('A' + i)));
		}
		else if (i < 52) {
			mapping.insert(make_pair(i, char('a' + i - 26)));
		}
		else if (i < 62) {
			mapping.insert(make_pair(i, char('0' + i - 52)));
		}
		else if (i == 62) {
			mapping.insert(make_pair(i, '+'));
		}
		else if (i == 63) {
			mapping.insert(make_pair(i, '/'));
		}
	}
	return mapping;
}

map<char, int> base64dmapping() {
	map<char, int> mapping;
	for (int i = 0; i < 64; i++) {
		if (i < 26) {
			mapping.insert(make_pair(char('A' + i), i));
		}
		else if (i < 52) {
			mapping.insert(make_pair(char('a' + i - 26), i));
		}
		else if (i < 62) {
			mapping.insert(make_pair(char('0' + i - 52), i));
		}
		else if (i == 62) {
			mapping.insert(make_pair('+', i));
		}
		else if (i == 63) {
			mapping.insert(make_pair('/', i));
		}
	}
	return mapping;
}

string base64encode(string text, map<int, char> mapping) {
	int binary = 2;
	int sextet = 6;
	int octet = 8;
	string output = "";
	string remainder_bits = "";

	for (int i = 0; i < text.length(); i++) {
		string current_byte = bitset<8>(text[i]).to_string();
		int bits_to_include = max(0, int(sextet - remainder_bits.length()));
		string current_bits = remainder_bits + current_byte.substr(0, bits_to_include);
		remainder_bits = current_byte.substr(bits_to_include);

		output += mapping[stoi(current_bits, 0, 2)];
		if (remainder_bits.length() >= sextet) {
			output += mapping[stoi(remainder_bits.substr(0, sextet), 0, 2)];
			remainder_bits = remainder_bits.substr(sextet);
		}
	}

	if (remainder_bits.length() > 0) {
		int additional_bits = sextet - remainder_bits.length();
		output += mapping[stoi(remainder_bits + string(additional_bits, '0'), 0, 2)];
	}
	int padding_size = output.length() % 4;
	output += string(padding_size, '=') + '\n';
	
	return output;
}

string base64decode(string text, map<char, int> mapping) {
	int binary = 2;
	int sextet = 6;
	int octet = 8;
	string output = "";
	string current_bits = "";
	
	for (int i = 0; i < text.length(); i++) {
		if (text[i] == '=') break;

		current_bits += bitset<6>(mapping[text[i]]).to_string();
		if (current_bits.length() >= octet) {
			output += stoi(current_bits.substr(0, octet), 0, 2);
			current_bits = current_bits.substr(octet);
		}
	}
	
	return output;
}

int main(int argc, char *argv[]) {
	char choice;
	string in_file;
	string out_file;
	if (argc == 4) {
		choice = *argv[1];
		in_file = argv[2];
		out_file = argv[3];
	}
	else return 0;

	ifstream ifs(in_file, ios::in | ios::binary);
		string text((istreambuf_iterator<char>(ifs)),
					(istreambuf_iterator<char>()));
		ifs.close();

	if (choice == 'e') {
		map<int, char> mapping = base64emapping();
		string base64text = base64encode(text, mapping);
		ofstream encoded(out_file, ios::out | ios::binary);
		encoded.write(base64text.c_str(), base64text.length());
		encoded.close();
	}
	else if (choice == 'd') {
		map<char, int> mapping = base64dmapping();
		string base64text = base64decode(text, mapping);
		ofstream decoded(out_file, ios::out | ios::binary);
		decoded.write(base64text.c_str(), base64text.length());
		decoded.close();
	}
}