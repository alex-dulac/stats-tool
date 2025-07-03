from fastapi import APIRouter, Depends

from app.models import stat_to_extended_model
from app.service import StatsService

router = APIRouter()

@router.get('/')
async def health():
    return {"status": "ok"}

@router.get('/stats')
async def stats(stats_service: StatsService = Depends()):
    response = []
    data = await stats_service.get_stats()

    for s in data:
        extended = await stat_to_extended_model(s)
        response.append(extended)

    return {"data": response}

@router.get('/players')
async def stats(stats_service: StatsService = Depends()):
    data = await stats_service.get_players()
    return {"data": data}

@router.get('/stats/{player_name}')
async def stats(player_name: str, stats_service: StatsService = Depends()):
    response = []
    data = await stats_service.get_stats_by_player_name(player_name)

    for s in data:
        extended = await stat_to_extended_model(s)
        response.append(extended)

    return {"data": response}

@router.get('/charts/total-points')
async def total_points_chart(season: int = None, stats_service: StatsService = Depends()):
    data = await stats_service.get_goals_assists_chart_data(season)
    return {"data": data}

@router.get('/charts/production')
async def production_chart(season: int = None, stats_service: StatsService = Depends()):
    data = await stats_service.get_production_chart_data(season)
    return {"data": data}

@router.get('/charts/shooting-efficiency')
async def shooting_efficiency(season: int = None, stats_service: StatsService = Depends()):
    data = await stats_service.get_shooting_efficiency_chart_data(season)
    return {"data": data}

@router.get('/charts/per-game-consistency')
async def shooting_efficiency(season: int = None, stats_service: StatsService = Depends()):
    data = await stats_service.get_per_game_consistency_chart_data(season)
    return {"data": data}

@router.get('/charts/scouting-heatmap')
async def scouting_heatmap(stats_service: StatsService = Depends()):
    data = await stats_service.get_scouting_heatmap_chart_data()
    return {"data": data}