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

    async def get_head_to_head_data(self, player_list: List[str], season: int = None):
        """
        Method that retrieves data for two players and compares their stats,
        deciding on a winner based on different criteria.
        It is pretty simplistic and could be expanded upon in a real-world scenario with more complex criteria.
        """
        if len(player_list) != 2:
            return {"error": "Exactly two players required for comparison"}

        player1, player2 = player_list

        query = select(Stats).where(Stats.player_name.in_([player1, player2]))
        if season:
            query = query.where(Stats.season == season)

        result = await self.db.exec(query)
        stats = result.all()

        player1_stats = [s for s in stats if s.player_name == player1]
        player2_stats = [s for s in stats if s.player_name == player2]

        if not player1_stats or not player2_stats:
            raise BaseException("One or both players not found for the specified criteria")

        def calculate_player_stats(player_stats, player_name):
            total_goals = sum(s.goals for s in player_stats)
            total_assists = sum(s.assists for s in player_stats)
            total_points = sum(s.points for s in player_stats)
            total_games = sum(s.gp for s in player_stats)
            total_shots = sum(s.shots for s in player_stats)
            total_toi = sum(s.toi for s in player_stats)
            avg_scouting_grade = sum(s.scouting_grade for s in player_stats) / len(player_stats)

            return {
                "name": player_name,
                "seasons_included": len(player_stats),
                "total_games": total_games,
                "total_goals": total_goals,
                "total_assists": total_assists,
                "total_points": total_points,
                "total_shots": total_shots,
                "points_per_game": round(total_points / total_games, 2) if total_games > 0 else 0,
                "goals_per_game": round(total_goals / total_games, 2) if total_games > 0 else 0,
                "assists_per_game": round(total_assists / total_games, 2) if total_games > 0 else 0,
                "shooting_percentage": round((total_goals / total_shots) * 100, 1) if total_shots > 0 else 0,
                "avg_toi_per_game": round(total_toi / total_games, 2) if total_games > 0 else 0,
                "avg_scouting_grade": round(avg_scouting_grade, 1)
            }

        player1_summary = calculate_player_stats(player1_stats, player1)
        player2_summary = calculate_player_stats(player2_stats, player2)

        comparisons = {
            "total_points": {
                "winner": player1 if player1_summary["total_points"] > player2_summary["total_points"] else player2,
                "values": {player1: player1_summary["total_points"], player2: player2_summary["total_points"]}
            },
            "points_per_game": {
                "winner": player1 if player1_summary["points_per_game"] > player2_summary["points_per_game"] else player2,
                "values": {player1: player1_summary["points_per_game"], player2: player2_summary["points_per_game"]}
            },
            "shooting_percentage": {
                "winner": player1 if player1_summary["shooting_percentage"] > player2_summary["shooting_percentage"] else player2,
                "values": {player1: player1_summary["shooting_percentage"], player2: player2_summary["shooting_percentage"]}
            },
            "avg_scouting_grade": {
                "winner": player1 if player1_summary["avg_scouting_grade"] > player2_summary["avg_scouting_grade"] else player2,
                "values": {player1: player1_summary["avg_scouting_grade"], player2: player2_summary["avg_scouting_grade"]}
            }
        }

        wins = {player1: 0, player2: 0}
        for comparison in comparisons.values():
            wins[comparison["winner"]] += 1

        overall_winner = player1 if wins[player1] > wins[player2] else player2 if wins[player2] > wins[player1] else "tie"

        return {
            "player1": player1_summary,
            "player2": player2_summary,
            "comparisons": comparisons,
            "overall_winner": overall_winner,
            "win_count": wins,
            "season_filter": season
        }

