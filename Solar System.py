
import tkinter as tk
import time, math

WIN_WIDTH = 1400
WIN_HEIGHT = 900

X_MID = WIN_WIDTH / 2
Y_MID = WIN_HEIGHT / 2

#Testing
WIN_WIDTH = 850
WIN_HEIGHT = 400

X_MID = 200
Y_MID = 200

def cart_pos(rho, phi, x_offset, y_offset):
    # Note: these take radians
    x = rho * math.cos( math.radians(phi) ) + x_offset
    y = rho * math.sin( math.radians(phi) ) + y_offset
    return x, y

class Body(tk.Frame):

    # Class-wide index constants
    nam_ind = 0
    rad_ind = 1
    per_ind = 2
    col_ind = 3

    apd_ind = 4
    tkid_ind = 5

    day = 0 # Increments in __next__()

    def __init__(self, window, canvas, centre_x, centre_y, *args, \
                 name="", radius=0, orbital_period=1, colour="#000000", \
                 diff=1, border_width=0, displacement=0, **kwargs):
        """
        Initialise instance variables
        Call _init_graphics()

        :param window: Tkinter window
        :type window: tkinter.Tk()
        :param canvas: Canvas on which to draw items
        :type canvas: tkinter.Canvas(tkinter.Tk())
        :param centre_x: x co-ordinate of (current) orbit centre
        :type centre_x: float
        :param centre_y: y co-ordinate of (current) orbit centre
        :type centre_y: float
        :param args: Extra positional arguments to pass to lower classes / decorators etc.
        :type args: list
        :param name: name of body
        :type name: str
        :param radius: radius of body
        :type radius: float
        :param orbital_period: time in days to orbit around centre point
        :type orbital_period: float
        :param colour: Hex value of body
        :type colour: str
        :param diff: Divisor to reduce radius by (use if more space is needed)
        :type diff: float
        :param border_width: Border width of singular bodies
        :type border_width: float
        :param displacement: displacement from orbital centre to body centre
        :type displacement: float
        :param kwargs: Extra keyword arguments to pass to lower classes / decorators etc.
        :type kwargs: dict
        """
        super().__init__()

        self.typestr = "Body"

        self.name = name
        self.radius = radius
        self.orbital_period = orbital_period
        self.colour = colour
        self.displacement = displacement

        self.radius /= diff  # Reduce radius if needed
        self.apd = 360 / self.orbital_period  # Angles per day

        # Point from which the bodies orbit
        self.centre_x = centre_x
        self.centre_y = centre_y

        self.window = window
        self.canvas = canvas
        self.border_width = border_width

        self._init_graphics()

        self.data = [self.name, self.radius, self.orbital_period, self.colour, self.apd, self.tk_id]

    def _init_graphics(self):
        angle = self.apd * self.day
        x, y = cart_pos(self.displacement, angle, self.centre_x, self.centre_y)
        r = self.radius
        self.tk_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.colour, width=self.border_width)

    def __next__(self):
        angle = self.apd * self.day
        self.x, self.y = cart_pos(self.displacement, angle, self.centre_x, self.centre_y)
        x, y = self.x, self.y
        r = self.radius
        bounds_coords = (x-r, y-r, x+r, y+r) # Canvas.coords() (to move) requires outer bounds for circles (ovals)
        #print(self.name)
        self.canvas.coords(self.tk_id, bounds_coords)
        self.window.update()
        self.day += 1
        if self.name in ("Earth Sys", "Earth", "Moon"):
            print("> name >>", self.name)
            print("> heyeheyhey >>", self.apd)
            print("> centre_x, centre_y >>", self.centre_x, self.centre_y)
            print("> x, y >>", x, y)
            print("> displacement, angle >>", self.displacement, angle)
            print("> tk_id >>", self.tk_id)
            print()

    def __iter__(self):
        for i in self.data:
            yield i

    def __str__(self):
        return str(list(self))

class OrbSys(Body):
    def __init__(self, bodies, *args, spacer=20, **kwargs):
        super().__init__(*args, **kwargs)

        self.typestr = "OrbSys"

        self.bodies = bodies
        self.body_tuples = [tuple(body) for body in bodies] # Convert nested OrbSys to tuples

        self.displacements = [0]#self.radius + spacer] # Clear (don't collide wih) centre body

        for index, body in enumerate(self.body_tuples[1:]):  # Skip first body
            #if body[self.nam_ind] == "Earth Sys":
            #    print("> Body >>", body)
            #    print("> Bodytype >>", type(body))
            #    for i in body: print("- ", i)
            #    print("> radind >>", self.rad_ind)

            self.displacements.append(self.displacements[index] + self.body_tuples[index][self.rad_ind])

            #if body[self.nam_ind] == "Earth Sys":
            #    print("> curdisp >>", self.displacements[index + 1])
            #    print("> HEY LOOK LISTEN RADIUS >>", body[self.rad_ind])
            #    print()

            self.displacements[index + 1] += spacer + body[self.rad_ind] ###

        self.radius = self.displacements[-1] + self.body_tuples[-1][self.rad_ind] # Full radius of system
        #if self.name == "Earth Sys": print(self.radius)
        self.data[self.rad_ind] = self.radius # Apparently not a shallow copy

        if self.name == "Earth Sys":
            self.orbital_period = self.body_tuples[0][self.per_ind]
            print("new orbper", self.body_tuples[0][self.per_ind])
            self.apd = 360 / self.orbital_period  # Angles per day
            print("new apd", 360 / self.orbital_period)

        self.body_objs = []
        for body, displacement in zip(self.bodies, self.displacements): #bodies document
            if isinstance(body, tuple):
                to_append = Body(self.window, self.canvas, self.centre_x, self.centre_y, \
                                 name=body[self.nam_ind], radius=body[self.rad_ind], orbital_period=body[self.per_ind], colour=body[self.col_ind], \
                                 displacement=displacement)
            else: # Basically 'if isinstance(body, Orbsys):', but it isn't defined yet
                print(body)
                body.displacement = displacement
                body.body_objs[0].displacement = displacement
                #body.centre_x = self.x
                #body.centre_y = self.y
                to_append = body
            self.body_objs.append(to_append)

        self.__next__()  # testing

    def __next__(self):
        super().__next__()
        for body in self.body_objs:
            body.centre_x = self.x
            body.centre_y = self.y
            #if body.typestr == "OrbSys":
            next(body)
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

    earthsyslis = [zipped.pop(3)]
    #earthsyslis.append(("Moon", 1.625, 27, "#B7B1AA")) #radius wrong?
    # Caution diff earthsys earthsyslis
    earthsys = OrbSys(earthsyslis, window, canvas, 0, 0, spacer=10, name="Earth Sys")
    earthsys.pack(fill=tk.BOTH, expand=1)
    print(earthsys.radius)
    zipped.insert(3, earthsys)
    #print("fasdfsaafs", earthsys.radius)
    #print("fasdfsaafs", earthsys)

    solsys = OrbSys(zipped, window, canvas, X_MID, Y_MID, spacer=10, name="I'll be back")
    solsys.pack(fill=tk.BOTH, expand=1)
    time.sleep(1)
    while True:
        next(solsys)
        time.sleep(.01)
    #window.mainloop()

main()
# unexpected centre body vertical movement
