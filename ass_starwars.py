__author__ = "Andrea Bonatti"

import random
from os import sys


class Jedi(object):
    age = 0

    def __init__(self, jedi_id, mother_jedi=None):
        self.jedi_id = jedi_id
        self.mother_jedi = mother_jedi
        self.sex = random.choice(["m", "f"])
        if self.sex == "m":
            self.mark = "m"
            self.name = random.choice(["Anakin", "Luke", "Han", "Obi-Wan", "Kylo"])
        else:
            self.mark = "f"
            self.name = random.choice(["Leia", "Rey", "Amilyn", "Ashoka", "Padmé"])
        self.planet = random.choice(["Alderaan", "Bespin", "Dagobah", "Hoth", "Tatooine"])

    def print_info(self):
        print("Id:" + str(self.jedi_id).rjust(5) + "| Name:".rjust(8) + self.name.rjust(15) + "| Planet:".rjust(10)
              + self.planet.rjust(10) + "| Age:".rjust(7) + str(self.age).rjust(4)
              + "| Type (mark):".rjust(15) + self.mark.rjust(3) + " |")

    def aging(self):
        self.age += 1
        if self.age >= 2:
            if self.sex == "m":
                self.mark = "M"
            else:
                self.mark = "F"

    def get_mark(self):
        return self.mark

    def get_planet(self):
        return self.planet

    def get_id(self):
        return self.jedi_id

    def is_too_old(self):
        if self.age > 10:
            return True
        else:
            return False


class EvilJedi(Jedi):
    def __init__(self, jedi_id, mother_jedi=None):
        super(EvilJedi, self).__init__(jedi_id, mother_jedi)
        self.time_no_bite = 0
        self.mark = "S"
        self.name = random.choice(["Darth Maul", "Darth Vader", "Darth Tyranus", "Darth Sidious", "Darth Bane"])

    def set_time_no_bite(self, bite):
        self.time_no_bite = bite

    def get_time_no_bite(self):
        return self.time_no_bite

    def aging(self):
        self.age += 1

    def is_too_old(self):
        if self.age >= 50:
            return True
        else:
            return False


class Universe(object):
    jedi = [Jedi(1), Jedi(2), Jedi(3), Jedi(4), Jedi(5)]
    year = 0
    next_jedi_id = 6

    def print_situation(self):
        if len(self.jedi) > 0:
            if self.year > 0:
                print("Situation at the end of the year " + str(self.year) + " -> size: "
                      + str(len(self.jedi)) + " Jedi.")
            else:
                print("A new universe is born. Starting situation -> size: " + str(len(self.jedi)) + " Jedi.")
            for j in self.jedi:
                j.print_info()
        else:
            print("Year " + str(self.year) + ": the universe is empty")

    def generate_a_new_jedi(self, mother):
        chance = random.randint(1, 100)
        # there is the 25% to generate an evil jedi
        if chance <= 25:
            self.jedi.append(EvilJedi(self.next_jedi_id, mother.get_planet()))
        else:
            self.jedi.append(Jedi(self.next_jedi_id, mother.get_planet()))
        print(str(self.jedi[len(self.jedi) - 1].get_id()) + " is born")
        self.next_jedi_id += 1

    def the_force_awakens(self):
        # if the jedi population exceeds 10 the force must kill exactly half of the jedi
        if len(self.jedi) > 10:
            to_kill = []
            number_of_jedi_to_kill = round(len(self.jedi) / 2)
            for i in range(1, number_of_jedi_to_kill):
                while True:
                    next_victim = self.jedi[random.randint(0, len(self.jedi) - 1)]
                    if next_victim not in to_kill:
                        to_kill.append(next_victim)
                        break
            print("Too many jedi. The force kills:")
            for k in to_kill:
                print(k.get_id())
                self.jedi.remove(k)

    def revenge_of_sith(self):
        to_kill = []
        # a evil jedi had the 80% chance to kill another jedi (suicide is not allowed)
        for j in self.jedi:
            if j.get_mark() == "S":
                killing = random.randint(1, 100)
                if killing <= 80:
                    next_victim = random.randint(0, len(self.jedi) - 1)
                    if is_not_the_same_jedi(j, self.jedi[next_victim]):
                        print(str(self.jedi[next_victim].get_id()) + " is killed by " + str(j.get_id()))
                        to_kill.append(self.jedi[next_victim])
                        j.set_time_no_bite(0)
                    else:
                        j.set_time_no_bite(j.get_time_no_bite() + 1)
                else:
                    j.set_time_no_bite(j.get_time_no_bite() + 1)
        # filter of the clones of the same dead jedi because there is the chance that there are more than 1 killer
        # for the same victim so more identical item in to_kill
        to_kill_without_clones = list(set(to_kill))
        for dead in to_kill_without_clones:
            self.jedi.remove(dead)

    def aging(self):
        self.year += 1

        for j in self.jedi:
            j.aging()

        for j in self.jedi:
            if j.get_mark() == "M":
                for f in self.jedi:
                    if f.get_mark() == "F":
                        # if exists a mature male(age >= 2) and a mature female(age >= 2) now I create a new jedi
                        self.generate_a_new_jedi(f)
                break

        # if a jedi becomes older then 10 years dies, evil jedi dies when are 50 years old
        too_old = []
        for j in self.jedi:
            if j.is_too_old():
                print(str(j.get_id()) + " died of old age")
                too_old.append(j)
        for dead in too_old:
            self.jedi.remove(dead)

        # the evil jedi attack the other jedi with 80% chance of success
        self.revenge_of_sith()

        too_good = []
        # an evil jedi must die if does not kill a jedi for 15 turns
        for j in self.jedi:
            if j.get_mark() == "S" and j.get_time_no_bite() >= 15:
                print(str(j.get_id()) + " died because of his inactivity")
                too_good.append(j)
        for dead in too_good:
            self.jedi.remove(dead)

        # if there are too many jedi the force must kill half of them
        if len(self.jedi) > 10:
            self.the_force_awakens()

        self.print_situation()


# i made this function to avoid that a evil jedi could do suicide
def is_not_the_same_jedi(x, y):
    if x.get_id() == y.get_id():
        return False
    return True


def main():
    universe = Universe()
    universe.print_situation()
    while True:
        choice = input("Press Enter to continue or Q to quit...\n")
        if choice == "q" or choice == "Q":
            sys.exit(0)
        else:
            universe.aging()


if __name__ == "__main__":
    main()
