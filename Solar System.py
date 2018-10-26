import tkinter as t
import time, math

win_width = 1400
win_height = 900

X_MID = win_width / 2
Y_MID = win_height / 2

def cart_pos(rho, phi, x, y):
    # These take radians
    x = rho * math.cos( math.radians(phi) ) + x
    y = rho * math.sin( math.radians(phi) ) + y
    return x, y

def set_pos(canvas, body, x, y):
    #canvas.move(obj, cur_x-targ_x, cur_y-targ_y)
    #canvas.move(body, targ_x-cur_x, targ_y-cur_y)
    #self.canvas.coords(body)[1]
    canvas.move(body, x - canvas.coords(body)[0], y - canvas.coords(body)[1])

class Planet(t.Frame):
    def __init__(self, foobaaah, x, y, name, *args, spacer=20, diff=1, borderwidth=0, **kwargs):
        super().__init__()

        self.x = x
        self.y = y

        self.name = name

        self.spacer = spacer
        self.diff = diff

        self.foobaaah = foobaaah
        self.borderwidth = borderwidth

        #self._init_graphics(*args, **kwargs)
        return args, kwargs

    def _init_graphics(self, *args, **kwargs):
        pass

    def _create_circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def __next__(self):
        pass

class OrbSys(Planet):
    def __init__(self, *args, **kwargs):
        args, kwargs = super().__init__(*args, **kwargs) # OOOOOOOOHHHHHHHHHHHHHHHHH
        print(args)
        print(kwargs)
        self.init_graphics(*args, **kwargs)

    def init_graphics(self, *args):
        self.data = [list(arg) for arg in args]

        nam_ind = 0
        dia_ind = 1
        rev_ind = 2
        col_ind = 3

        rad_ind = 4
        apd_ind = 5
        dis_ind = 6

        for planet in self.data:
            radius = planet[dia_ind] / 2
            #self.radii = [radius / self.diff for radius in self.radii] # Smaller radii to fit on screen
            planet.append(radius)

            angles_per_day = 360 / planet[rev_ind]
            planet.append(angles_per_day)


        for i in self.data:
            print(i)

        self.names = [arg[0] for arg in args]
        self.diameters = [arg[1] for arg in args]
        self.revolutions = [arg[2] for arg in args]
        self.colours = [arg[3] for arg in args]



        self.radii = [size / 2 for size in self.diameters]
        #self.radii = [radius / self.diff for radius in self.radii] # Smaller radii to fit on screen

        #self.angles_per_day = [360 / rev for rev in self.revolutions]
        #self.angles_per_day = [0]*32

        self.distances = [0] # First body (stationary)
        for index, radius in enumerate(self.radii[1:]): # Skip first body
            self.distances.append( self.distances[index] + self.radii[index] )
            self.distances[index+1] += self.spacer + radius


        self.master.title(self.name)
        self.pack(fill=t.BOTH, expand=1)

        self.canvas = t.Canvas(self)
        self.canvas.config(bg='#000000')

        self.canvas.pack(fill=t.BOTH, expand=1)


        self.bodies = []


        self.day = 0
        for distance, body in zip(self.distances, self.data):
            coords = cart_pos(distance, body[apd_ind] * self.day, self.x, self.y)
            foo = self._create_circle(*coords, body[rad_ind], \
                                fill=body[col_ind], width=self.borderwidth)
            self.bodies.append(foo)
        self.foobaaah.update()

    def __next__(self):
        super().__next__()
        for distance, body in zip(self.distances, self.bodies):
            coords = cart_pos(distance, body[apd_ind] * self.day, x, y)
            set_pos(self.canvas, body, *coords)
        self.foobaaah.update()
        self.day += 1

def main():
    # name diameter rev colour
    window = t.Tk()
    #window.attributes("-fullscreen", True)
    window.geometry(f"{win_width}x{win_height}")

    years = 360

    names = ["Sun",\
                    "Mercury", "Venus", "Earth", "Mars", \
                    "Jupiter", "Saturn", "Uranus", "Neptune", \
                    "Pluto"]
    diameters = [200, \
                    5, 12, 13, 7, \
                  143, 125, 51, 50, \
                  2.3]
    # 1 to avoid division by 0
    revolutions = [ 1, \
                        87.97, 224.7, 365.26, 1.88 * years, \
                        11.86 * years, 29.46 * years, 84.01 * years, 164.79 * years, \
                        248.59 * years]
    colours = ["#FDA73E", \
                    "#89868C", "#DBD6D2", "#4958D2", "#F7835B", \
                    "#8E6549","#DBBF76","#CCF2F3","#5661FF", \
                    "#E0D4C6"]

    zipped = [i for i in zip(names, diameters, revolutions, colours)]
    #print(zipped)

    test = OrbSys(window, X_MID, Y_MID, "Solar System", \
                    *zipped)
    time.sleep(1)
    while True:
            next(test)
            time.sleep(.01)
    #window.mainloop()

main()
