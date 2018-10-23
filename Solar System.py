import tkinter as t
import time, math

win_width = 1400
win_height = 900

X_MID = win_width / 2
Y_MID = win_height / 2

window = t.Tk()
#window.attributes("-fullscreen", True)
window.geometry(f"{win_width}x{win_height}")

class Solsys(t.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.init_graphics(*args, **kwargs)

    def init_graphics(self, name, \
                      names, diameters, days_per_revolution, colours, \
                      spacer=20, diff=1, borderwidth=0):
        self.names = names
        self.diameters = diameters
        self.revolutions = days_per_revolution
        self.colours = colours

        self.borderwidth = borderwidth

        self.sun_radius = 240 / 4

        self.radii = [size / 2 for size in self.diameters]
        self.radii = [size / diff for size in self.radii] # Smaller radii to fit on screen

        self.angles_per_day = [360 / rev for rev in self.revolutions]

        self.distances = [self.sun_radius]
        for num in range(len(self.radii)):
            cur_rad = self.radii[num]
            self.distances[num] += spacer + cur_rad
            self.distances.append( self.distances[num] + cur_rad )

        self.master.title(name)
        self.pack(fill=t.BOTH, expand=1)

        self.canvas = t.Canvas(self)
        self.canvas.config(bg='#000000')

        self.canvas.pack(fill=t.BOTH, expand=1)

        print(self.cart_pos(math.sqrt(2), 45))
        day = 0
        while True:
            self.next_frame(day)
            day += 1
            time.sleep(.001)

    def _create_circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def cart_pos(self, rho, phi):
        # These take radians
        x = rho * math.cos( math.radians(phi) ) + X_MID
        y = rho * math.sin( math.radians(phi) ) + Y_MID
        return x, y

    def next_frame(self, day):
        self.canvas.delete("all")
        self._draw_sun()

        #later, use move and coords functions
        for distance, radius, colour, anglepd in zip(self.distances, self.radii, self.colours, self.angles_per_day):
            coords = self.cart_pos(distance, anglepd * day)
            self._create_circle(*coords, radius, \
                                fill=colour, width=self.borderwidth)
        window.update()

    def _draw_sun(self):
        self._create_circle(X_MID, Y_MID, self.sun_radius, \
                            fill="#FDA73E", width=self.borderwidth)

def main():
    years = 360

    names = ["Mercury", "Venus", "Earth", "Mars", \
                    "Jupiter", "Saturn", "Uranus", "Neptune", \
                    "Pluto"]
    diameters = [5, 12, 13, 7, \
                  143, 125, 51, 50, \
                  2.3]
    revolutions = [87.97, 224.7, 365.26, 1.88 * years, \
                        11.86 * years, 29.46 * years, 84.01 * years, 164.79 * years, \
                        248.59 * years]
    colours = ["#89868C", "#DBD6D2", "#4958D2", "#F7835B", \
                    "#8E6549","#DBBF76","#CCF2F3","#5661FF", \
                    "#E0D4C6"]
    test = Solsys(name="Solar System", names=names, diameters=diameters, days_per_revolution=revolutions, colours=colours)
    #window.mainloop()

main()
