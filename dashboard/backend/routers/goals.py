# dashboard/backend/routers/goals.py
from fastapi import APIRouter, HTTPException
from models import Goal, StrategyUpdate

router = APIRouter()

mock_goals = [
    Goal(agent_id="agent_001", agent_name="MarketingBot", description="Grow Twitter by 30%", deadline="2025-06-01", progress=60),
    Goal(agent_id="agent_002", agent_name="DevOpsBot", description="Deploy 5 modules", deadline="2025-05-15", progress=80),
]

agent_strategies = {
    "agent_001": "exploratory",
    "agent_002": "conservative",
}

@router.get("/goals")
def get_goals():
    return mock_goals

@router.get("/strategies")
def get_strategies():
    return agent_strategies

@router.put("/strategies/{agent_id}")
def update_strategy(agent_id: str, update: StrategyUpdate):
    if agent_id not in [g.agent_id for g in mock_goals]:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent_strategies[agent_id] = update.strategy
    return {"status": "updated", "agent_id": agent_id}
