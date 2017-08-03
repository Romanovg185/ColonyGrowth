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
normal_dist_growth(0.0, growth_rate_dev), //growth distribution added to daughter cells, sigma = 0.277
normal_dist_angle(0.0, orient_noise); //Noise in orientation for daughter cells
boost::variate_generator<boost::mt19937, boost::normal_distribution<> >
random_mu(generator, normal_dist_growth), //generates deviation in growth rate
random_theta(generator, normal_dist_angle); //generates noise in orientation

///Rotate a point p around point c
void rotate_around_point(Coordinate &p, Coordinate c, double angle){
    p = Coordinate(cos(angle) * (p.x - c.x) - sin(angle)* (p.y - c.y) + c.x,
                   sin(angle) * (p.x - c.x) + cos(angle)* (p.y - c.y) + c.y);
}

///Get the sum of lengths from a vector of n coordinates
double get_total_length(vector<Coordinate> &my_points){
    double l = 0;
    for(int i = 0; i < my_points.size()-1; ++i){
        l+=dist(my_points[i], my_points[i + 1]);
    }
    l /= (npivot+1);
	return l;
}

///Finds Coordinate on a line that is a distance l removed from point circleCenter, returning bool to show if it succeeded
pair<Coordinate, bool> equidistant_point_on_line(Coordinate p1, Coordinate p2, Coordinate circleCenter, double radius){
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
void correct_head(std::vector<Coordinate> &first_positions, std::vector<Coordinate> &second_positions, double D){
    TwoVec r = first_positions[first_positions.size() - 2] - first_positions.back();
    TwoVec s = second_positions[second_positions.size() - 2] - second_positions.back();
    //r.str();
    //s.str();
    Coordinate A = first_positions.back();
    r = r/norm(r);
    s = s/norm(s);
    double lambda = sqrt(1/( (r.x - s.x)*(r.x - s.x) + (r.y - s.y)*(r.y - s.y) ));
    if(lambda < 0) lambda = -lambda;
    Coordinate P = A + lambda*r;
    Coordinate Q = A + lambda*s;
    first_positions.back() = P;
    second_positions.back() = Q;
}

void relax(std::vector<Coordinate> &my_array){
    std::deque<std::pair<Coordinate, Coordinate>> possible_lines;
    for(size_t i = 0; i < my_array.size() - 1; ++i){
        possible_lines.push_back(std::pair<Coordinate, Coordinate>{my_array[i], my_array[i+1]});
    }
    std::vector<Coordinate> fixed;
    fixed.push_back(my_array.front());
    double relaxed_length = get_total_length(my_array);
    std::pair<Coordinate, bool> my_data; // Return type of equidistantPointOnLine
    for(int i = 0; i < npivot; ++i){
        bool flag = false;
        while(!flag){
            std::pair<Coordinate, Coordinate> line_currently_checked{possible_lines.front()};
            my_data = equidistant_point_on_line(possible_lines.front().first, possible_lines.front().second, fixed[i], relaxed_length);
            flag = my_data.second;
            if(!flag){
                possible_lines.pop_front();
            }
        }
        fixed.push_back(my_data.first);
        possible_lines.front().first = my_data.first;
    }
    fixed.push_back(my_array.back()); // To prevent off-by-one errors
    my_array.clear();
    for(Coordinate foo : fixed) my_array.push_back(foo);
}

vector<Coordinate> prepare_position_vector(Particle &p, int number){
    vector<Coordinate> positions;
    if(number == 1){
        for(int i = 0; i < (npivot+1)/2 + 1; i++) positions.push_back(p.positions[i]);
    }
    else if(number == 2){
        for(int i = npivot+1; i >= (npivot+1)/2; i--) positions.push_back(p.positions[i]);
    }
    return positions;
}

void set_rest_length_after_division(Particle &p){
    double total_length;
    for(int i = 0; i < npivot + 1; i++) total_length += dist(p.positions[i], p.positions[i+1]);
    p.len = total_length;
    p.L = total_length/(npivot+1);
}

///Divides the particles by performing the following steps:
// 1. Divides the old points over 2 new particles of which one passed in blank
// 2. Shifts the head such that at the division planes the particles do not overlap using correctHead()
// 3. Interpolates using relax() to make all internal springs relaxed
void divide(Particle &p_old, Particle &p_new){
    // Find middle point of particle
    int split = (npivot+1)/2;

    // Inherit (in the biological sense) from the mother cell
    p_new.mu = p_old.mu + random_mu(); //Growth noise instead of length noise
    p_old.mu += random_mu();
    p_new.Lmax = p_old.Lmax;
    p_new.D = p_old.D;

    // Insert points of old particle for relaxation
    vector<Coordinate> first_positions = prepare_position_vector(p_old, 1);
    vector<Coordinate> second_positions = prepare_position_vector(p_old, 2);

    // Correct the head at division plane
    correct_head(first_positions, second_positions, p_old.D);

    // Remove tension from all springs but one
    if(npivot > 1){
        relax(first_positions);
        relax(second_positions);
    } else {
        first_positions.push_back(first_positions[1]);
        first_positions[1] = first_positions[0] + ((first_positions[2] - first_positions[0])*0.5);
        second_positions.push_back(second_positions[1]);
        second_positions[1] = second_positions[0] + ((second_positions[2] - second_positions[0])*0.5);
    }

    // Copy back into the array property of Particle, the STL algorithms are apparently a good pal :)
    array<Coordinate, npivot+2> new_position_array;
    copy(first_positions.begin(), first_positions.begin() + npivot + 2, new_position_array.begin());
    p_new.positions = new_position_array;
    copy(second_positions.begin(), second_positions.begin() + npivot + 2, new_position_array.begin());
    p_old.positions = new_position_array;

    // Angle noise
    double random_angle = random_theta();
    for(Coordinate &c : p_new.positions) rotate_around_point(c, p_new.positions.front(), random_angle);
    random_angle = random_theta();
    for(Coordinate &c : p_old.positions) rotate_around_point(c, p_old.positions.front(), random_angle);

        cout << "First" << endl;
    for(Coordinate i : p_old.positions) cout << i << endl;
    cout << "Second" << endl;
    for(Coordinate i : p_old.positions) cout << i << endl;

    // Set rest length equal to total particle length divided by number of springs
    set_rest_length_after_division(p_old);
    set_rest_length_after_division(p_new);
}
