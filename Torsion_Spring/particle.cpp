#include <vector>
#include <cmath>
#include <array>
#include <iostream>
#include <boost/random.hpp>
#include "twovec.h"
#include "coordinate.h"
#include "global.h"
#include "repulsion.h"
#include "particle.h"


/// Constructor of the Particle structure
Particle::Particle(double x_start, double y_start, double angle, double rest_length, double diameter, double growth){

    ID = 0;
    D = diameter;
    L = rest_length;
    mu = growth;
    Lmax = max_length;
    len = L*(npivot+1);

    theta = angle;
    positions[0].x = x_start;
    positions[0].y = y_start;
    positions[npivot + 1].x = x_start + L*(npivot + 1)*cos(theta);
    positions[npivot + 1].y = y_start + L*(npivot + 1)*sin(theta);

    for (int i = 1; i <= npivot; i++) {
        positions[i] = Coordinate(x_start + (positions[npivot + 1].x - x_start)/(npivot + 1)*i,
                                  y_start + (positions[npivot + 1].y - y_start)/(npivot + 1)*i);
    }

    for (int i = 0; i < npivot + 2; i++){
        forces[i] = TwoVec(0, 0);
        pressures[i] = 0;
    }
}

///Grows every spring with distance mu
void Particle::grow(){
    L += mu*dt;
}

///Output a couple of interesting facts about a particle
void Particle::str(){
    std::cout << "The ID is: " << ID << '\n';
    std::cout << "The diameter is: " << D << '\n';
    std::cout << "The growth rate is: " << mu << '\n';
    std::cout << "The head-to-head length is: " << len << '\n';
    std::cout << "The rest length each spring needs to have before dividing is: " << Lmax << '\n';
    std::cout << "Each spring has rest length: " << L << '\n';
    for(int i = 0; i <= npivot+1; i++ ){
        std::cout << "The coordinates of pivot " << i << " is: (" << positions[i].x << "," << positions[i].y << ")" << '\n';
    }
    for(int i = 0; i <= npivot+1; i++ ){
        std::cout << "The force on pivot " << i << " is: (" << forces[i].x << "," << forces[i].y << ")" << '\n';
    }
    for(int i = 0; i <= npivot+1; i++ ){
        std::cout << "The pressure on pivot " << i << " is " << pressures[i]  << '\n';
    }
}

///Calculates the internal spring force
void Particle::force_internal(){
    TwoVec dr;
    double len;
    TwoVec fint;
    for(int i = 0; i < npivot + 1; ++i){
        dr = positions[i] - positions[i + 1];
        len = dist(positions[i], positions[i + 1]);
        fint = -ki * (len - L)/len * dr;
        forces[i] += fint;
        forces[i + 1] -= fint;
    }
}

///Prevents the particle from crossing through itself
void Particle::remove_self_overlap(){
    double d;
    double d_rest;
    double Ftot;
    TwoVec v;
    for(int i = 0; i < npivot; ++i){
        for(int j = i+2; j < npivot + 2; ++j){
            d = dist(positions[i], positions[j]);
            d_rest = dist(positions[i], positions[i + 1]);
            if(d < d_rest){
                Ftot = ko*(d - d_rest);
                v = positions[i + 2] - positions[i];
                v = v*(1/(v*v));
                forces[i] += v*Ftot;
                forces[j] += v*Ftot*(-1);
            }
        }
    }
}

///Torsion spring
void Particle::torsion_force(){
    double alpha;
    double torque;
    TwoVec m;
    TwoVec tau_hat;
    TwoVec l1;
    TwoVec l2;
    TwoVec f;
    for(int i = 1; i < npivot + 1; ++i){
        l1 = positions[i] - positions[i - 1];
        l2 = positions[i + 1] - positions[i];
        alpha = angle_between_vectors(l1, l2);
        if(ID == 0)cout << alpha << "," << endl;
        torque = kappa*alpha;
		m = cross(l1, l2);
		if(fabs(m.z) > EPSILON){
            tau_hat.z = m.z/(sqrt(m.z*m.z));
            f = torque/(norm(l1)*norm(l1))*(cross(l1, tau_hat));
            forces[i - 1] += f;
            forces[i] -= f;
            f = torque/(norm(l2)*norm(l2))*(cross(l2, tau_hat));
            forces[i + 1] += f;
            forces[i] -= f;
		}
    }

}

///Moves the particle
void Particle::move(){
    TwoVec vel;
    for(int i = 0; i < npivot + 2; i++){
        vel = forces[i]*(2/dzeta*D);
        positions[i] = positions[i] + vel*dt;
    }
    //Update head-to-head length too
    len = 0;
    for(int j = 0; j < npivot + 1; ++j){
        len += dist(positions[j], positions[j+1]);
    }
}

///Clears the forces after moving
void Particle::clear(){
    TwoVec naught = TwoVec(0, 0);
    for(TwoVec &f : forces){
        f = naught;
    }
    for(double &i : pressures){
        i = 0;
    }
}
