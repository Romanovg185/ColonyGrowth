#include "twovec.h" //Coordinate needs to know what a TwoVec is
#include "coordinate.h" //Particle needs to know what a Coordinate is
#include "global.h"
#include <iostream>
#include <list>
#include <cmath>
#include <vector>
#include <array>
#include <deque>
#include <tuple>
#include <boost/random.hpp>
#include "particle.h"
#include "division.h"

//Random number generator
boost::mt19937 generator(time(0)); //number generator from random list
boost::normal_distribution<> //setup distributions
normalDistGrowth(0.0, growthRateDev), //growth distribution added to daughter cells, sigma = 0.277
normalDistAngle(0.0, orientNoise), //Noise in orientation for daughter cells
normalDistLength(maxLength, maxLengthDev); //distribution of maximum length that particles can reach, 4.54, sigma = 0.46
boost::variate_generator<boost::mt19937, boost::normal_distribution<> >
randomMu(generator, normalDistGrowth), //generates deviation in growth rate
randomTheta(generator, normalDistAngle), //generates noise in orientation
randomLmax(generator, normalDistLength); //generates division lengths

///Finds Coordinate on a line that is a distance l removed from point circleCenter, returning bool to show if it succeeded
std::pair<Coordinate, bool> equidistantPointOnLine(Coordinate p1, Coordinate p2, Coordinate circleCenter, double radius){
    TwoVec d = p2 - p1;
    TwoVec f = p1 - circleCenter;
    double a = d*d;
    double b = f*d*2;
    double c = f*f - radius*radius;

    double D = b*b-4*a*c;
    if(D >= 0){
        D = sqrt(D);
        float t1 = (-b - D)/(2*a);
        float t2 = (-b + D)/(2*a);
        if(t1 >= 0 && t1 <= 1){
            return std::pair<Coordinate, bool>{p1 + (d*t1), true};
        }
        if(t2 >= 0 && t2 <= 1){
            return std::pair<Coordinate, bool>{p1 + (d*t2), true};
        }
    }
    return std::pair<Coordinate, bool>{Coordinate(0,0), false}; // If no equidistant point is found, a coordinate that is over nine thousand will be returned
}

///Makes sure that the two points at the division plane are distance D apart, even when old points have to be removed to make that possible
void correctHead(std::vector<Coordinate> &firstPositions, std::vector<Coordinate> &secondPositions, double D){
    TwoVec r = firstPositions[firstPositions.size() - 2] - firstPositions.back();
    TwoVec s = secondPositions[secondPositions.size() - 2] - secondPositions.back();
    r.str();
    s.str();
    Coordinate A = firstPositions.back();
    r = r/norm(r);
    s = s/norm(s);
    double lambda = sqrt(1/( (r.x - s.x)*(r.x - s.x) + (r.y - s.y)*(r.y - s.y) ));
    if(lambda < 0) lambda = -lambda;
    Coordinate P = A + lambda*r;
    Coordinate Q = A + lambda*s;
    firstPositions.back() = P;
    secondPositions.back() = Q;
}

void relax(std::vector<Coordinate> &myArray){
    std::deque<std::pair<Coordinate, Coordinate>> possibleLines;
    for(size_t i = 0; i < myArray.size() - 1; ++i){
        possibleLines.push_back(std::pair<Coordinate, Coordinate>{myArray[i], myArray[i+1]});
    }
    std::vector<Coordinate> fixed;
    fixed.push_back(myArray.front());
    double relaxedLength = getTotalLength(myArray);
    std::pair<Coordinate, bool> myData; // Return type of equidistantPointOnLine
    for(int i = 0; i < npivot; ++i){
        bool flag = false;
        while(!flag){
            std::pair<Coordinate, Coordinate> lineCurrentlyChecked{possibleLines.front()};
            myData = equidistantPointOnLine(possibleLines.front().first, possibleLines.front().second, fixed[i], relaxedLength);
            flag = myData.second;
            if(!flag){
                possibleLines.pop_front();
            }
        }
        fixed.push_back(myData.first);
        possibleLines.front().first = myData.first;
    }
    fixed.push_back(myArray.back()); // To prevent off-by-one errors
    myArray.clear();
    for(Coordinate foo : fixed) myArray.push_back(foo);
}

