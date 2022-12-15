test: base64cpp
	./testcpp.sh $(random)

base64cpp: base64.o
	g++ base64.o -o base64cpp

base64.o: base64.cpp
	g++ -c base64.cpp

clean:
	rm *.o