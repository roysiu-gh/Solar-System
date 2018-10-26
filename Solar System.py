import tkinter as tk
import time, math

win_width = 1400
win_height = 900

X_MID = win_width / 2
Y_MID = win_height / 2

def cart_pos(rho, phi, x, y):
    # Note: these take radians
    x = rho * math.cos( math.radians(phi) ) + x
    y = rho * math.sin( math.radians(phi) ) + y
    return x, y

class Body(tk.Frame):

    nam_ind = 0
    rad_ind = 1
    rev_ind = 2
    col_ind = 3

    apd_ind = 4
    tkid_ind = 5

    day = 0 # Increments in __next__()

    def __init__(self, window, centre_x, centre_y, *args, spacer=20, diff=1, border_width=0, displacement=0, super_call=False, canvas=None, **kwargs):
        super().__init__()

        centre_body = args[0]
        self.name = centre_body[0]
        self.radius = centre_body[1]
        self.revolutions = centre_body[2]
        self.colour = centre_body[3]
        self.displacement = displacement
        self.apd = 360 / self.revolutions # Angles per day

        # Point from which the planets orbit
        self.centre_x = centre_x
        self.centre_y = centre_y

        self.spacer = spacer
        self.diff = diff

        self.window = window
        self.border_width = border_width

        # Use same canvas if exists
        if canvas == None:
            self.canvas = tk.Canvas(self)
        else:
            self.canvas = canvas

        self._init_graphics()

        if super_call:
            return args[1:], kwargs # Ignore centre body, also screw it, I'm returning

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
        self.window.update()
        self.day += 1

class OrbSys(Body):
    def __init__(self, *args, **kwargs):
        args, kwargs = super().__init__(*args, **kwargs, super_call=True)

        self.bodies = [list(arg) for arg in args]

        for body in self.bodies:
            angles_per_day = 360 / body[self.rev_ind]
            body.append(angles_per_day)

        self.displacements = [self.radius + self.spacer] # Clear (don't collide wih) centre body
        for index, body in enumerate(self.bodies[1:]):  # Skip first body
            self.displacements.append(self.displacements[index] + self.bodies[index][self.rad_ind])
            self.displacements[index + 1] += self.spacer + body[self.rad_ind]

        self.pack(fill=tk.BOTH, expand=1)

        self.canvas.config(bg='#000000')

        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.body_objs = []
        for body, displacement in zip(self.bodies, self.displacements):
            to_append = Body(self.window, self.centre_x, self.centre_y, body, name=body[self.nam_ind], displacement=displacement, canvas=self.canvas)
            self.body_objs.append(to_append)

    def __next__(self):
        super().__next__()
        for body in self.body_objs:
            body.centre_x = self.x
            body.centre_y = self.y
            next(body)
        self.window.update()

def main():
    # name radius rev colour angles_per_day tkinter_canvas_id
    window = tk.Tk()
    window.title("Solar System")
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
    radii = [x/2 for x in diameters]
    # 1 to avoid division by 0
    revolutions = [ 1, \
                        87.97, 224.7, 365.26, 1.88 * years, \
                        11.86 * years, 29.46 * years, 84.01 * years, 164.79 * years, \
                        248.59 * years]
    #revolutions = [360]*10
    colours = ["#FDA73E", \
                    "#89868C", "#DBD6D2", "#4958D2", "#F7835B", \
                    "#8E6549","#DBBF76","#CCF2F3","#5661FF", \
                    "#E0D4C6"]

    zipped = [i for i in zip(names, radii, revolutions, colours)]
    #print(zipped)

    SolarSystem = OrbSys(window, X_MID, Y_MID, *zipped)
    time.sleep(1)
    while True:
            next(SolarSystem)
            time.sleep(.01)
    #window.mainloop()

main()
# fix private objects
