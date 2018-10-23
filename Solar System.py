import tkinter as t
import time, math

win_width = 1400
win_height = 900

X_MID = win_width / 2
Y_MID = win_height / 2

gui = t.Tk()
gui.geometry(f"{win_width}x{win_height}+300+300")
class Solsys(t.Frame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        spacer = 20
        diff = 2

        years = 360

        self.width = 0

        self.names = ["Mercury", "Venus", "Earth", "Mars", \
                        "Jupiter", "Saturn", "Uranus", "Neptune", \
                        "Pluto"]

        self.sun_radius = 240 / 4

        self.sizes = [5, 12, 13, 7, \
                      143, 125, 51, 50, \
                      2.3]
        self.revolutions = [87.97, 224.7, 365.26, 1.88 * years, \
                            11.86 * years, 29.46 * years, 84.01 * years, 164.79 * years, \
                            248.59 * years]
        #self.angles_per_day = [360 / rev for rev in self.revolutions]
        #self.angles_per_day = [.01 for rev in self.revolutions]
        self.angles_per_day = [360 / rev for rev in self.revolutions] # I don't know why
        print(self.angles_per_day)

        self.colours = ["#89868C", "#DBD6D2", "#4958D2", "#F7835B", \
                        "#8E6549","#DBBF76","#CCF2F3","#5661FF", \
                        "#E0D4C6"]

        self.radii = [size / diff for size in self.sizes]

        self.spacers = [self.sun_radius]
        for num in range(len(self.radii)):
            cur_rad = self.radii[num]
            self.spacers[num] += spacer + cur_rad
            self.spacers.append( self.spacers[num] + cur_rad )

        #print(self.spacers)

        self.master.title("Lines")
        self.pack(fill=t.BOTH, expand=1)

        self.canvas = t.Canvas(self)
        self.canvas.config(bg='#000000')

        self.canvas.pack(fill=t.BOTH, expand=1)

        #while True:
        #    for day in range(360):
        #        print(day)
        #        self.next_frame(day)

        print(self.cart_pos(math.sqrt(2), 45))
        day = 0
        while True:
            self.next_frame(day)
            day += 1
            time.sleep(.001)


    def _create_circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def cart_pos(self, rho, phi):
        # THEESE TAKE RADIANS NOT DEGREES
        x = rho * math.cos( math.radians(phi) ) + X_MID
        y = rho * math.sin( math.radians(phi) ) + Y_MID
        return x, y

    def cart2pol(self, x, y):
        rho = math.sqrt(x ** 2 + y ** 2)
        phi = math.atan2(y, x)
        return rho, phi

    def next_frame(self, day):
        self.canvas.delete("all")
        self._draw_sun()

        #later, use move and coords functions
        for spacer, radius, colour, anglepd in zip(self.spacers, self.radii, self.colours, self.angles_per_day):
            distance = spacer
            print((distance, anglepd * day))
            coords = self.cart_pos(distance, anglepd * day)
            print(coords)
            print( self.cart2pol( *coords ) )
            print()
            self._create_circle(*coords, radius, \
                                fill=colour, width=self.width)
            print(int( (anglepd * day) % 360 //1))
            print(*[int(coord//1) for coord in coords])
            print(spacer, radius, colour, anglepd)
            print()
        gui.update()
        print()

        #self._draw_mercury(day)
        #gui.update()
        #self._draw_venus(day)
        #self._draw_earth(day)
        #self._draw_mars(day)

        #self._draw_jupiter(day)
        #self._draw_saturn(day)
        #self._draw_uranus(day)
        #self._draw_neptune(day)

        #self._draw_pluto(day)

    def _draw_sun(self):
        self._create_circle(X_MID, Y_MID, self.sun_radius, \
                            fill="yellow", width=self.width)

    """def _draw_mercury(self, day):
        self._create_circle(X_MID + self.spacers[0], Y_MID, self.radii[0], \
                            fill="grey", width=self.width)
    def _draw_venus(self, day):
        self._create_circle(X_MID + self.spacers[1], Y_MID, self.radii[1], \
                            fill="yellow", width=self.width)
    def _draw_earth(self, day):
        self._create_circle(X_MID + self.spacers[2], Y_MID, self.radii[2], \
                            fill="blue", width=self.width)
    def _draw_mars(self, day):
        self._create_circle(X_MID + self.spacers[3], Y_MID, self.radii[3], \
                            fill="brown", width=self.width)

    def _draw_jupiter(self, day):
        self._create_circle(X_MID + self.spacers[4], Y_MID, self.radii[4], \
                            fill="orange", width=self.width)
    def _draw_saturn(self, day):
        self._create_circle(X_MID + self.spacers[5], Y_MID, self.radii[5], \
                            fill="gold", width=self.width)
    def _draw_uranus(self, day):
        self._create_circle(X_MID + self.spacers[6], Y_MID, self.radii[6], \
                            fill="blue", width=self.width)
    def _draw_neptune(self, day):
        self._create_circle(X_MID + self.spacers[7], Y_MID, self.radii[7], \
                            fill="brown", width=self.width)

    def _draw_pluto(self, day):
        self._create_circle(X_MID + self.spacers[8], Y_MID, self.radii[8], \
                            fill="blue", width=self.width)"""


def main():
    ex = Solsys()
    #ex.next_frame()
    gui.mainloop()

main()
