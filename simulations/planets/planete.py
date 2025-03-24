import math

class Planete :
    def __init__(self, x, y, vx, vy, m, index):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.index = index

    def showPlaneteInConsole(self):
        print("\nPlanete ", self.index, " :")
        print("    x, y = ", entry[3].get(), ", ", entry[5].get())
        print("    vx, vy = ", entry[7].get(), ", ", entry[9].get())
        print("    m = ", entry[11].get())

    def distanceFrom(self, p2):
        return math.sqrt((p2.x - self.x)**2 + (p2.y - self.y)**2)
