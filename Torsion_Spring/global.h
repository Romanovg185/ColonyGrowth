#ifndef GLOBAL_H_INCLUDED
#define GLOBAL_H_INCLUDED

#include <cmath>
#include <string>

const double EPSILON = 0.00001;
const double pi = 3.14159;

	//Characteristics
const double diameter = 1.0; //diameter should equal 0.75 +- 0.0375 micrometer in real life
const double dzeta = 1.0; //viscous drag coefficient
const double dt = 1; //timestep
const double tau = diameter * dzeta / dt;

	//Parameter
const double AR=7; // division length of a particle used as aspect ratio
const int npivot=1; // number of particles
const double ki=0.1 * tau / (npivot + 1); //internal spring constant, must be smaller than zeta*D*dt/2 otherwise system will explode, good value is 0.25
const double ko=0.2 * tau; //overlap spring constant, halved because every force seems to be applied twice
const int relax_time= 10; //set time to let system relax after growth step
const double growth_rate = 0.0002; // for 1 pivot 0.0002, for 3 pivots 0.00005
const double growth_rate_dev = 0.1 * growth_rate; //sets deviation in growth rate
const double orient_noise = 0.01; //ssets value for noise in orientation of daughter cells to prevent growing in one line
const double kappa= 0.001 *npivot; //torsional spring constant, 0.01 still works but if higher, overshooting can be present

//Constants
const double max_length = diameter * AR / (npivot+1); //sets maximum rest length of a single spring
const double start_length = max_length / 2; //starting length of first set of springs
const int Nmax= 3; //maximum amount of particles
const int write_time=100;
const double d_repulse =  3*AR*diameter;

const std::string path{"/home/romano/Desktop/SourceCode/"};
#endif // GLOBAL_H_INCLUDED
