import tkinter as tk
import time, math

WIN_WIDTH = 1400
WIN_HEIGHT = 900

X_MID = WIN_WIDTH / 2
Y_MID = WIN_HEIGHT / 2

def cart_pos(rho, phi, x, y):
    # Note: these take radians
    x = rho * math.cos( math.radians(phi) ) + x
    y = rho * math.sin( math.radians(phi) ) + y
    return x, y

class Body(tk.Frame):

    nam_ind = 0
    rad_ind = 1
    per_ind = 2
    col_ind = 3

    apd_ind = 4
    tkid_ind = 5

    day = 0 # Increments in __next__()

    def __init__(self, window, canvas, centre_x, centre_y, *args, \
                 name="", radius=0, orbital_period=1, colour="#000000", \
                 diff=1, border_width=0, displacement=0, super_call=False, **kwargs):
        """
        Initialise instance variables
        Create canvas if not already created/passed
        Call _init_graphics()
        Pass extra arguments to outer daughter (instance) initialisation

        :param window: Tkinter window
        :type window: tkinter.Tk()
        :param centre_x: x co-ordinate of (current) orbit centre
        :type centre_x: float
        :param centre_y: y co-ordinate of (current) orbit centre
        :type centre_y: float
        :param args: Data for bodies: tuples of Name, Radius, Orbital period, and Colour
        :type args: list( tuples(str, float, float, str) )
        :param diff: Divisor to reduce radius by (use if more space is needed)
        :type diff: float
        :param border_width: Border width of singular bodies
        :type border_width: float
        :param displacement: displacement from orbital centre to body centre
        :type displacement: float
        :param super_call: Only return leftover arguments if calling super().__init__() from a daughter class
        :type super_call: bool
        :param canvas: Canvas on which to draw items
        :type canvas: tkinter.Canvas(tkinter.Frame)
        :param kwargs: Extra keyword arguments to pass to lower classes / decorators etc.
        :type kwargs: dict

        .. note:: same canvas must be passed if nesting orbital systems
        """
        super().__init__()

        #self.data = list(args[0])
        #self.name = self.data[0]
        #self.radius = self.data[1]
        #self.radius /= diff # Reduce size if needed
        #self.orbital_period = self.data[2]
        #self.colour = self.data[3]
        #self.displacement = displacement
        #self.apd = 360 / self.orbital_period # Angles per day
        #self.data.append(self.apd)

        self.name = name
        self.radius = radius
        self.radius /= diff  # Reduce size if needed
        self.orbital_period = orbital_period
        self.colour = colour
        self.displacement = displacement
        self.apd = 360 / self.orbital_period  # Angles per day

        # Point from which the bodies orbit
        self.centre_x = centre_x
        self.centre_y = centre_y

        self.diff = diff

        self.window = window
        self.border_width = border_width

        self.canvas = canvas

        self._init_graphics()

        self.data = [self.name, self.radius, self.orbital_period, self.colour, self.apd, self.tk_id]

    def _init_graphics(self):
        angle = self.apd * self.day
        x, y = cart_pos(self.displacement, angle, self.centre_x, self.centre_y)
        r = self.radius
        self.tk_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, \
                                        fill=self.colour, width=self.border_width)

    def __next__(self):
        angle = self.apd * self.day
        self.x, self.y = cart_pos(self.displacement, angle, self.centre_x, self.centre_y)
        x, y = self.x, self.y
        r = self.radius
        bounds_coords = (x-r, y-r, x+r, y+r) # Canvas.coords() (to move) requires outer bounds for circles (ovals)
        self.canvas.coords(self.tk_id, bounds_coords)
        print(self.name)
        print(self.tk_id)
        self.window.update()
        self.day += 1

    def __iter__(self):
        for i in self.data:
            yield i

class OrbSys(Body):
    def __init__(self, bodies, *args, spacer=20, **kwargs):
        print(args,kwargs)
        #args, kwargs = super().__init__(*args, name="", radius=0, orbital_period=1, colour ="", **kwargs, super_call=True) # Find a better way to do this
        super().__init__(*args, name="", radius=0, orbital_period=1, colour="", **kwargs, super_call=True)

        self.name = args[self.nam_ind]
        self.orbital_period = args[self.per_ind]
        self.colour = args[self.col_ind]

        self.spacer = spacer

        self.bodies = bodies

        print("self.bodies")
        for i in self.bodies:
            print(i)

        self.displacements = [self.radius + self.spacer] # Clear (don't collide wih) centre body
        for index, body in enumerate(self.bodies[1:]):  # Skip first body
            self.displacements.append(self.displacements[index] + self.bodies[index][self.rad_ind])
            self.displacements[index + 1] += self.spacer + body[self.rad_ind]

        self.radius = self.displacements[-1] + self.bodies[-1][self.rad_ind] #Do this for nested orbital syss

        self.body_objs = []
        for body, displacement in zip(self.bodies, self.displacements):
            print(body)
            to_append = Body(self.window, self.canvas, self.centre_x, self.centre_y, \
                             name=body[self.nam_ind], radius=body[self.rad_ind], orbital_period=body[self.per_ind], colour=body[self.col_ind], \
                             displacement=displacement)
            self.body_objs.append(to_append)
            print()

    def __next__(self):
        super().__next__()
        for body in self.body_objs:
            body.centre_x = self.x
            body.centre_y = self.y
            #print(body.name)
            next(body)
        #print()
        self.window.update()

def main():
    window = tk.Tk()
    window.title("Solar System")
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

    canvas = tk.Canvas(window, width=WIN_WIDTH, height=WIN_HEIGHT)
    canvas.config(bg='#000000')
    canvas.pack(fill=tk.BOTH, expand=1)

    years = 360

    names = ["Sun",\
                    "Mercury", "Venus", "Earth", "Mars", \
                    "Jupiter", "Saturn", "Uranus", "Neptune", \
                    "Pluto"]
    diameters = [200, \
                    5, 12, 13, 7, \
                  143, 125, 51, 50, \
                  2.3]
    radii = [x/2 for x in diameters]
    # 1 to avoid division by 0
    orbital_period = [ 1, \
                        87.97, 224.7, 365.26, 1.88 * years, \
                        11.86 * years, 29.46 * years, 84.01 * years, 164.79 * years, \
                        248.59 * years]
    colours = ["#FDA73E", \
                    "#89868C", "#DBD6D2", "#4958D2", "#F7835B", \
                    "#8E6549","#DBBF76","#CCF2F3","#5661FF", \
                    "#E0D4C6"]

    zipped = [i for i in zip(names, radii, orbital_period, colours)]

    #earthsyslis = [zipped.pop(3)]
    #earthsyslis.append(("Moon", 1.625, 27, "#B7B1AA"))
    ## Caution diff earthsys earthsyslis
    #earthsys = OrbSys(window, canvas, 0, 0, *earthsyslis, spacer=10)
    #zipped.insert(3, earthsys)
    ##print(type(earthsys))

    #for i in zipped:
    #    print(i)
    #print()

    solsys = OrbSys(zipped, window, canvas, X_MID, Y_MID)#, spacer=10)
    solsys.pack(fill=tk.BOTH, expand=1)
    time.sleep(1)
    while True:
        next(solsys)
        time.sleep(.01)
    #window.mainloop()

main()
