import random
from typing import Dict
from typing import List
from typing import Sequence
from typing import Union

from oop_hack.abstract_util import AbstractFighter
from oop_hack.battle_log import BattleLog
from oop_hack.battle_log import Importance
from oop_hack.equipment import Magic
from oop_hack.equipment import MagicThing
from oop_hack.equipment import Thing
from oop_hack.params import HumanParams
from oop_hack.params import MAX_THINGS_COUNT
from oop_hack.utils import Moment
from oop_hack.utils import Target


def is_alive_check(method):
    def checker(self: 'Fighter', *args, **kwargs):
        if self.hp > 0:
            return method(self, *args, **kwargs)
        return self.dead_should_be_dead()
    return checker


class Person:

    def __init__(self, name, health_points, damage, armor):
        self.name = name
        self.base_hp = health_points
        self.base_damage = damage
        self.base_armor = armor
        self.equipment = []  # type: List[Union[Thing, MagicThing]]

        self._combat_hp = None
        self._combat_damage = None
        self._combat_defence = None

    def prepare_to_die(self, things: Sequence[Thing]):
        self.add_things(things)
        self.calculate_combat_characteristics()

    def add_things(self, things: Sequence[Thing]):
        if len(things) + len(self.equipment) > MAX_THINGS_COUNT:
            raise RuntimeError(f'Max {MAX_THINGS_COUNT} weapons to persons')
        for thing in things:
            self.equipment.append(thing)
            self.write_thing_stats(thing)

    def write_thing_stats(self, thing: Thing):
        message = (f'{self.name} wear {thing.name} with stats: {thing.hp} HP, '
                   f'{thing.attack} attack and {thing.armor} armor')
        BattleLog().log(
            Importance.important,
            message
        )

    def calculate_combat_characteristics(self):
        self.calculate_combat_hp()
        self.calculate_combat_damage()
        self.calculate_combat_defence()

    @property
    def combat_hp(self):
        return self._combat_hp

    def calculate_combat_hp(self):
        self._combat_hp = self.base_hp
        for item in self.equipment:
            self._combat_hp += item.hp

    @property
    def combat_damage(self):
        return self._combat_damage

    def calculate_combat_damage(self):
        self._combat_damage = self.base_damage
        for item in self.equipment:
            self._combat_damage += item.attack

    @property
    def combat_defence(self):
        return self._combat_defence

    def calculate_combat_defence(self):
        total_armor = self.base_armor
        for item in self.equipment:
            total_armor += item.armor
        self._combat_defence = (0.06 * total_armor) / \
                               (1 + 0.06 * abs(total_armor))


class Warrior(Person):
    def __init__(self, name, health_points, damage, armor):
        super().__init__(name, health_points, damage * 2, armor)


class Paladin(Person):
    def __init__(self, name, health_points, damage, armor):
        super().__init__(name, health_points * 2, damage, armor * 2)


class Fighter(AbstractFighter):
    def __init__(self, person: Person, things: Sequence[Thing]):
        person.prepare_to_die(things)
        self.name = person.name
        self.hp = person.combat_hp
        self.damage = person.combat_damage
        self.defence = person.combat_defence
        self.weapons = person.equipment  # type: List[Union[Thing, MagicThing]]
        self.write_characteristics()
        self.last_event = None

    def write_characteristics(self):
        message = (f'{self.name} have {self.hp} HP, {self.damage} damage '
                   f'and {self.defence} resist.')
        BattleLog().log(
            Importance.very_important,
            message
        )

    @is_alive_check
    def attack(self, other: 'Fighter', targets: Dict[Target, 'Fighter']):
        other.try_to_defend(self)
        if other.is_alive(log=False):
            self.cast_spells(moment=Moment.on_hit, targets=targets)

    @is_alive_check
    def try_to_defend(self, other: 'Fighter'):
        reduced_damage = other.damage * (1 - self.defence)
        self.hp -= reduced_damage
        self.last_event = (f'{other.name} attack with strength {other.damage} '
                           f'and deal {reduced_damage} damage')
        message = f'{self.name} affected by {self.last_event}'
        BattleLog().log(Importance.not_important, message)

    @is_alive_check
    def cast_spells(self, moment: Moment, targets: Dict[Target, 'Fighter']):
        for item in self.weapons:
            item.apply_effect(self.name, moment, targets)

    @is_alive_check
    def take_spell_in_face(self, magician, spell: Magic):
        self.hp -= spell.value
        self.last_event = f'{magician} apply {spell.name}'
        message = f'{self.name} affected by {self.last_event}'
        BattleLog().log(Importance.not_important, message)

    @is_alive_check
    def blood_rage(self):
        self.damage *= 2
        BattleLog().log(
            Importance.very_important,
            f'{self.name} in BLOOD RAGE'
        )

    def dead_should_be_dead(self):
        pass

    def is_alive(self, log=True):
        if self.hp > 0:
            return True
        if log:
            message = f'Brave {self.name} died by {self.last_event}'
            BattleLog().log(Importance.very_important, message)
        return False


class PeopleConstructor:
    available_persons = [Person, Warrior, Paladin]

    @classmethod
    def get_human(cls):
        human_type = random.choice(cls.available_persons)
        human_params = HumanParams.get_random_human_params()
        return human_type(**human_params)
