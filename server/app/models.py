from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


TEAM_MAPPING = {
    "ANA": "Anaheim Ducks",
    "BOS": "Boston Bruins",
    "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes",
    "CBJ": "Columbus Blue Jackets",
    "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NJD": "New Jersey Devils",
    "NSH": "Nashville Predators",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SEA": "Seattle Kraken",
    "SJS": "San Jose Sharks",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "UTA": "Utah Mammoth",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals",
}


class Stats(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    season: int = Field(index=True)
    player_name: str = Field(index=True) # trusting the format is "Last, First" for simplicity
    team: str = Field(index=True)
    gp: int = Field()
    toi: int = Field()
    shots: int = Field()
    goals: int = Field()
    assists: int = Field()
    points: int = Field()
    scouting_grade: int = Field()

    @property
    def team_full_name(self) -> str:
        return TEAM_MAPPING.get(self.team, "Unknown Team")

    @property
    def toi_per_game(self) -> float:
        return round(self.toi / self.gp, 2) if self.gp > 0 else 0.0

    @property
    def goals_per_game(self) -> float:
        return round(self.goals / self.gp, 2) if self.gp > 0 else 0.0

    @property
    def assists_per_game(self) -> float:
        return round(self.assists / self.gp, 2) if self.gp > 0 else 0.0

    @property
    def points_per_game(self) -> float:
        return round(self.points / self.gp, 2) if self.gp > 0 else 0.0

    @property
    def shots_per_game(self) -> float:
        return round(self.shots / self.gp, 2) if self.gp > 0 else 0.0

    @property
    def shooting_percentage(self) -> float:
        # percentage of shots that are goals
        return round(self.goals / self.shots * 100, 1) if self.shots > 0 else 0.0

    # more ...
    # def plus_minus(self):
    #     pass

# Naming things can be hard sometimes
class StatsExtended(BaseModel):
    id: int
    season: int
    player_name: str
    team: str
    team_full_name: str
    gp: int
    toi: float
    toi_per_game: float
    shots: int
    shots_per_game: float
    shooting_percentage: float
    goals: int
    goals_per_game: float
    assists: int
    assists_per_game: float
    points: int
    points_per_game: float
    scouting_grade: int


async def stat_to_extended_model(stat: Stats) -> StatsExtended:
    return StatsExtended(
        **stat.model_dump(),
        team_full_name=stat.team_full_name,
        toi_per_game=stat.toi_per_game,
        shots_per_game=stat.shots_per_game,
        goals_per_game=stat.goals_per_game,
        assists_per_game=stat.assists_per_game,
        points_per_game=stat.points_per_game,
        shooting_percentage=stat.shooting_percentage
    )
