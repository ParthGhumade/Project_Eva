#include <iostream>
#include <String>
using namespace std;

int main() {
	String inp = "M:100";

	cout << inp.substring(2).toInt() << endl;
}