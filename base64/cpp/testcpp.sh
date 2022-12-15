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

	./base64cpp e $input_file $encoded_file
	base64 -i $input_file -o $decoded_file
	#++ base64cpp d $encoded_file $decoded_file

	if cmp -s $encoded_file $decoded_file
		then
			echo $i Algorithm Works!
		else
			echo $i Failure!
	fi
done