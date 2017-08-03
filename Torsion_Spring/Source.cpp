#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <ctime> // time_t
#include <cstdio>
#include <array>
#include <fstream>
#include <tuple>
#include "twovec.h" //Coordinate needs to know what a TwoVec is
#include "coordinate.h" //Particle needs to know what a Coordinate is
#include "global.h" //Particle needs to access the global variables
#include "repulsion.h"
#include "particle.h" // All clean and tidy in its own file
#include "division.h"

using namespace std;

///Master function growAll
void grow_all(vector<Particle> &p, int ts){
    int length_before = p.size(); //Since a particle cannot divide twice during the same growAll() call, only loop over the initial amount of particles
    for(int i = 0; i < length_before; i++){ //Unable to be range based since the ranging object changes length, leading to an infinite loop
        p[i].grow();
        if(p[i].L > p[i].Lmax){
            //p[i].str();
            Particle pnew = Particle(0, 0, 0, 0, diameter, 0); //Necessary copy of all old parameters
            p.push_back(pnew); //Add new particle to p
            divide(p[i], p.back()); //Set new properties of daughter particles
            p.back().ID = p.size() - 1; //Set new particle ID
            p[i].str();
            p.back().str();
            //std::cout << "Division number " << p.size() - 1 << " has occurred at time step " << ts << std::endl;
        }
    }
}

///Master function moveAll
void move_all(vector<Particle> &p){
    for(Particle &part : p){
        part.clear(); //Put on top to be able to monitor the forces after a time step
    }
    repulsive_force(p);
    for(Particle &part : p){
		part.force_internal();
        part.remove_self_overlap();
        part.torsion_force();
		part.move();
    }
}

void write_all(vector<Particle> &p, ofstream &out_stream, int ts){
    for(Particle &part : p){
        out_stream << ts << " ";
        out_stream << part.ID << " ";
        out_stream << part.D << " ";
        for(Coordinate &coord : part.positions){
            out_stream << coord.x << "," << coord.y << " ";
        }
        for(TwoVec &tv : part.forces){
            out_stream << tv.x << "," << tv.y << " ";
        }
        for(double &d : part.pressures){
            out_stream << d << " ";
        }
		out_stream << ";";
    }
    out_stream << std::endl;
}

void run(string file_name){
	cout << path << endl;
    ofstream out_stream;
    out_stream.open(path);
    Particle Test(0, 0, 0, start_length, diameter, growth_rate);
    vector<Particle> p;
	p.reserve(Nmax);
	p.push_back(Test);
    int ts = 0;
    do{
        if(ts % relax_time == 0) grow_all(p, ts);
        if(ts % write_time == 0) write_all(p, out_stream, ts);
        move_all(p);
        ts++;
    } while(p.size() < Nmax);
    out_stream.close();
}

int main(int argc, char* argv[]){
string stringy(argv[1]);
clock_t before;
before = clock();
run(stringy);
clock_t t = clock() - before;
std::cout << t/CLOCKS_PER_SEC << std::endl;
return 0;
}
