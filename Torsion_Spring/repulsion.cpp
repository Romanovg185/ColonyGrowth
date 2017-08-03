#include "twovec.h" //Coordinate needs to know what a TwoVec is
#include "coordinate.h" //Particle needs to know what a Coordinate is
#include "global.h"
#include <iostream>
#include <list>
#include <cmath>
#include <vector>
#include <array>
#include <deque>
#include "particle.h"
#include "repulsion.h"
#include "random"

//http://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments#18994296
array<double, 5> shortest_distance(Coordinate a0, Coordinate a1, Coordinate b0, Coordinate b1){
    double EPSILON = 0.0001;

    TwoVec A = a1 - a0;
    TwoVec B = b1 - b0;
    double magA = sqrt(A*A);
    double magB = sqrt(B*B);
    A = A/magA;
    B = B/magB;
    TwoVec C = cross(A, B);
    double D = (sqrt(C.z*C.z))*(sqrt(C.z*C.z));
    // Case that lines are parallel
    if(fabs(D) < EPSILON){
        double d0 = A * (b0 - a0);
        double d1 = A * (b1 - a0);
        if(d0 <= 0 && 0 >= d1){
            if(fabs(d0) < fabs(d1)){
                return array<double, 5>{sqrt((a0 - b0)*(a0 - b0)), a0.x - b0.x, a0.y - b0.y, 0, 0};
            }
            return array<double, 5>{sqrt((a0 - b1)*(a0 - b1)), a0.x - b1.x, a0.y - b1.y, 0, 1};
        }
        else if(d0 >= magA && magA <= d1){
            if(fabs(d0) < fabs(d1)){
                return array<double, 5>{sqrt((a1 - b0)*(a1 - b0)), a1.x - b0.x, a1.y - b0.y, 1, 0};
            }
            return  array<double, 5>{sqrt((a1 - b1)*(a1 - b1)), a1.x - b1.x, a1.y - b1.y, 1, 1};
        }
        TwoVec when_overlap = TwoVec((a0.x + A.x*d0) - b0.x, (a0.y + A.y*d0) - b0.y);
        Coordinate a_halfway = a0 + 0.5*(a1 - a0);
        Coordinate b_halfway = b0 + 0.5*(b1 - b0);
        return array<double, 5>{sqrt(when_overlap*when_overlap), a_halfway.x - b_halfway.x, a_halfway.y - b_halfway.y, 0.5, 0.5};
    }
    // Extended lines cross somewhere
    TwoVec t = b0 - a0;
    double detA = determinant(t, B, C);
    double detB = determinant(t, A, C);

    // These t's vary between 0 and magA or magB, not from 0 to 1;
    double t0 = detA/D;
    double t1 = detB/D;

    // Closest point on infinite line
    Coordinate pA = a0 + (A*t0);
    Coordinate pB = b0 + (B*t1);

    // Clamping, parameters not in [0, 1] but in [0, magA/B]
    if(t0 < 0) pA = a0;
    else if(t0 > magA) pA = a1;
    if(t1 <0) pB = b0;
    else if(t1 > magB) pB = b1;

    // Project A
    if(t0 < 0 || t0 > magB){
        double dot = B*(pA - b0);
        if(dot < 0) dot = 0;
        else if(dot > magB) dot = magB;
        pB = b0 + (B * dot);
    }

    // Project B
    if(t1 < 0 || t1 > magA){
        double dotdot = A*(pB - a0);
        if(dotdot < 0) dotdot = 0;
        else if(dotdot > magA) dotdot = magA;
        pA = a0 + (A*dotdot);
    }

    // Clamps coordinates, but not parameters
    if(t0 < 0) t0 = 0;
    if(t1 < 0) t1 = 0;
    if(t0 > magA) t0 = 1;
    if(t1 > magB) t1 = 1;

    return array<double, 5>{dist(pA, pB), pA.x - pB.x, pA.y - pB.y, t0/magA, t1/magB};

}

///Gets the average position of a particle
Coordinate get_center(Particle &p){
    Coordinate center(0, 0);
    for(Coordinate i : p.positions){
        center.x += i.x;
        center.y += i.y;
    }
    center.x /= (npivot+2);
    center.y /= (npivot+2);
    return center;
}

vector<pair<int, int>> find_indices_repulsion(std::vector<Particle> &plist){
    vector<Coordinate> centers;
    for(Particle &p : plist){
        centers.push_back(get_center(p));
    }
    vector<pair<int, int>> ans;
    int csize = centers.size();
    for(int i = 0; i < csize; ++i){
        for(int j = i+1; j < csize; ++j){
            if(centers[i].x < centers[j].x + d_repulse && centers[i].x > centers[j].x - d_repulse && centers[i].y < centers[j].y + d_repulse && centers[i].y > centers[j].y - d_repulse){
                ans.push_back(pair<int, int>{i, j});
            }
        }
    }
    return ans;
}

void apply_repulsive_force_particle_to_particle(Particle &p1, Particle &p2){
    double d;
    double Ftot;
    TwoVec Fp;
    TwoVec Fq;
    array<double, 5> st; //Contains scalar distance, coordinates of vectorial distance and values of parameter for parametrization line
    for(int i = 0; i < npivot + 1; ++i){
        for(int j = 0; j < npivot + 1; ++j){
            st = shortest_distance(p1.positions[i], p1.positions[i+1], p2.positions[j], p2.positions[j + 1]);
            d = st[0];
            if(d < p1.D){
                Ftot = ko*(d - p1.D);
                Fp = TwoVec(st[1], st[2])*Ftot;
                Fq = -1*Fp;
                p1.forces[i] += Fq*(1 - st[3]);
                p1.pressures[i] += norm(Fq*(1 - st[3]))/p1.len;
                p1.forces[i + 1] += Fq*st[3];
                p1.pressures[i + 1] += norm(Fq*st[3])/p1.len;
                p2.forces[j] += Fp*(1 - st[4]);
                p2.pressures[j] += norm(Fp*(1 - st[4]))/p2.len;
                p2.forces[j + 1] += Fp*st[4];
                p2.pressures[j + 1] += norm(Fp*st[4])/p2.len;
            }
        }
    }
}

void repulsive_force(vector<Particle> &plist){
    vector<pair<int, int>> indices = find_indices_repulsion(plist);
    for(pair<int, int> index_pair : indices){
        apply_repulsive_force_particle_to_particle(plist[index_pair.first], plist[index_pair.second]);
    }
}
