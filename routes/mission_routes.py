from fastapi import APIRouter, HTTPException

from database.mission_db import MissionDB
from database.agent_db import AgentDB

mission_db = MissionDB()
agent_db = AgentDB()
router = APIRouter()


def validate(condition, status, message):
    if condition:
        raise HTTPException(status_code=status, detail=message)
    

def validate_assignment(m_id: int, a_id: int):
    mission = mission_db.get_mission_by_id(m_id)
    agent = agent_db.get_agent_by_id(a_id)

    validate(mission is None, 404, "Mission not found")
    validate(agent is None, 404, "Agent not found")
    validate(mission["status"] != "NEW", 400, "Mission not available")
    validate(not agent["is_active"], 400, "Agent is not active")
    validate(len(mission_db.get_open_missions_by_agent(a_id)) >= 3, 
             400, "Agent has reached maximum missions")
    validate(mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander", 
             400, "Only Commander can handle critical missions")



@router.post("", status_code=201)
def create_mission(body: dict):
    for field in ("title", "description", "location", "difficulty", "importance"):
        validate(field not in body, 400, f"Field '{field}' is required")

    for field in ("difficulty", "importance"):
        validate(body[field] < 1 or 10 < body[field], 404, f"'{field}' must be between 1 and 10")

    mission = mission_db.create_mission(body)
    return mission


@router.get("")
def get_all_missions():
    missions = mission_db.get_all_missions()
    return missions


@router.get("/{id}")
def get_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    return mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission(m_id: int, a_id: int):
    validate_assignment(m_id, a_id)
    
    changed = mission_db.assign_mission(m_id, a_id)
    return {
            "message": "Mission assigned successfully",
            "changed": changed
        }

@router.put("/{id}/start")
def start_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "ASSIGNED", 
             400, "Mission's status is not 'ASSIGNED'")
    
    changed = mission_db.update_mission_status(id, "IN_PROGRESS")
    return {
            "message": "Mission updated to 'IN_PROGRESS' successfully",
            "changed": changed
        }

@router.put("/{id}/complete")
def complete_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "IN_PROGRESS", 
             400, "Mission's status is not 'IN_PROGRESS'")
    
    changed = mission_db.update_mission_status(id, "COMPLETED")
    return {
            "message": "Mission updated to 'COMPLETED' successfully",
            "changed": changed
        }

@router.put("/{id}/fail")
def fail_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] != "IN_PROGRESS", 
             400, "Mission's status is not 'IN_PROGRESS'")
    
    changed = mission_db.update_mission_status(id, "FAILED")
    return {
            "message": "Mission updated to 'FAILED' successfully",
            "changed": changed
        }

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    validate(mission is None, 404, "Mission not found")
    validate(mission["status"] not in ("NEW ", "ASSIGNED"), 
             400, "Mission's status is not 'NEW' or 'ASSIGNED'")
    
    changed = mission_db.update_mission_status(id, "CANCELLED")
    return {
            "message": "Mission updated to 'CANCELLED' successfully",
            "changed": changed
        }