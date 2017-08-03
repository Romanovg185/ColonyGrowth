#ifndef DIVISION_H_INCLUDED
#define DIVISION_H_INCLUDED

std::pair<Coordinate, bool> equidistantPointOnLine(Coordinate p1, Coordinate p2, Coordinate circleCenter, double radius);
void correctHead(std::vector<Coordinate> &first, std::vector<Coordinate> &second, double D);
void relax(std::vector<Coordinate> &myArray);
void divide(Particle &pOld, Particle &pNew);

#endif // DIVISION_H_INCLUDED
