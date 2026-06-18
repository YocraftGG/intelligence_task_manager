from fastapi import APIRouter, HTTPException
import mysql.connector

from database.agent_db import AgentDB
from logs.setup_logger import logger

agent_db = AgentDB()
router = APIRouter()

def validate(field, body):
    if field not in body:
        logger.error("User did not enter %s", field)
        raise HTTPException(status_code=400, detail=f"Field '{field}' is required")

@router.post("", status_code=201)
def create_agent(body: dict):
    logger.info("POST /agents called")
    for field in ("name", "specialty", "agent_rank"):
        validate(field, body)

    try:
        logger.info("Creating agent")
        agent = agent_db.create_agent(body)
        logger.info("Agent created successfully: id=%s", agent["id"])
        return agent
    except mysql.connector.errors.Error:
        logger.error("User entered rank that is not Junior / Senior / Commander")
        raise HTTPException(status_code=400, detail="Rank must be Junior / Senior / Commander")
    

@router.get("")
def get_all_agent():
    logger.info("GET /agents called")
    logger.info("Getting agents")
    agents = agent_db.get_all_agents()
    logger.info("Got agents successfully")
    return agents


@router.get("/{id}")
def get_agent(id: int):
    logger.info("GET /agents/{id} called")
    logger.info("Getting agent with id %s", id)
    agent = agent_db.get_agent_by_id(id)
    if agent is None:
        logger.error("Agent not found: %s", id)
        raise HTTPException(status_code=404, detail="Agent not found")
    logger.info("Got agent with id %s successfully", id)
    return agent


@router.put("/{id}")
def update_agent(id: int, body: dict):
    logger.info("PUT /agents/{id} called")
    if agent_db.get_agent_by_id(id) is None:
        logger.error("Agent not found: %s", id)
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        logger.info("Updating agent with id %s", id)
        changed = agent_db.update_agent(id, body)
        logger.info("Agent Updated successfully: id=%s", id)
        return {
            "message": "Agent updated successfully",
            "changed": changed
        }
    except mysql.connector.errors.Error:
        logger.error("User entered rank that is not Junior / Senior / Commander")
        raise HTTPException(status_code=400, detail="Rank must be Junior / Senior / Commander")
    

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    logger.info("PUT /agents/{id}/deactivate called")
    if agent_db.get_agent_by_id(id) is None:
        logger.error("Agent not found: %s", id)
        raise HTTPException(status_code=404, detail="Agent not found")
    
    logger.info("Deactivating agent with id %s", id)
    changed = agent_db.deactivate_agent(id)
    logger.info("Agent deactivated successfully: id=%s", id)
    return {
        "message": "Agent deactivated successfully",
        "changed": changed
    }


@router.get("/{id}/performance")
def get_agent(id: int):
    logger.info("GET /agents/{id}/performance")
    if agent_db.get_agent_by_id(id) is None:
        logger.error("Agent not found: %s", id)
        raise HTTPException(status_code=404, detail="Agent not found")
    logger.info("Getting performance of agent with id %s", id)
    performance = agent_db.get_agent_performance(id)
    logger.info("Got performance of agent with id %s successfully", id)
    return performance