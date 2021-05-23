import random

from oop_hack.arena import Arena
from oop_hack.battle_log import BattleLog
from oop_hack.battle_log import Importance
from oop_hack.equipment import ThingsConstructor
from oop_hack.params import MAX_THINGS_COUNT
from oop_hack.params import PEOPLE_COUNT
from oop_hack.user_custom_fighter import SUPERMAN
from oop_hack.user_custom_fighter import SUPER_THINGS
from oop_hack.warrior import PeopleConstructor


def main():
    BattleLog()
    BattleLog().log(Importance.very_important, '# Morituri te salutant')

    innocents_with_things = [
        (PeopleConstructor.get_human(),
         ThingsConstructor.get_several_things(
             random.randint(0, MAX_THINGS_COUNT)))
        for i in range(PEOPLE_COUNT)
    ]

    innocents_with_things.append((SUPERMAN, SUPER_THINGS))

    arena = Arena(innocents_with_things)

    while arena.show_must_go_on():
        for i in range(PEOPLE_COUNT):
            if not arena.fight_two_random():
                break
        else:
            arena.end_the_round()

    BattleLog().close_files()


if __name__ == '__main__':
    main()
