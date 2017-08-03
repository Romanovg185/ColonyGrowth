class ParticleData(object):
    def __init__(self):
        self.ts = 0
        self.ID = 0
        self.D = 0
        self.positions = []
        self.forces = []
        self.pressures = []
        self.center = 0

    def set_position(self, inp):
        self.positions.append(inp)

    def set_force(self, inp):
        self.forces.append(inp)

    def set_pressure(self, inp):
        self.pressures.append(inp)

    def set_center(self):
        my_center = [0.0, 0.0]
        for point in self.positions:
            my_center[0] += point[0]/len(self.positions)
            my_center[1] += point[1]/len(self.positions)
        self.center = tuple(my_center)

    def __str__(self):
        stringy = ["Time step is " + str(self.ts) + "\n"]
        stringy.append("Particle ID is " + str(self.ID) + "\n")
        stringy.append("Diameter is " + str(self.D) + "\n")
        for i, pos in enumerate(self.positions):
            stringy.append("Position {} has coordinates ({},{}) \n"
                           .format(i, self.positions[i][0], self.positions[i][1]))
        for i, pos in enumerate(self.pressures):
            stringy.append("Position {} has pressure {} \n".format(i, self.pressures[i]))
        ans = "".join(stringy)
        return ans


def format_data(data_in, n_pivot):
    """Make data per time step per particle"""
    data = []
    z = 0
    for line in data_in:
        if z%5 != 0:
            z += 1
            continue
        z += 1
        time_step = []
        particles = line.split(";")
        for part in particles[:-1]:
            properties = part.split(" ")
            properties = properties[:-1]
            my_part = ParticleData()
            for i, prop in enumerate(properties):
                if i < 1:
                    my_part.ts = int(prop)
                elif i < 2:
                    my_part.ID = int(prop)
                elif i < 3:
                    my_part.D = float(prop)
                elif i < n_pivot + 5:
                    floats = [float(i) for i in prop.split(',')]
                    floats = tuple(floats)
                    my_part.set_position(floats)
                elif i < 2*(n_pivot + 2) + 3:
                    floats = [float(i) for i in prop.split(',')]
                    floats = tuple(floats)
                    my_part.set_force(floats)
                else:
                    my_part.set_pressure(float(prop))
            my_part.set_center()
            time_step.append(my_part)
        data.append(time_step)
    return data
