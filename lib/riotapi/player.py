import datetime
from typing import List
from cassiopeia.core.match import Participant

from discord import Embed

from merakicommons.container import SearchError
from datapipelines.common import NotFoundError
from cassiopeia import Summoner, Queue, Champion
from cassiopeia import apply_settings

default_settings = {
    "settings": {
        "default_region": "NA"
    },
    "RiotAPI": {
        "api_key": "RIOT_API_KEY"
    },
    "logging": {
        "print_calls": False,
        "print_riot_api_key": False
    }
}

apply_settings(default_settings)

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
        try:
            return (f"{self._entries[self._mode].tier} "
                    f"{self._entries[self._mode].division} " 
                    f"{self._entries[self._mode].league_points} LP")
        except SearchError:
            return -1

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

class Match:
    @staticmethod
    def ingame_check(name: str, region: str) -> bool:
        try:
            s = Summoner(name=name, region=region)
            return s.current_match.exists
        except NotFoundError:
            return False

    @staticmethod
    def ingame_info(name: str, region: str) -> Embed:
        
        if Match.ingame_check(name, region):
            s = Summoner(name=name, region=region)
            embed = Embed(title=f"Current match with {name}", description=f"{s.current_match.mode}")
            blue_team: List[Participant] = s.current_match.blue_team.participants
            for participant in blue_team:
                participant.summoner.name
            blue_team_str = '\n'.join(blue_team)
            embed.add_field(name="Blue Team", value=blue_team_str)
            red_team: List[Participant] = s.current_match.red_team.participants
            red_team_str = '\n'.join(red_team)
            embed.add_field(name="Red Team", value=red_team_str)
            return embed
            pass
        return




if __name__ == "__main__":
    p = Player("SheepForest", Queue.ranked_solo_fives, 'NA')
    print(Match.ingame_info("princesspower", "NA"))
