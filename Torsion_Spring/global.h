#ifndef GLOBAL_H_INCLUDED
#define GLOBAL_H_INCLUDED

#include <cmath>
const double EPSILON = 0.000001;
const double pi = 3.14159;

	//Characteristics
const double diameter = 1.0; //diameter should equal 0.75 +- 0.0375 micrometer in real life
const double dzeta = 1.0; //viscous drag coefficient
const double dt = 1; //timestep
const double tau = diameter * dzeta / dt;

	//Parameter
const double maxLoverD=7; //gives relation between straight length of particle and D
const int npivot=3; //((int)(floor(maxLoverD) - 1)) + ((int)(floor(maxLoverD)-1)%2 - 1); //number of pivots, np=floor(maxLoverD - 1) rounded down till odd
const double ki=0.1 * tau / (npivot + 1); //internal spring constant, must be smaller than zeta*D*dt/2 otherwise system will explode, good value is 0.25
const double ko=0.2 * tau; //overlap spring constant, halved because every force seems to be applied twice
const int relaxTime= 10; //set time to let system relax after growth step
const double growthRate = 150E-6; //0.0000025 * tau * relaxTime; //number gives growth rate per time step. exp: 1.23 per hour, small compared to ki for relaxation
const double growthRateDev = 0.1 * growthRate; //sets deviation in growth rate
const double maxLengthDev = 0.02 * diameter * maxLoverD; //sets deviation in max length
const double orientNoise = 0.01; //ssets value for noise in orientation of daughter cells to prevent growing in one line
const double kappa=0.05 / npivot; //torsional spring constant, 0.001 is very stiff but still somewhat noticeable, 0.0001 is nice, 0.00001 is too floppy

const double restAngle = pi;

//Constants
const double maxLength = diameter * maxLoverD / (npivot+1); //sets mean maximum length of a single spring
const double startLength = maxLength / 2; //starting length of first set of springs
const int Nmax= 12; //maximum amount of particles
const int writeTime=100;
//const double repulsionSelection = 3*maxLoverD*diameter;
const double dRepulse =  3*maxLoverD*diameter;

const bool onCluster = true;

#endif // GLOBAL_H_INCLUDED
