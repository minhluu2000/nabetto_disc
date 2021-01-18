from typing import Dict, List, Tuple


from cassiopeia import Summoner, Queue
from cassiopeia import apply_settings
from cassiopeia.core.spectator import Participant
from datapipelines.common import NotFoundError

apply_settings("./lib/riotapi/cass_settings.json")

class Match:
    @staticmethod
    def current_match_check(name: str, region: str) -> bool:
        try:
            s = Summoner(name=name, region=region)
            return s.current_match.exists
        except NotFoundError:
            return False

class CurrentMatch:
    def __init__(self, name: str, region: str):
        self._current_match = Summoner(name=name, region=region).current_match

    @property
    def teams(self) -> Dict:
        return {
            "blue_team": self._current_match.blue_team.participants,
            "red_team":self._current_match.red_team.participants
        }
        
    @property
    def queue(self) -> Queue:
        return self._current_match.queue
        


if __name__ == "__main__":
    pass