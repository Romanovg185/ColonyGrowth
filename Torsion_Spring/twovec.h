#ifndef TWOVEC_H_INCLUDED
#define TWOVEC_H_INCLUDED

#include <cmath>
#include <iostream>

using namespace std;

struct TwoVec{
    // Empty constructor
    TwoVec() : x(0), y(0), z(0) {}
    // Default constructor
    TwoVec(double xin, double yin) : x(xin), y(yin), z(0) {}

    // Coordinates, z defaults to 0, but is possible to be altered to make a 3D model
    double x;
    double y;
    double z;

    // Operators are overloaded, so normal arithmetic can be done with vectors
    TwoVec operator+(TwoVec v) {
        return TwoVec(x + v.x, y + v.y);
    }

    TwoVec& operator+=(const TwoVec& v) {
        this->x += v.x;
        this->y += v.y;
        this->z += v.z;
        return *this;
    }

    TwoVec operator-(TwoVec v) {
        return TwoVec(x - v.x, y - v.y);
    }

    TwoVec& operator-=(const TwoVec& v) {
        this->x -= v.x;
        this->y -= v.y;
        this->z -= v.z;
        return *this;
    }

    TwoVec operator*(double d) {
        return TwoVec(d*x, d*y);
    }

    TwoVec operator/(double d) {
        return TwoVec(x/d, y/d);
    }

    double operator*(TwoVec myvec) {
        return (x*myvec.x + y*myvec.y);
    }

    // First way to print a TwoVec
	  void str(){
	      cout << "<" << x << "," << y << ">" << endl;
	  }
};

// Second way to make a print of a TwoVec
static std::ostream& operator<<(std::ostream &os, const TwoVec &my_twovec){
	os << "<" << my_twovec.x << "," << my_twovec.y << ">";
	return os;
}

// Also operator overloading
static TwoVec operator*(double d, TwoVec v) {
    return TwoVec(d*v.x, d*v.y);
}

// Cross product
static TwoVec cross(TwoVec u, TwoVec v) {
    TwoVec ans;
    ans.x = (u.y * v.z) - (u.z * v.y);
    ans.y = (u.z * v.x) - (u.x * v.z);
    ans.z = (u.x * v.y) - (u.y * v.x);
    return ans;
}

// Determinant
static double determinant(TwoVec a, TwoVec b, TwoVec c) {
    double x = b.y * c.z - c.y * b.z;
    double y = a.y * c.z - c.y * a.z;
    double z = a.y * b.z - b.y * a.z;
    return a.x*x - b.x*y + c.x*z;
}

// Norm of a vector
static double norm(TwoVec a) {
    return sqrt(a*a);
}

// Returns an angle between two vectors in the range [0, pi]
static double angle_between_vectors(TwoVec u, TwoVec v){
	return(2*atan2( norm(norm(v)*u - norm(u)*v) , norm(norm(v)*u + norm(u)*v)));
}

#endif // TWOVEC_H_INCLUDED
