from oop_hack.equipment import Magic
from oop_hack.equipment import MagicThing
from oop_hack.params import HumanParams
from oop_hack.params import MAX_THINGS_COUNT
from oop_hack.params import MagicParams
from oop_hack.params import ThingParams
from oop_hack.utils import Moment
from oop_hack.utils import Target
from oop_hack.warrior import Person

SUPERMAN = Person(
    'SUPERMAN',
    HumanParams.max_health_points,
    HumanParams.max_damage,
    HumanParams.max_armor
)

SUPER_THINGS = [
    MagicThing(
        ThingParams.max_hp, ThingParams.max_attack, ThingParams.max_armor,
        Magic(MagicParams.max_value, Moment.on_hit, Target.enemy)
    )
    for i in range(MAX_THINGS_COUNT - 1)
]

# чутка ослабим
SUPER_THINGS.append(
    MagicThing(
        ThingParams.max_hp, ThingParams.max_attack, ThingParams.max_armor,
        Magic(MagicParams.max_value, Moment.on_hit, Target.me)
    )
)