///Makes it such that all points besides the last one are both on the initial lines and equidistant and therefore relaxed
void oldRelax(std::vector<Coordinate> &myArray){
    std::deque<Coordinate> myDeq;
    for(Coordinate i : myArray){
        myDeq.push_back(i); // Fill the double-ended queue (sort of like a two-headed vector) up with all coordinates
    }
    std::vector<Coordinate> fixed; // Contains the relaxed points
    fixed.push_back(myDeq[0]);
    myDeq.pop_front(); // Move the zeroth element, that is relaxed by definition, to the fixed vector

    double l = getTotalLength(myArray); // Relaxation length
    bool flag = false;
    std::pair<Coordinate, bool> myData; // Return type of equidistantPointOnLine

    for(int i = 0; i < npivot; ++i){
        while(!flag){
            myData = equidistantPointOnLine(fixed[i], myDeq.front(), fixed[i], l);
            flag = myData.second;
            if(!flag){
                myDeq.pop_front(); // Pop the line if the point is passed
            }
        }
        fixed.push_back(myData.first);
        flag = false;
    }
    fixed.push_back(myArray.back()); // To prevent off-by-one errors
	myArray.clear();
	for(Coordinate foo : fixed) myArray.push_back(foo);
}

///Divides the particles by performing the following steps:
// 1. Divides the old points over 2 new particles of which one passed in blank
// 2. Shifts the head such that at the division planes the particles do not overlap using correctHead()
// 3. Interpolates using relax() to make all internal springs relaxed
void divide(Particle &pOld, Particle &pNew){
    // Find middle point of particle
    int split = (npivot+1)/2;
    pNew.mu = pOld.mu + randomMu(); //Growth noise instead of length noise
    pOld.mu += randomMu();
    pNew.Lmax = pOld.Lmax;
    pNew.D = pOld.D;

    // Insert points of old particle for relaxation
    std::vector<Coordinate> firstPositions;
    std::vector<Coordinate> secondPositions;
    firstPositions.push_back(pOld.positions[0]);
    for(int i = 0; i < (npivot-1)/2; i++){
        firstPositions.push_back(pOld.positions[i+1]);
    }
    firstPositions.push_back(pOld.positions[split]);

    secondPositions.push_back(pOld.positions[npivot+1]);
    for(int i = npivot; i > split; i--){
        secondPositions.push_back(pOld.positions[i]);
    }
    secondPositions.push_back(pOld.positions[split]);

    correctHead(firstPositions, secondPositions, pOld.D);

    // Remove tension from all springs but one
    if(npivot > 1) relax(firstPositions);
	else if(npivot == 1){
		firstPositions.push_back(firstPositions[1]);
		firstPositions[1] = firstPositions[0] + ((firstPositions[2] - firstPositions[0])*0.5);
	}

    std::array<Coordinate, npivot+2> newPositionArray;
    for(int i = 0; i < npivot+2; ++i){
        newPositionArray[i] = firstPositions[i];
    }
    pNew.positions = newPositionArray;

    // Angle noise
	double randomAngle = randomTheta();
    for(int i = 0; i < npivot + 1; ++i){
            pNew.positions[i] = rotateAroundPoint(pNew.positions[i], pNew.positions.back().x, pNew.positions.back().y, randomAngle); //Angle noise!
    }

    // Set rest length equal to total particle length divided by number of springs
    double totalLength;
    for(int i = 0; i < npivot + 1; i++){
        totalLength += dist(pNew.positions[i], pNew.positions[i+1]);
    }
    pNew.len = totalLength;
    pNew.L = totalLength/(npivot+1);

    // ---Right particle pOld---

    // ---Update old particle from the right half of the particle positions---
    // Remove tension from all springs but one
    if(npivot > 1) relax(secondPositions);
	else if(npivot == 1){
		secondPositions.push_back(secondPositions[1]);
		secondPositions[1] = secondPositions[0] + ((secondPositions[2] - secondPositions[0])*0.5);
	}
    for(int i = 0; i < npivot+2; ++i){
        newPositionArray[i] = secondPositions[i];
    }
    pOld.positions = newPositionArray;

    // Angle noise
	randomAngle = randomTheta();
    for(int i = 0; i < npivot + 1; ++i){
            pOld.positions[i] = rotateAroundPoint(pOld.positions[i], pOld.positions.back().x, pOld.positions.back().y, randomAngle); //Angle noise!
    }

    // Set rest length equal to total particle length divided by number of springs
    totalLength = 0;
    for(int i = 0; i < npivot + 1; i++){
        totalLength += dist(pOld.positions[i], pOld.positions[i+1]);
    }
    pOld.len = totalLength;
    pOld.L = totalLength/(npivot+1);

}
