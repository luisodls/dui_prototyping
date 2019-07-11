from itertools import chain

class SolarSystem:

    def __init__ (self):
        self.reset_num()

    def count_01 (self):
        self.counting += 1
        self.update_count()

    def explain (self):
        document.getElementById ('explain').innerHTML = "reset ..."
        self.reset_num()
        self.update_count()
        document.getElementById ('explain').innerHTML = "done ..."

    def reset_num(self):
        self.counting = 0

    def update_count(self):
        str_counting = "Number of planets = " + str(self.counting) + "..."
        document.getElementById ('count_01') .innerHTML = str_counting



solarSystem = SolarSystem ()
