#include <iostream>
#include <cmath>
#include "twovec.h"
#include "global.h"

///Print method
void TwoVec::str(){
    std::cout << "<" << x << "," << y << ">" << std::endl;
}

///Returns an angle between two vectors in the range [0, pi]
double angleBetweenVectors(TwoVec u, TwoVec v){
	return(2*atan2( norm(norm(v)*u - norm(u)*v) , norm(norm(v)*u + norm(u)*v)));
}

//Not related to anything, but often needed so placed high in the dependency tree
///Sine that cuts off
double mySin(double input){
    if(fabs(input) < 0.0001 || fabs(input-3.1415) < 0.0001){
        return 0;
    }
    return sin(input);
}
