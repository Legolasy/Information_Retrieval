#include <iostream>
#include <string>
#include <direct.h>
#include <io.h>
#include "Statistics.h"
using namespace std;



void main() {

	Statistics statistics = Statistics("./data");
	cout << "\n ------------------------- \n\n";
	statistics.display();

	statistics.user_search();
}
