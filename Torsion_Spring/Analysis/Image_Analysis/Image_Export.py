import matplotlib as mpl
mpl.use('Agg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import colorsys as col
from PIL import Image
import Colony_Properties as prop
import os
import sys

#========================================
D = 1.0
n_boxes = 4
#========================================
class ParticleData(object):
    def __init__(self):
        self.ts = 0
        self.ID = 0
        self.D = 0
        self.positions = []
        self.forces = []
        self.pressures = []
        self.center = 0

    def setPosition(self, inp):
        self.positions.append(inp)

    def setForce(self, inp):
        self.forces.append(inp)

    def setPressure(self, inp):
        self.pressures.append(inp)

    def setCenter(self):
        myCenter = [0.0, 0.0]
        for point in self.positions:
            myCenter[0] += point[0]
            myCenter[1] += point[1]
        self.center = tuple(myCenter)

    def __str__(self):
        stringy = ["Time step is " + str(self.ts) + "\n"]
        stringy.append("Particle ID is " + str(self.ID) + "\n")
        stringy.append("Diameter is " + str(self.D) + "\n")
        for i, pos in enumerate(self.positions):
            stringy.append("Position {} has coordinates ({},{}) \n".format(i, self.positions[i][0], self.positions[i][1]))
        for i, pos in enumerate(self.pressures):
            stringy.append("Position {} has pressure {} \n".format(i, self.pressures[i]))
        ans = "".join(stringy)
        return ans

def makeShapes():
    myShapes = []
    # Stored in the form [rectangles first, then circles]
    for j in range(numparticles):
        particleShapes = []
        for n in range(npivot+1):
            rect = patches.Rectangle((0, 0), width=0, height=0, angle=0.0, edgecolor='black')
            ax.add_artist(rect)
            particleShapes.append(rect)
        for n in range(npivot+2):
            circ = patches.Circle((0, 0), radius=0, edgecolor='black')
            ax.add_artist(circ)
            particleShapes.append(circ)
        myShapes.append(particleShapes)
    return myShapes

def findPropertiesData(f, g):
    i = 0
    for data in f:
        i += 1
    lnumparticles = 0
    lnpivot = 0
    j = 0
    for data in g:
        j += 1
        if j == i:
            lnumparticles = data.count(";")
            lnpivot = data.count(",")/(2*lnumparticles)
    global npivot
    global numparticles
    npivot = int(lnpivot - 2)
    numparticles = int(lnumparticles)
    print("There are {} particles maximum!".format(numparticles))

def formatData(data_in):
    '''Make data per time step per particle'''
    data = []
    for line in data_in:
        timestep = []
        particles = line.split(";")
        for part in particles[:-1]:
            properties = part.split(" ")
            properties = properties[:-1]
            myPart = ParticleData()
            for i, prop in enumerate(properties):
                if i < 1:
                    myPart.ts = int(prop)
                elif i < 2:
                    myPart.ID = int(prop)
                elif i < 3:
                    myPart.D = float(prop)
                elif i < npivot + 5:
                    floats = [float(i) for i in prop.split(',')]
                    floats = tuple(floats)
                    myPart.setPosition(floats)
                elif i < 2*(npivot + 2) + 3:
                    floats = [float(i) for i in prop.split(',')]
                    floats = tuple(floats)
                    myPart.setForce(floats)
                else:
                    myPart.setPressure(float(prop))
            myPart.setCenter()
            timestep.append(myPart)
        data.append(timestep)
    return data

def chooseColor(particle):
    pres = np.mean(particle.pressures)
    H = 1/3*(1 - pres/maxPressure)
    L = 0.5
    S = 1
    rigby = col.hls_to_rgb(H, L, S)
    return rigby

def linewidth_from_data_units(linewidth, axis, reference='y'):
    fig = axis.get_figure()
    if reference == 'x':
        length = fig.bbox_inches.width * axis.get_position().width
        value_range = np.diff(axis.get_xlim())[0]
    elif reference == 'y':
        length = fig.bbox_inches.width * axis.get_position().width
        value_range = np.diff(axis.get_ylim())[0]
    length *= 72
    return linewidth * (length / value_range)

def makeRectangle(c1, c2, D):
    h = D
    v = np.array([(c2[0] - c1[0]), (c2[1] - c1[1])])
    w = np.linalg.norm(v)
    r = np.array([v[1], -v[0]])
    r *= D/(2*np.linalg.norm(r))
    corner = (c1[0] + r[0], c1[1] + r[1])
    theta = np.arctan2(v[1], v[0])
    return (corner, w, h, theta)

#takes 10E-4 sec, but still very slow...?
def neoAnimate(i):
    for j, particle in enumerate(data[i]):
        #set data rectangles
        for k in range(npivot+1):
            rectData = makeRectangle(particle.positions[k], particle.positions[k+1], D)
            myShapes[j][k].set_xy(rectData[0])
            myShapes[j][k].set_width(rectData[1])
            myShapes[j][k].set_height(rectData[2])
            myShapes[j][k].set_facecolor(chooseColor(particle))
            transf = mpl.transforms.Affine2D().rotate_around(rectData[0][0], rectData[0][1], rectData[3]) + ax.transData
            myShapes[j][k].set_transform(transf)
        for l in range(npivot+1, 2*npivot + 3):
            myShapes[j][l].set_radius(D / 2)
            myShapes[j][l].center = (particle.positions[l - npivot - 1][0], particle.positions[l - npivot - 1][1])
            myShapes[j][l].set_facecolor(chooseColor(particle))
    return myShapes

def findMaxPressure():
    maxPressureList = []
    for ts in data:
        for particle in ts:
            maxPressureList.append(sum(particle.pressures)/len(particle.pressures))
    maxPressure = max(maxPressureList)
    return maxPressure

def pressurePlot(i):
    for j, particle in enumerate(data[i]):
        #set data rectangles
        for k in range(npivot+1):
            rectData = makeRectangle(particle.positions[k], particle.positions[k+1], D)
            myShapes[j][k].set_xy(rectData[0])
            myShapes[j][k].set_width(rectData[1])
            myShapes[j][k].set_height(rectData[2])
            transf = mpl.transforms.Affine2D().rotate_around(rectData[0][0], rectData[0][1], rectData[3]) + ax.transData
            myShapes[j][k].set_transform(transf)
        for l in range(npivot+1, 2*npivot + 3):
            myShapes[j][l].set_radius(D / 2)
            myShapes[j][l].center = (particle.positions[l - npivot - 1][0], particle.positions[l - npivot - 1][1])
    return myShapes

def generate_boxes(n_boxes, width_canvas):
    n = int(n_boxes/2)
    box_width = width_canvas/(2*n)
    for y in range(n, -n, -1):
        for x in range(-n, n, 1):
            xl = box_width*x
            xr = box_width*(x+1)
            yl = box_width*y
            yr = box_width*(y-1)
            yield (xl, xr, yl, yr)

if __name__ == "__main__":

    # Find and format the data
    filename = sys.argv[1] 
    N = int(sys.argv[2])
    fig = plt.figure(frameon=False)
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111) #, aspect='equal')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
            hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    f = open(filename, 'r')
    g = open(filename, 'r')
    h = open(filename, 'r')
    findPropertiesData(f, g)
    global data
    data = formatData(h)

    # Prepare for whole plot and plot final ts
    global myShapes
    myShapes = makeShapes()
    global maxPressure
    maxPressure = findMaxPressure()
    for i, ts in enumerate(data):
        if len(ts) >= N:
            ts_interest = i
            break
    neoAnimate(ts_interest)

    # Get width of canvas
    plt.xticks([-10001, 10001])
    plt.yticks([-10001, 10001])
    k = 0
    my_com = prop.get_com_colony(data[-1])
    r = prop.get_radius_colony(com= my_com, ts=data[-1])
    dist_from_origin = max([my_com[0]+r, my_com[1]+r, abs(my_com[0]-r), abs(my_com[1]-r)])
    width_this_canvas = 2*(dist_from_origin - (dist_from_origin%10) + 10)

    # Loop to write images
    for j, i in enumerate(generate_boxes(n_boxes, width_this_canvas)):
        ax.set_xlim([i[0], i[1]])
        ax.set_ylim([i[2], i[3]])
        print(i[0])
        print(i[1])
        print(i[2])
        print(i[3])
        name = "image_{}.png".format(j)
        plt.savefig(name, bbox_inches='tight', pad_inches=0)
        print(k)
        k += 1
    row_list = []
    for l in range(n_boxes**2):
        index = (l // 20, l%20)
        #print(20*index[0]+index[1])
        # print(l)
        # print(k-1)
        my_image = Image.open("image_{}.png".format(l))
        my_image_array = np.asarray(my_image)
        my_image_array = my_image_array[4:-3, 4:-3]
        if l == 0:
            row = np.asarray(my_image_array)
        elif l == (n_boxes**2 -1):
            row = np.hstack([row, my_image_array])
            row_list.append(row)
            print("FINALE")
        elif l%n_boxes != 0:
            row = np.hstack([row, my_image_array])
            print(l)
        else:
            row_list.append(row)
            row = my_image_array
    print(len(row_list))
    finalimage = row_list[0]
    for i in row_list[1:]:
        finalimage = np.vstack([i, finalimage])
    im = Image.fromarray(finalimage)
    im.save("final_{}_Np={}.png".format(filename, N))
