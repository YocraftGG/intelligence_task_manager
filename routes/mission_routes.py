from fastapi import APIRouter, HTTPException

from database.mission_db import MissionDB
from database.agent_db import AgentDB
from logs.setup_logger import logger

mission_db = MissionDB()
agent_db = AgentDB()
router = APIRouter()


def validate(condition, status, message, *args):
    if condition:
        logger.error(message, *args)
        raise HTTPException(status_code=status, detail=message)
    

def validate_assignment(m_id: int, a_id: int):
    mission = mission_db.get_mission_by_id(m_id)
    agent = agent_db.get_agent_by_id(a_id)

    validate(mission is None, 404, "Mission not found", m_id)
    validate(agent is None, 404, "Agent not found", a_id)
    validate(mission["status"] != "NEW", 400, "Mission not available")
    validate(not agent["is_active"], 400, "Agent is not active")
    validate(len(mission_db.get_open_missions_by_agent(a_id)) >= 3, 
             400, "Agent has reached maximum missions")
    validate(mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander", 
             400, "Only Commander can handle critical missions")


@router.post("", status_code=201)
def create_mission(body: dict):
    logger.info("POST /missions called")
    for field in ("title", "description", "location", "difficulty", "importance"):
        validate(field not in body, 400, f"Field '{field}' is required")

    for field in ("difficulty", "importance"):
        validate(body[field] < 1 or 10 < body[field], 400, f"'{field}' must be between 1 and 10")

    logger.info("Creating mission")
    mission = mission_db.create_mission(body)
    logger.info("Mission created successfully: id=%s", mission["id"])
    return mission


@router.get("")
def get_all_missions():
    logger.info("GET /missions called")
    logger.info("Getting mission")
    missions = mission_db.get_all_missions()
    logger.info("Got mission successfully")
    return missions


@router.get("/{id}")
def get_mission(id: int):
    logger.info("POST /missions/{id} called")
    logger.info("Getting mission with id %s", id)
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found", id)
    logger.info("Got mission with id %s successfully", id)
    return mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission(m_id: int, a_id: int):
    logger.info("PUT /missions/{id} called")
    validate_assignment(m_id, a_id)
    
    logger.info("Assigning mission")
    changed = mission_db.assign_mission(m_id, a_id)
    logger.info("Assigned mission with id %s to agent with id %s successfully", m_id, a_id)
    return {
            "message": "Mission assigned successfully",
            "changed": changed
        }

@router.put("/{id}/start")
def start_mission(id: int):
    logger.info("PUT /missions/{id}/start called")
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "ASSIGNED", 
             400, "Mission's status is not 'ASSIGNED'")
    
    logger.info("Starting mission")
    changed = mission_db.update_mission_status(id, "IN_PROGRESS")
    logger.info("Mission with id %s started successfully", id)
    return {
            "message": "Mission updated to 'IN_PROGRESS' successfully",
            "changed": changed
        }

@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info("PUT /missions/{id}/complete called")
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "IN_PROGRESS", 
             400, "Mission's status is not 'IN_PROGRESS'")
    
    logger.info("Completing mission")
    changed = mission_db.update_mission_status(id, "COMPLETED")
    logger.info("Mission with id %s completed successfully", id)
    return {
            "message": "Mission updated to 'COMPLETED' successfully",
            "changed": changed
        }

@router.put("/{id}/fail")
def fail_mission(id: int):
    logger.info("PUT /missions/{id}/fail called")
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "IN_PROGRESS", 
             400, "Mission's status is not 'IN_PROGRESS'")
    
    logger.info("failing mission")
    changed = mission_db.update_mission_status(id, "FAILED")
    logger.info("Mission with id %s failed successfully", id)
    return {
            "message": "Mission updated to 'FAILED' successfully",
            "changed": changed
        }

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    logger.info("PUT /missions/{id}/cancel called")
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] not in ("NEW ", "ASSIGNED"), 
             400, "Mission's status is not 'NEW' or 'ASSIGNED'")
    
    logger.info("Cancelling mission")
    changed = mission_db.update_mission_status(id, "CANCELLED")
    logger.info("Mission with id %s cancelled successfully", id)
    return {
            "message": "Mission updated to 'CANCELLED' successfully",
            "changed": changed
        }