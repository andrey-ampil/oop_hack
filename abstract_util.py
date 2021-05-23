from abc import ABC


class AbstractFighter(ABC):

    def attack(self, other, targets):
        pass

    def try_to_defend(self, other):
        pass

    def cast_spells(self, moment, targets):
        pass

    def take_spell_in_face(self, magician, spell):
        pass

    def blood_rage(self):
        pass

    def dead_should_be_dead(self):
        pass

    def is_alive(self):
        pass
