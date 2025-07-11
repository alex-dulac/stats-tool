from typing import List

from fastapi import Depends
from sqlalchemy import func
from sqlmodel import select, distinct
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_db
from app.models import Stats


def build_query(fields, season: int = None, player_list: List[str] = None) -> select:
    query = select(*fields)
    if season:
        query = query.where(Stats.season == season)
    if player_list:
        query = query.where(Stats.player_name.in_(player_list))

    return query

class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db


class StatsService(BaseService):
    async def get_stats(self):
        # Query to select all rows from the 'Stats' table
        # Normally, we would want to be more methodical about this, with limits/pagination for example
        # for this demonstration, we'll use a simple select statement since we know the data
        query = select(Stats).order_by(Stats.player_name, Stats.season.desc())
        result = await self.db.exec(query)
        return result.all()

    async def get_players(self):
        # Returns a list of distinct player names from the 'Stats' table
        query = select(distinct(Stats.player_name)).order_by(Stats.player_name)
        result = await self.db.exec(query)
        return result.all()

    async def get_stats_by_player_name(self, player_name: str):
        query = select(Stats).where(Stats.player_name == player_name)
        result = await self.db.exec(query)
        return result.all()

    async def get_goals_assists_chart_data(self, season: int = None, player_list: List[str] = None):
        fields = [
            Stats.player_name,
            Stats.team,
            Stats.season,
            Stats.goals,
            Stats.assists,
            Stats.points,
        ]

        query = build_query(fields, season, player_list)
        result = await self.db.exec(query.order_by(Stats.points.desc()))

        data = [
            {
                "player_name": row[0],
                "team": row[1],
                "season": row[2],
                "goals": row[3],
                "assists": row[4],
                "points": row[5],
            }
            for row in result.all()
        ]

        return data

    async def get_production_chart_data(self, season: int = None, player_list: List[str] = None):
        toi_per_game = (Stats.toi / Stats.gp).label("toi_per_game")
        points_per_game = (Stats.points / Stats.gp).label("points_per_game")

        fields = [
            Stats.player_name,
            Stats.team,
            Stats.season,
            toi_per_game,
            points_per_game
        ]

        query = build_query(fields, season, player_list)
        query = query.where(Stats.gp > 0)
        result = await self.db.exec(query.order_by(points_per_game.desc()))

        data = [
            {
                "player_name": row[0],
                "team": row[1],
                "season": row[2],
                "toi_per_game": round(row[3], 2) if row[3] is not None else 0,
                "points_per_game": round(row[4], 2) if row[4] is not None else 0
            }
            for row in result.all()
        ]

        return data

    async def get_shooting_efficiency_chart_data(self, season: int = None, player_list: List[str] = None):
        shooting_efficiency = (Stats.goals / Stats.shots).label("shooting_efficiency")

        fields = [
            Stats.player_name,
            Stats.team,
            Stats.season,
            Stats.goals,
            Stats.shots,
            shooting_efficiency
        ]

        query = build_query(fields, season, player_list)
        query = query.where(Stats.shots > 0)
        result = await self.db.exec(query.order_by(shooting_efficiency.desc()))

        data = [
            {
                "player_name": row[0],
                "team": row[1],
                "season": row[2],
                "goals": row[3],
                "shots": row[4],
                "shooting_efficiency": round(row[5], 4) if row[5] is not None else 0,
            }
            for row in result.all()
        ]

        return data

    async def get_per_game_consistency_chart_data(self, season: int = None, player_list: List[str] = None):
        goals_per_game = (Stats.goals / Stats.gp).label("goals_per_game")
        assists_per_game = (Stats.assists / Stats.gp).label("assists_per_game")
        shots_per_game = (Stats.shots / Stats.gp).label("shots_per_game")
        toi_per_game = (Stats.toi / Stats.gp).label("toi_per_game")

        fields = [
            Stats.player_name,
            Stats.team,
            Stats.season,
            goals_per_game,
            assists_per_game,
            shots_per_game,
            toi_per_game,
        ]

        query = build_query(fields, season, player_list)
        result = await self.db.exec(query)

        data = [
            {
                "player_name": row[0],
                "team": row[1],
                "season": row[2],
                "goals_per_game": round(row[3], 2) if row[3] is not None else 0,
                "assists_per_game": round(row[4], 2) if row[4] is not None else 0,
                "shots_per_game": round(row[5], 2) if row[5] is not None else 0,
                "toi_per_game": round(row[6], 2) if row[6] is not None else 0,
            }
            for row in result.all()
        ]

        return data

    async def get_scouting_heatmap_chart_data(self):
        query = select(
            Stats.season,
            Stats.scouting_grade,
            func.avg(Stats.points).label("average_points")
        ).group_by(Stats.season, Stats.scouting_grade)

        result = await self.db.exec(query)

        data = [
            {
                "season": row[0],
                "scouting_grade": row[1],
                "average_points": round(row[2], 2) if row[2] is not None else 0
            }
            for row in result.all()
        ]
        return data
