from fastapi import APIRouter

from database.mission_db import MissionDB
from database.agent_db import AgentDB
from logs.setup_logger import logger

mission_db = MissionDB()
agent_db = AgentDB()
router = APIRouter()


@router.get("/summary")
def get_summary():
    logger.info("POST /reports/summary called")
    logger.info("Getting summary")
    summary = {
        "active_agents_count": agent_db.count_active_agents(),   
        "total_missions": mission_db.count_all_missions(),   
        "open_missions": mission_db.count_open_missions(),  
        "completed_missions": mission_db.count_by_status("COMPLETED"),
        "failed_missions": mission_db.count_by_status("FAILED"),   
        "critical_missions": mission_db.count_critical_missions()
    }
    logger.info("Got missions by status successfully")
    return summary


@router.get("/missions-by-status")
def get_missions_by_status():
    logger.info("POST /reports/missions-by-status called")
    logger.info("Getting missions by status")
    missions_by_status = {
        "new": mission_db.count_by_status("NEW"),
        "assigned": mission_db.count_by_status("ASSIGNED"),
        "in_progress": mission_db.count_by_status("IN_PROGRESS"),
        "completed": mission_db.count_by_status("COMPLETED"),
        "failed": mission_db.count_by_status("FAILED"), 
        "cancelled": mission_db.count_by_status("CANCELLED"), 
    }
    logger.info("Got missions by status successfully")
    return missions_by_status


@router.get("/top-agent")
def get_top_agent():
    logger.info("POST /reports/top-agent called")
    logger.info("Getting top agent")
    top_agent = mission_db.get_top_agent()
    logger.info("Got top agent successfully")
    return top_agent