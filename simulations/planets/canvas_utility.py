from tkinter import Tk, Button, Label, Entry, Canvas, StringVar, messagebox, PhotoImage, ttk

import sys
sys.path.append('/')

from random import randint
import math
from planete import *

class MyCanvas(Canvas):

    def __init__(self, root, **kw):
        super(MyCanvas, self).__init__(master=root, **kw)

        self.objects = []
        self.drawings = []
        self.colors = []

        self.G = 6.67408e-11
        self.dt = 100000000

    def setObjects(self, objects):
        self.delete("all")
        self.objects = objects
        self.drawings = []
        self.colors = []

        for obj in self.objects :
            tempColor = self.generateColor()
            oval = self.create_oval(obj.x-obj.m/2, obj.y-obj.m/2, obj.x+obj.m/2, obj.y+obj.m/2, fill=tempColor)
            vecteurX = self.create_line(obj.x, obj.y, obj.x+obj.vx, obj.y, fill='blue')
            vecteurY = self.create_line(obj.x, obj.y, obj.x, obj.y+obj.vy, fill='red')
            vecteurVitesse = self.create_line(obj.x, obj.y, obj.x+obj.vx, obj.y+obj.vy, fill='green')
            self.drawings.append([oval, vecteurX, vecteurY, vecteurVitesse])
            self.colors.append(tempColor)

    def moveObjects(self):
        objectsCopy = self.objects + []
        
        for i, drawing in enumerate(self.drawings) :
            current_coords = self.coords(drawing[0])

            sumX = 0
            sumY = 0

            #print("Objet ", i, " :")

            for k, otherObject in enumerate(objectsCopy) :
                if (k != i):
                    distance = objectsCopy[i].distanceFrom(otherObject)

                    if (distance != 0):
                        sumX += self.G * otherObject.m * (otherObject.x - objectsCopy[i].x) / distance
                        #print("    sumX += ", self.G, " * ", otherObject.m, " * (", otherObject.x, " - ", objectsCopy[i].x, ") / ", distance, ") = ", sumX)
                    if (distance != 0):
                        sumY += self.G * otherObject.m * (otherObject.y - objectsCopy[i].y) / distance
                        #print("    sumY += ", self.G, " * ", otherObject.m, " * (", otherObject.y, " - ", objectsCopy[i].y, ") / ", distance, ") = ", sumY)

            #print("    vx = ", self.objects[i].vx, " + ", sumX, " * ", self.dt, " = ", self.objects[i].vx + sumX * self.dt)
            #print("    vy = ", self.objects[i].vy, " + ", sumY, " * ", self.dt, " = ", self.objects[i].vy + sumY * self.dt)

            self.objects[i].vx = self.objects[i].vx + sumX * self.dt
            self.objects[i].vy = self.objects[i].vy + sumY * self.dt

            self.objects[i].x = self.objects[i].x + self.objects[i].vx
            self.objects[i].y = self.objects[i].y + self.objects[i].vy
            
            self.create_line(
                current_coords[0]+(self.objects[i].m/2), current_coords[1]+(self.objects[i].m/2),
                current_coords[0]+(self.objects[i].m/2)+self.objects[i].vx, current_coords[1]+(self.objects[i].m/2)+self.objects[i].vy,
                fill=self.colors[i])

            self.delete(drawing[1])
            self.delete(drawing[2])
            self.delete(drawing[3])

            obj = self.objects[i]

            vecteurX = self.create_line(obj.x, obj.y, obj.x+obj.vx, obj.y, fill='blue')
            vecteurY = self.create_line(obj.x, obj.y, obj.x, obj.y+obj.vy, fill='red')
            vecteurVitesse = self.create_line(obj.x, obj.y, obj.x+obj.vx, obj.y+obj.vy, fill='green')

            drawing[1] = vecteurX
            drawing[2] = vecteurY
            drawing[3] = vecteurVitesse
            
            self.move(drawing[0], self.objects[i].vx, self.objects[i].vy)
            self.move(drawing[1], self.objects[i].vx, self.objects[i].vy)
            self.move(drawing[2], self.objects[i].vx, self.objects[i].vy)
            self.move(drawing[3], self.objects[i].vx, self.objects[i].vy)

    def generateColor(self):
        return self.rgbToHex(randint(0, 255), randint(0, 255), randint(0, 255))

    def rgbToHex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def fx(self, M, x, y):
        return -((self.G*M)/(x**2+y**2)**(3/2))*x*(self.t**2/self.au**3)

    def fy(self, M, x, y):
        return -((self.G*M)/(x**2+y**2)**(3/2))*y*(self.t**2/self.au**3)

