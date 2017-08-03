#ifndef COORDINATE_H_INCLUDED
#define COORDINATE_H_INCLUDED

#include <vector>
#include <cmath>
#include <iostream>
#include "global.h"

using namespace std;

struct Coordinate{
    double x;
    double y;

    Coordinate() : x(0), y(0) {}
    Coordinate(double xin, double yin) : x(xin), y(yin) {}

    Coordinate operator+(TwoVec v) {
        return Coordinate(x + v.x, y + v.y);
    }
    Coordinate operator-(TwoVec v) {
        return Coordinate(x + v.x, y + v.y);
    }

    TwoVec operator-(Coordinate mycoord) {
        return TwoVec(x - mycoord.x, y - mycoord.y);
    }

	///Print statement for TwoVec
    void str(){
   	    cout << "<" << x << "," << y << ">" << endl;
	  }
};

static std::ostream& operator<<(std::ostream &os, const Coordinate &my_coordinate){
	os << "<" << my_coordinate.x << "," << my_coordinate.y << ">";
	return os;
}

// Some useful functions that take Coordinates
static double dist(Coordinate s1, Coordinate s2) {
    return sqrt((s1.y - s2.y)*(s1.y - s2.y) + (s1.x - s2.x)*(s1.x - s2.x));
}
static double ang(Coordinate s1, Coordinate s2) {
    return atan2(s1.y - s2.y, s1.x - s2.x);
}





#endif // COORDINATE_H_INCLUDED
