from itertools import chain

class SolarSystem:

    def __init__ (self):
        self.reset_num()

    def counter (self):
        self.counting += 1
        self.update_count()

    def reset_but (self):
        document.getElementById ('reset_but').innerHTML = "reset ..."
        self.reset_num()
        self.update_count()
        document.getElementById ('reset_but').innerHTML = "done ..."

    def reset_num(self):
        self.counting = 0

    def update_count(self):
        str_counting = "Number of planets = " + str(self.counting) + "..."
        document.getElementById ('counter') .innerHTML = str_counting



solarSystem = SolarSystem ()
