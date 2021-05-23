import random
import time
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union

from oop_hack.battle_log import BattleLog
from oop_hack.battle_log import Importance
from oop_hack.equipment import Thing
from oop_hack.utils import Moment
from oop_hack.utils import Target
from oop_hack.warrior import Fighter
from oop_hack.warrior import Person


class Morituri:
    def __init__(self, morituri: List[Fighter]):
        self.morituri = morituri

    def __iter__(self):
        for fighter in self.morituri:
            yield fighter

    def __len__(self):
        lenght = len(self.morituri)
        print(lenght)
        return len(self.morituri)

    def clear_battlefield(self):
        self.morituri = [fighter
                         for fighter in self.morituri
                         if fighter.is_alive()]
        return self.morituri

    def take_random_targets(self):
        morituri = self.morituri[::]
        random.shuffle(morituri)
        attacker = morituri.pop()
        defender = morituri.pop()
        return self.targets(attacker, defender)

    def targets(self, attacker, defender
                ) -> Dict[Target, Union[Fighter, None]]:
        return {
            Target.me: attacker,
            Target.enemy: defender,
            Target.random: random.choice(self.morituri)
        }

    def cast_in_turn(self):
        morituri = self.morituri[::]
        for fighter in morituri:
            if fighter in self.morituri:
                yield self.targets(fighter, None)

    def weakest(self):
        return min(self.morituri, key=lambda fighter: fighter.damage)


class Arena:
    def __init__(self,
                 people_with_things: List[Tuple[Person, Sequence[Thing]]]
                 ):
        fighters = self.prepare_fighters(people_with_things)
        self.morituri = Morituri(fighters)
        self.round = 0
        self.new_round()

    def new_round(self):
        self.round += 1
        BattleLog().log(Importance.very_important, f'## Round {self.round}!')

    @staticmethod
    def prepare_fighters(people_with_things) -> List[Fighter]:
        return [
            Fighter(person, things)
            for person, things in people_with_things
        ]

    def fight_two_random(self):
        if not self.show_must_go_on(log=False):
            return False
        targets = self.morituri.take_random_targets()
        attacker = targets[Target.me]
        defender = targets[Target.enemy]
        attacker.attack(defender, targets)
        self.clear_battlefield()
        return True

    def clear_battlefield(self):
        self.morituri = Morituri(self.morituri.clear_battlefield())

    def end_the_round(self):
        if not self.show_must_go_on(log=False):
            return False
        BattleLog().log(
            Importance.very_important,
            '# Apply end of round spells'
        )
        for targets in self.morituri.cast_in_turn():
            targets[Target.me].cast_spells(Moment.end_round, targets)
            self.clear_battlefield()

        if self.show_must_go_on():
            self.morituri.weakest().blood_rage()
            self.new_round()
        time.sleep(0.1)
        return True

    def show_must_go_on(self, log=True):
        self.clear_battlefield()
        if len(self.morituri) > 1:
            return True
        elif len(self.morituri) == 0:
            if log:
                BattleLog().log(Importance.very_important, 'EVERYONE ARE DEAD')
            return False
        if log:
            winner = self.morituri.morituri[0]
            message = (f'Winner now {winner.name} congratulations!\n '
                       f'Health remaining {winner.hp}.')
            BattleLog().log(Importance.very_important, message)
        return False
