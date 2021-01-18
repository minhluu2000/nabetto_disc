import datetime
from typing import List

from discord import Embed

from merakicommons.container import SearchError
from datapipelines.common import NotFoundError
from cassiopeia import Summoner, Queue, Champion
from cassiopeia import apply_settings

from .data import QUEUE_ANNOTATES

apply_settings("./lib/riotapi/cass_settings.json")

class Player:
    def __init__(self, name: str, mode: Queue, region: str):
        self._summoner = Summoner(name=name, region=region)
        self._mode = mode
        self._entries = self._summoner.league_entries
    
    @property
    def name(self):
        return self._summoner.name

    @property
    def id(self):
        return self._summoner.id

    @property
    def level(self):
        return self._summoner.level

    @property
    def icon_url(self):
        return self._summoner.profile_icon.url

    @property
    def rank(self) -> str:
        queue_priorities = [self._mode, Queue.ranked_solo_fives, Queue.ranked_flex_fives]

        for queue in queue_priorities:
            try:
                entry = self._entries[queue]
                break
            except SearchError:
                pass

        else:
            return "Unknown"

        return (f"{entry.tier} "
        f"{entry.division} " 
        f"{entry.league_points} LP"
        f" ({QUEUE_ANNOTATES[queue]})")


    @property
    def wins(self) -> int:
        try: 
            return self._entries[self._mode].wins
        except SearchError:
            return -1

    @property
    def losses(self) -> int:
        try: 
            return self._entries[self._mode].losses
        except SearchError:
            return -1

    @property
    def winrate(self) -> float:
        if self.wins + self.losses < 0:
            return -1
        else:
            return (self.wins / (self.wins + self.losses)) * 100



if __name__ == "__main__":
    p = Player("SheepForest", Queue.ranked_solo_fives, 'NA')
