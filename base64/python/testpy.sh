#! /bin/bash
random=${1:-"false"}
input_file=../input_file.txt
encoded_file=../encoded.txt
decoded_file=../decoded.txt

if [ $random = "true" ]
	then
		file_size=$(( $RANDOM ))
		openssl rand $file_size > $input_file
fi

python3 base64.py --choice encode --in_file $input_file --out_file $encoded_file
base64 -i $input_file -o $decoded_file
#python3 base64.py --choice decode --in_file $input_file --out_file $decoded_file

if cmp -s $encoded_file $decoded_file
	then
		echo Algorithm Works!
	else
		echo Failure!
fi
