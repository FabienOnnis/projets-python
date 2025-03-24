from tkinter import Tk, Button, Label, Entry, Canvas, StringVar, messagebox, PhotoImage, ttk

import sys
sys.path.append('/')

from planete import *
from canvas_utility import *

from threading import Thread

import time

class MyWindow(Tk):

    def __init__(self):
        super().__init__()

        self.entries = []

        self.canvas = None
        self.addEntryButton = None
        self.submitButton = None
        self.stopSimulationButton = None
        self.numberOfRowPerEntry = 5
        self.simulate = False

        self.deleteImage = PhotoImage(file='deleteImage.png')
        
        self.init_interface()

        self.simulationThread = Thread(target=self.simulation)

    def init_interface(self):
        self.state('zoomed')
        self.init_canvas()
        self.init_parameters_editor()

    def init_canvas(self):
        #self.canvas = Canvas(self, width=self.winfo_screenwidth()-400, height=self.winfo_screenheight()-200, bg='black')
        self.canvas = MyCanvas(self, width=self.winfo_screenwidth()-400, height=self.winfo_screenheight()-200, bg='black')
        self.canvas.grid(column=0, row=0, rowspan=30)

    def update_canvas(self):
        self.canvas.grid(column=0, row=0, rowspan=30)

    def init_parameters_editor(self):
        
        self.addEntryButton = Button(self, text="Ajouter une entrée", command=self.addEntry)
        self.addEntryButton.grid(column=1, row=0, columnspan=10)

        self.stopSimulationButton = Button(self, text="Arrêter la simulation", state='disabled', width=21, command=self.stopSimulation)
        self.stopSimulationButton.grid(column=1, row=1)

        self.submitButton = Button(self, text="Lancer la simulation", width=21, command=self.submitForm)
        self.submitButton.grid(column=4, row=1)

    def update_parameters_editor(self):

        for row, entry in enumerate(self.entries) :
            if (row != 0) :
                # Separator
                entry[0].grid(column=1, row=row*self.numberOfRowPerEntry, columnspan=10, sticky="ew")

            entry[1].grid(column=1, row=row*self.numberOfRowPerEntry+1)
            entry[2].grid(column=2, row=row*self.numberOfRowPerEntry+2, sticky='w')
            entry[3].grid(column=3, row=row*self.numberOfRowPerEntry+2, sticky='w')
            entry[4].grid(column=4, row=row*self.numberOfRowPerEntry+2, sticky='w')
            entry[5].grid(column=5, row=row*self.numberOfRowPerEntry+2, sticky='w')
            entry[6].grid(column=2, row=row*self.numberOfRowPerEntry+3, sticky='w')
            entry[7].grid(column=3, row=row*self.numberOfRowPerEntry+3, sticky='w')
            entry[8].grid(column=4, row=row*self.numberOfRowPerEntry+3, sticky='w')
            entry[9].grid(column=5, row=row*self.numberOfRowPerEntry+3, sticky='w')
            entry[10].grid(column=2, row=row*self.numberOfRowPerEntry+4, sticky='w')
            entry[11].grid(column=3, row=row*self.numberOfRowPerEntry+4, sticky='w')
            entry[12].grid(column=4, row=row*self.numberOfRowPerEntry+4, columnspan=2)
        
        self.addEntryButton.grid(column=1, row=len(self.entries)*self.numberOfRowPerEntry, columnspan=10)
        self.stopSimulationButton.grid(column=1, row=len(self.entries)*self.numberOfRowPerEntry+1, columnspan=2)
        self.submitButton.grid(column=4, row=len(self.entries)*self.numberOfRowPerEntry+1, columnspan=2)

    def addEntry(self):
        posXVar = StringVar()
        posYVar = StringVar()
        vxVar = StringVar()
        vyVar = StringVar()
        masseVar = StringVar()

        separator = ttk.Separator(self, orient='horizontal')
        
        newCoordLabel = Label(self, text="Objet :", width=7)

        newLabelX = Label(self, text="xStart :", width=8, anchor="e")
        newEntryX = Entry(self, textvariable=posXVar, width=10)

        newLabelY = Label(self, text="yStart :", width=8, anchor="e")
        newEntryY = Entry(self, textvariable=posYVar, width=10)

        newLabelVX = Label(self, text="vx :", width=8, anchor="e")
        newEntryVX = Entry(self, textvariable=vxVar, width=10)

        newLabelVY = Label(self, text="vy :", width=8, anchor="e")
        newEntryVY = Entry(self, textvariable=vyVar, width=10)

        newLabelMasse = Label(self, text="Masse :", width=8, anchor="e")
        newEntryMasse = Entry(self, textvariable=masseVar, width=10)

        actualLength = len(self.entries)

        newButtonDelete = Button(self, text="", image=self.deleteImage, command = lambda : self.removeEntry(actualLength))
        
        self.entries.append([separator,
                             newCoordLabel,
                             newLabelX, newEntryX,
                             newLabelY, newEntryY,
                             newLabelVX, newEntryVX,
                             newLabelVY, newEntryVY,
                             newLabelMasse, newEntryMasse,
                             newButtonDelete])
        
        self.update_parameters_editor()
        self.update_canvas()

    def removeEntry(self, entryIndex):
        for widget in self.entries[entryIndex] :
            widget.destroy()
            
        self.entries.pop(entryIndex)

        for i, entry in enumerate(self.entries) :
            entry[12].destroy()
            entry[12] = Button(self, text="", image=self.deleteImage, command = lambda : self.removeEntry(i))

        self.update_parameters_editor()

    def submitForm(self):
        if (len(self.entries) == 0):
            messagebox.showinfo("Erreur", "Aucune donnée en entrée.")
        elif (not self.isFormValid()):
            messagebox.showinfo("Erreur", "Certains champs sont incorrects ou ne sont pas remplis")
        else :
            print("Lancement de la simulation")
            self.disableEntries()
            self.retrieveValuesAndLaunchSimulation()

    def isFormValid(self):
        
        isValid = True
        
        for entry in self.entries :
            isValid = isValid and self.isFieldValid(entry)
        
        return isValid

    def isFieldValid(self, entry):
        
        isValid = self.isEntryValidAt(entry, 3)
        isValid = bool(isValid and self.isEntryValidAt(entry, 5))
        isValid = bool(isValid and self.isEntryValidAt(entry, 7))
        isValid = bool(isValid and self.isEntryValidAt(entry, 9))
        isValid = bool(isValid and self.isEntryValidAt(entry, 11))
        
        return isValid

    def isEntryValidAt(self, entry, index):
        isValid = True
        
        try :
            res = float(entry[index].get())

            if (entry[index].get() == ""):
                entry[index].config(bg='red')
                isValid = False
            else :
                entry[index].config(bg='white')
        except :
            entry[index].config(bg='red')
            isValid = False
        
        return isValid

    def disableEntries(self):
        for entry in self.entries :
            entry[3].config(state = 'disabled')
            entry[5].config(state = 'disabled')
            entry[7].config(state = 'disabled')
            entry[9].config(state = 'disabled')
            entry[11].config(state = 'disabled')

        self.submitButton.config(state='disabled')
        self.stopSimulationButton.config(state='active')
        self.addEntryButton.config(state='disabled')

    def stopSimulation(self):
        print("Arrêt de la simulation")
        self.simulate = False
        
        for entry in self.entries :
            entry[3].config(state = 'normal')
            entry[5].config(state = 'normal')
            entry[7].config(state = 'normal')
            entry[9].config(state = 'normal')
            entry[11].config(state = 'normal')

        self.submitButton.config(state='active')
        self.stopSimulationButton.config(state='disabled')
        self.addEntryButton.config(state='active')

    def retrieveValuesAndLaunchSimulation(self):

        planetes = []
        
        for i, entry in enumerate(self.entries) :
            planetes.append(Planete(
                float(entry[3].get()), float(entry[5].get()),
                float(entry[7].get()), float(entry[9].get()),
                float(entry[11].get()), i))

        self.simulate = True
        self.canvas.setObjects(planetes)

        self.simulationThread = Thread(target=self.simulation)
        self.simulationThread.start()

    def simulation(self):
        while self.simulate :
            self.canvas.moveObjects()
            time.sleep(0.01)
