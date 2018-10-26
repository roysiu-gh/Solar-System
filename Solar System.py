import tkinter as t
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

class Body(t.Frame):

    nam_ind = 0
    rad_ind = 1
    rev_ind = 2
    col_ind = 3

    apd_ind = 4
    tkid_ind = 5

    day = 0 # Increments in __next__()

    def __init__(self, window, x, y, name, *args, spacer=20, diff=1, border_width=0, **kwargs):
        super().__init__()

        self.x = x
        self.y = y
        self.coords = (x, y)

        self.name = name

        self.spacer = spacer
        self.diff = diff

        self.window = window
        self.border_width = border_width

        self.canvas = t.Canvas(self)

        #self._init_graphics(*args, **kwargs)
        return args, kwargs

    def _init_graphics(self, *args, **kwargs):
        pass

    def __next__(self):
        self.day += 1

class OrbSys(Body):
    def __init__(self, *args, **kwargs):
        args, kwargs = super().__init__(*args, **kwargs)

        self.bodies = [list(arg) for arg in args]

        for body in self.bodies:
            body[self.rad_ind] # Smaller radii to fit on screen

            angles_per_day = 360 / body[self.rev_ind]
            body.append(angles_per_day)

        self.displacements = [0] # First body (zero displacement)
        for index, body in enumerate(self.bodies[1:]): # Skip first body
            self.displacements.append(self.displacements[index] + self.bodies[index][self.rad_ind])
            self.displacements[index + 1] += self.spacer + body[self.rad_ind]

        self.master.title(self.name)
        self.pack(fill=t.BOTH, expand=1)

        self.canvas.config(bg='#000000')

        self.canvas.pack(fill=t.BOTH, expand=1)

        self.init_graphics()

    def init_graphics(self):
        for displacement, body in zip(self.displacements, self.bodies):
            angle = body[self.apd_ind] * self.day
            x, y = cart_pos(displacement, angle, self.x, self.y)[:2]
            r = body[self.rad_ind]
            tk_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, \
                                            fill=body[self.col_ind], width=self.border_width)
            body.append(tk_id)
        self.window.update()

        #for i in self.bodies:
        #    print(i)

    def __next__(self):
        super().__next__()
        #self.canvas.delete("all")
        for displacement, body in zip(self.displacements, self.bodies):
            angle = body[self.apd_ind] * self.day
            x, y = cart_pos(displacement, angle, self.x, self.y)
            r = body[self.rad_ind]
            bounds_coords = (x-r, y-r, x+r, y+r) # Canvas.coords() (to move) requires outer bounds for circles (ovals)
            self.canvas.coords(body[self.tkid_ind], bounds_coords)
        self.window.update()

def main():
    # name radius rev colour angles_per_day tkinter_canvas_id
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

    test = OrbSys(window, X_MID, Y_MID, "Solar System", \
                    *zipped)
    time.sleep(1)
    while True:
            next(test)
            time.sleep(.01)
    #window.mainloop()

main()
# fix private objects
