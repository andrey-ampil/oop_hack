import random
from typing import Dict

from oop_hack.abstract_util import AbstractFighter
from oop_hack.params import MagicParams
from oop_hack.params import ThingParams
from oop_hack.utils import Moment
from oop_hack.utils import Target


class Thing:
    def __init__(self, health_points: float, attack: float, armor: int):
        self.hp = health_points
        self.attack = attack
        self.armor = armor
        self.name = self.construct_name()

    def construct_name(self):
        name = ''
        if self.hp > 0:
            name += 'HEALTH increase, '
        elif self.hp < 0:
            name += 'HEALTH reduction, '

        if self.attack > 0:
            name += 'ATTACK increase, '
        elif self.attack < 0:
            name += 'ATTACK reduction, '

        if self.armor > 0:
            name += 'DEFENCE increase, '
        elif self.armor < 0:
            name += 'DEFENCE reduction, '

        if self.hp != 0 and self.armor != 0:
            name += 'ROBE '
            if self.attack > 0 and self.hp < 0:
                name += 'with spikes outwards and inside '
            elif self.attack > 0:
                name += 'with spikes outwards '
            elif self.hp < 0:
                name += 'with spikes inside '
        elif self.attack != 0:
            name += 'SWORD'
        else:
            name += 'RING'

        return name

    def apply_effect(self, magician, moment, targets):
        pass


class Magic:

    def __init__(self, value: int, moment: Moment, target: Target):
        self.value = value
        self.moment = moment
        self.target = target
        self.name = self.construct_name()

    def construct_name(self):
        if self.value > 0:
            name = 'fireball'
        else:
            name = 'heal'
        return f'{name} {self.target.name} {self.moment.name}'


class MagicThing(Thing):

    def __init__(self,
                 health_points: float,
                 attack: float,
                 armor: int,
                 effect: Magic):
        super().__init__(health_points, attack, armor)
        self.effect = effect
        self.update_name()

    def update_name(self):
        self.name += f' of {self.effect.name}'

    def apply_effect(self, magician, moment,
                     targets: Dict[Target, AbstractFighter]):
        effect = self.effect
        if effect.moment != moment:
            return
        targets[effect.target].take_spell_in_face(magician, effect)


class ThingsConstructor:

    @classmethod
    def get_several_things(cls, count):
        return [cls.get_thing() for i in range(count)]

    @classmethod
    def get_thing(cls):
        if random.randint(0, 1):
            return cls.get_magic_thing()
        return cls.get_simple_thing()

    @staticmethod
    def get_magic_thing():
        thing_params = ThingParams.get_random_thing_params()
        magic_params = MagicParams.get_random_magic_params()
        thing_params.update(effect=Magic(**magic_params))
        return MagicThing(**thing_params)

    @staticmethod
    def get_simple_thing():
        thing_params = ThingParams.get_random_thing_params()
        return Thing(**thing_params)
