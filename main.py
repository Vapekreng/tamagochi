import random

MIN_HEALTH = 0
MAX_HEALTH = 100
MIN_HUNGER = 0
MAX_HUNGER = 100
MIN_TIRED = 0
MAX_TIRED = 100
MIN_MOOD = 0
MAX_MOOD = 100
BASE_HUNGER_GET = 1
AVERAGE_HUNGER = 50
STRONG_HUNGER = 80
BASE_TIRE_GET = 1
BASE_TIER_LOSE = -5
BASE_MOOD_LOSE = 1
BASE_HEALTH_LOSE = -1
GOOD_TIRE = 40
BAD_TIRE = 80
BAD_MOOD = 20
INIT_VIRUSES_TIME_LEFT = [0, 0]
FIRST_VIRUS_TIME = 20
FIRST_VIRUS_TIRE_RESTRICTION = 20
FIRST_VIRUS_HEALTH_RESTRICTION = 80
SECOND_VIRUS_TIME = 10
SECOND_VIRUS_HUNGER_RESTRICTION = 66
ALIVE = 'Жив'
DEAD = 'Умер'
IS_NOT_HUNGRY = 'Сыт'
IS_HUNGRY = 'Голоден'
ILL = 'Болен'
NOT_ILL = 'Здоров'
START_CONDITION = [ALIVE, IS_NOT_HUNGRY, NOT_ILL]


class Tamagochi:

    def __init__(self):
        self.health = MAX_HEALTH
        self.hunger = MIN_HUNGER
        self.tired = MIN_TIRED
        self.mood = MAX_MOOD
        self.sleep = True
        self.viruses = INIT_VIRUSES_TIME_LEFT
        self.condition = START_CONDITION

    def _set_condition(self):
        if self.health > 0:
            self.condition[0] = ALIVE
        else:
            self.condition[0] = DEAD

        if self.hunger > AVERAGE_HUNGER:
            self.condition[1] = IS_HUNGRY
        else:
            self.condition[1] = IS_NOT_HUNGRY

        if self.viruses[0] + self.viruses[1] == 0:
            self.condition[2] = NOT_ILL
        else:
            self.condition[2] = ILL

    def _change_health(self, count_of_health):
        self.health += count_of_health
        if self.health < MIN_HEALTH:
            self.health = MIN_HEALTH
        if self.health > MAX_HEALTH:
            self.health = MAX_HEALTH

    def _change_hunger(self, count_of_hunger):
        self.hunger += count_of_hunger
        if self.hunger > MAX_HUNGER:
            self.hunger = MAX_HUNGER
        if self.hunger < MIN_HUNGER:
            self.hunger = MIN_HUNGER

    def _change_tired(self, count_of_tired):
        self.tired += count_of_tired
        if self.tired > MAX_TIRED:
            self.tired = MAX_TIRED
        if self.tired < MIN_TIRED:
            self.tired = MIN_TIRED

    def _change_mood(self, count_of_mood):
        self.mood += count_of_mood
        if self.mood > MAX_MOOD:
            self.mood = MAX_MOOD
        if self.mood < MIN_MOOD:
            self.mood = MIN_MOOD

    def _check_hunger(self):
        if self.hunger > AVERAGE_HUNGER:
            self.tired += BASE_TIRE_GET
            self.mood -= BASE_MOOD_LOSE
        if self.hunger > STRONG_HUNGER:
            self._change_health(BASE_HEALTH_LOSE)

    def _check_tired(self):
        if self.tired > BAD_TIRE:
            self.sleep = False
        if self.sleep < GOOD_TIRE:
            self.sleep = True

    def _check_mood(self):
        if self.mood < BAD_MOOD:
            self._change_health(BASE_HEALTH_LOSE)

    def _check_if_sleep(self):
        if self.sleep:
            self._change_tired(BASE_TIRE_GET)
        else:
            self._change_tired(BASE_TIER_LOSE)

    def _check_for_infection(self):
        infected = random.random() < ((100 - self.health) / 100)
        if infected:
            self._add_virus()

    def _add_virus(self):
        if self.viruses[0] == 0:
            self.viruses[0] = FIRST_VIRUS_TIME
        elif self.viruses[1] == 0:
            self.viruses[1] = SECOND_VIRUS_TIME

    def _virus_attack(self):
        if self.viruses[0] > 0:
            self.viruses[0] -= 1
            self._first_virus_attack()
        if self.viruses[1] > 0:
            self.viruses[1] -= 1
            self._second_virus_attack()

    def _first_virus_attack(self):
        if self.tired < FIRST_VIRUS_TIRE_RESTRICTION:
            self.tired = FIRST_VIRUS_TIRE_RESTRICTION
        if self.health > FIRST_VIRUS_HEALTH_RESTRICTION:
            self.health = FIRST_VIRUS_HEALTH_RESTRICTION

    def _second_virus_attack(self):
        if self.hunger < SECOND_VIRUS_HUNGER_RESTRICTION:
            self.hunger = SECOND_VIRUS_HUNGER_RESTRICTION

    def tick(self):
        self._change_hunger(BASE_HUNGER_GET)
        self._check_hunger()
        self._check_if_sleep()
        self._check_tired()
        self._change_mood(BASE_MOOD_LOSE)
        self._check_mood()
        self._check_for_infection()
        self._virus_attack()
        self._set_condition()

    def party(self):
        if self.Alive():
            new_mood = random.randint(-5, 20)
            self._change_mood(new_mood)
            lose = random.randint(5, 15)
            self._change_tired(lose)
            self._change_hunger(lose)

    def eat(self):
        if self.Alive() and self.sleep:
            food = random.randint(10, 20)
            self._change_hunger(-food)
            self._change_tired(-food)
            self._change_mood(food)
            self._change_health(food)

    def Alive(self):
        is_alive = self.condition[0] == ALIVE
        return is_alive
