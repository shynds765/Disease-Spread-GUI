# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:28:24 2020

@author: shynd
"""

import tkinter as tk
from random import randint
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Program:
    def __init__(self, main):
        main.title("Disease Spread Simulation")
        
        tk.Label(main, text = "Disease Spread Simulation", font = ("calibri", 20)).grid(row = 0, column = 0, columnspan = 4)

        tk.Label(main, text = "Days to Run Simulation Over", font = ('calibiri', 10), pady = 30).grid(row = 1, column = 0)
        self.daysEntry = tk.Entry(main)
        self.daysEntry.grid(row = 1, column = 1)
        
        tk.Label(main, text = "Population Size", font = ('calibiri', 10), pady = 30).grid(row = 2, column = 0)
        self.populationEntry = tk.Entry(main)
        self.populationEntry.grid(row = 2, column = 1)
        
        tk.Label(main, text = "Initial Number of People Infected", font = ('calibiri', 10), pady = 30).grid(row = 3, column = 0)
        self.infectedEntry = tk.Entry(main)
        self.infectedEntry.grid(row = 3, column = 1)
        
        tk.Label(main, text = "Odds of Contact (perecent)", font = ("calibri", 10)).grid(row = 4, column = 0)
        self.contactSlider = tk.Scale(main, from_ = 0, to = 100, 
                                orient = tk.HORIZONTAL, 
                                length = 500,
                                tickinterval = 10)
        self.contactSlider.grid(row = 4, column = 1)
        
        tk.Label(main, text = "Odds the Vaccine Works (percentage)").grid(row = 5, column = 0)
        self.vaccineSlider = tk.Scale(main, from_ = 0, to = 100, 
                                orient = tk.HORIZONTAL, 
                                length = 500,
                                tickinterval = 10)
        self.vaccineSlider.grid(row = 5, column = 1)
        
        done = tk.Button(main, text = "Run", command = self.simulation)
        done.grid(row = 6, column = 0, columnspan = 2)
        
        
    def simulation(self):
        days = int(self.daysEntry.get())
        population = int(self.populationEntry.get())
        numInfected = int(self.infectedEntry.get())
        contactCoeff = self.contactSlider.get()
        vaccineCoeff = self.vaccineSlider.get()
        #Determines if a person came into contact with anyone during the day
        #returns true if yes and false if no
        def contact():
            oddsContact = contactCoeff #odds a person came into contact with someone
            odds = randint(0,100)
            if odds <= oddsContact:
                contact = 1
            else:
                contact = 0
            return(contact)
        
        #Determines if the poeple you came into contact with had the virus
        #Assumes a 100% transmision rate
        #returns true if infected and false if not
        def infected(numPop, numInfected):
            chance = randint(0,100)
            odds = (numInfected / numPop) * 100
            if chance <= odds:
                infected = 1
            else:
                infected = 0
            return(infected)
        
        #Determines if a vaccine is effectice
        #Assumes immunity lasts forever
        #Returns true if vaccine worked and false if it didn't
        def vaccineWorks():
            odds = randint(0,100)
            oddsEffective = vaccineCoeff #odds the vaccine works on any given person
            if odds <= oddsEffective:
                vaccine = 1
            else:
                vaccine = 0
            return(vaccine)
            
        infectedPerDay = [0] * days
        infectedPerDay[0] = numInfected
        populationArray = [0] * population
        timeInfected = [0] * population
        newInfections = [0] * days
        
        x = 0
        while x < numInfected:
            populationArray[x] = 1
            x += 1
            
        immunity = 0
        for x in populationArray:
            if x == 0:
                if vaccineWorks():
                    populationArray[immunity] = 2
            immunity += 1
                    
        newInfection = 0
        personCounter = 0
        day = 0
        while day < days:
            if day > 0:
                infectedPerDay[day] = infectedPerDay[day - 1]
            for person in populationArray:
                if person == 0:
                    if contact():
                        if infected(population, infectedPerDay[day]):
                            infectedPerDay[day] += 1
                            populationArray[personCounter] = 1
                            newInfection += 1
                elif person == 1:
                    timeInfected[personCounter] += 1
                if timeInfected[personCounter] == 14:
                    infectedPerDay[day] -= 1
                personCounter += 1
            personCounter = 0
            newInfections[day] = newInfection
            newInfection = 0
            day += 1
        
        fig = Figure(figsize = (10,4), dpi = 100)
        infections = fig.add_subplot(111)
        infections.plot(infectedPerDay)
        infections.set_ylabel("Number of People Infected", fontsize=12)
        infections.set_xlabel("Day", fontsize=12)
        infections.set_title("Infections Over Time", fontsize=15)       
        
        canvas = FigureCanvasTkAgg(fig)
        canvas.get_tk_widget().grid(row = 1, column = 3, rowspan = 3)
        
        fig2 = Figure(figsize = (10,4), dpi = 100)
        dailyInfections = fig2.add_subplot(111)
        dailyInfections.bar(range(0, days), newInfections)
        dailyInfections.set_ylabel("New Infections", fontsize = 12)
        dailyInfections.set_xlabel("Day", fontsize=12)
        dailyInfections.set_title("Infections Per Day", fontsize=15)
        
        canvas2 = FigureCanvasTkAgg(fig2)
        canvas2.get_tk_widget().grid(row =4,column = 3, rowspan = 3, pady = 10)
        

main = tk.Tk()
GUI = Program(main)
main.mainloop()
