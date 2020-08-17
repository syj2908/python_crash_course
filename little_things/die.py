from random import randint
class Die():
    def __init__(self,sides=6):
        self.sides = sides
    def roll_die(self):
        print(str(randint(1, self.sides)))
die = Die(20)
for x in list(range(90)):
    die.roll_die()

        