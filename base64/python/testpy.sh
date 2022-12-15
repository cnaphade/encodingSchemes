#! /bin/bash
random=${1:-"false"}
input_file=../input_file.txt
encoded_file=../encoded.txt
decoded_file=../decoded.txt

for i in {0..40}
do
	if [ $random = "true" ]
		then
			file_size=$(( $RANDOM * 30 ))
			openssl rand $file_size > $input_file
	fi

	python3 base64.py --choice encode --in_file $input_file --out_file $encoded_file
	python3 base64.py --choice decode --in_file $encoded_file --out_file $decoded_file

	if cmp -s $input_file $decoded_file
		then
			echo $i Algorithm Works!
		else
			echo $i Failure!
	fi
done