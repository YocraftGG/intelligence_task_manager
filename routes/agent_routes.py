from fastapi import APIRouter, HTTPException
import mysql.connector

from database.agent_db import AgentDB

agent_db = AgentDB()
router = APIRouter()

def validate(field, body):
    if field not in body:
        raise HTTPException(status_code=400, detail=f"Field '{field}' is required")

@router.post("", status_code=201)
def create_agent(body: dict):
    for field in ("name", "specialty", "agent_rank"):
        validate(field, body)

    try:
        agent = agent_db.create_agent(body)
        return agent
    except mysql.connector.errors.Error:
        raise HTTPException(status_code=400, detail="Rank must be Junior / Senior / Commander")
    

@router.get("")
def get_all_agent():
    agents = agent_db.get_all_agents()
    return agents


@router.get("/{id}")
def get_agent(id: int):
    agent = agent_db.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{id}")
def update_agent(id: int, body: dict):
    if agent_db.get_agent_by_id(id) is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        changed = agent_db.update_agent(id, body)
        return {
            "message": "Agent updated successfully",
            "changed": changed
        }
    except mysql.connector.errors.Error:
        raise HTTPException(status_code=400, detail="Rank must be Junior / Senior / Commander")
    

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    if agent_db.get_agent_by_id(id) is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    changed = agent_db.deactivate_agent(id)
    return {
        "message": "Agent deactivated successfully",
        "changed": changed
    }


@router.get("/{id}/performance")
def get_agent(id: int):
    if agent_db.get_agent_by_id(id) is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    performance = agent_db.get_agent_performance(id)
    return performance