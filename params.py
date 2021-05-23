import random

from oop_hack.utils import Moment
from oop_hack.utils import Target


MAX_THINGS_COUNT = 4
PEOPLE_COUNT = 10


class ThingParams:
    max_hp = 100
    max_attack = 20
    max_armor = 4

    @classmethod
    def get_random_thing_params(cls):
        hp = random.randint(-cls.max_hp, cls.max_hp)
        attack = random.randint(0, cls.max_attack)
        armor = random.randint(-cls.max_armor, cls.max_armor)

        return dict(health_points=hp, attack=attack, armor=armor)
        # return hp, attack, armor


class MagicParams:
    max_value = 100
    available_moments = list(Moment.__members__.values())
    available_targets = list(Target.__members__.values())

    @classmethod
    def get_random_magic_params(cls):
        value = random.randint(-cls.max_value, cls.max_value)
        moment = random.choice(cls.available_moments)

        available_targets = cls.available_targets
        if moment == Moment.end_round:
            available_targets = list(filter(
                lambda target_: target_ != Target.enemy,
                available_targets
            ))
        target = random.choice(available_targets)

        return dict(value=value, moment=moment, target=target)


class HumanParams:
    available_names = ['alpha', 'beta', 'gamma']
    available_second_names = ['coward', 'strong', 'brash']
    min_health_points = 300
    max_health_points = 500
    min_damage = 50
    max_damage = 100
    max_armor = 10

    @classmethod
    def get_random_human_params(cls):
        first_name = random.choice(cls.available_names)
        second_name = random.choice(cls.available_second_names)
        name = f'{first_name} {second_name}'.upper()
        hp = random.randint(cls.min_health_points, cls.max_health_points)
        damage = random.randint(cls.min_damage, cls.max_damage)
        armor = random.randint(0, cls.max_armor)

        return dict(
            name=name,
            health_points=hp,
            damage=damage,
            armor=armor
        )
