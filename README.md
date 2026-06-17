# Intelligence Task Manager

An intelligence unit called ShadowNet needs a system to manage agents and tasks. The goal of the project: to create a system to manage the database using OOP and MySQL tables.

## File structure
intelligence-task-manager/  
├── atabase/  
│ ├── db_connection.py  
│ ├── agent_db.py  
│ └── mission_db.py  
├── README.md  
├── requirements.txt  
└── .gitignore  

## Table structure
### agents
Field | Type | Notes
--- | --- | ---
id | INT, AUTO_INCREMENT, PK | Unique identifier
name | VARCHAR | Agent name
specialty | VARCHAR | Specialty
is_active | BOOLEAN | Default: TRUE
completed_missions | INT | Default: 0
failed_missions | INT | Default: 0
agent_rank | ENUM | Junior / Senior / Commander only

### missions
Field | Type | Notes
--- | --- | ---
id | INT, AUTO_INCREMENT, PK | Unique identifier
title | VARCHAR | Mission title
description | TEXT | Detailed description
location | VARCHAR | Location
difficulty | INT | 1-0 only
importance | INT | 1-0 only
status | VARCHAR | Default: NEW
risk_level | VARCHAR | Automatically calculated — not provided by user
assigned_agent_id | INT | NULL until assigned

## Classes
### DB_connection
Responsible for creating and connecting to the database.
Method | Role
--- | ---
get_connection() | Returns an active MySQL connection
create_database() | Creates Intelligence_db if it does not exist
create_tables() | Creates both tables if they do not exist

### AgentDB
Responsible for all SQL operations against the agents table.
Method | Role
--- | ---
create_agent(data) | Creates a new agent and returns the agent object
get_all_agents() | Returns a list of all agents
get_agent_by_id(id) | Returns one agent by ID, or None
update_agent(id, data) | UPDATE to the entire row (id cannot be changed)
deactivate_agent(id) | Sets agent status to inactive
increment_completed(id) | Updates the number of completed tasks
increment_failed(id) | Updates the number of failed tasks
get_agent_performance(id) | Returns a dictionary with these keys completed, failed, total, success_rate
count_active_agents() | Returns the number of active agents

### MissionDB
Responsible for all SQL operations against the missions table.
Method | Role
--- | ---
create_mission(data) | Create a new mission and return the entire object
get_all_missions() | Returns all missions
get_mission_by_id(id) | Returns a single mission by ID, or None
assign_mission(m_id, a_id) | Assigns a mission to an agent
update_mission_status(id, status) | Used for any status change
get_open_missions_by_agent(id) | Returns ASSIGNED/IN_PROGRESS missions of an agent
count_all_missions() | Total missions
count_by_status(status) | Counts by a specific status
count_open_missions() | Counts open missions
count_critical_missions() | Counts CRITICAL missions
get_top_agent() | The agent with the highest completed_missions

## System rule
Responsible for all SQL operations against the missions table.
Number | Rule
--- | ---
1 | rank must be Junior / Senior / Commander — any other value throws an error.
2 | difficulty and importance must be between 1 and 10 — otherwise an error.
3 | risk_level is calculated automatically when creating a mission — the user does not submit it.
4 | An agent with is_active=False cannot accept missions.
5 | An agent cannot have more than 3 open missions (ASSIGNED / IN_PROGRESS) at the same time.
6 | If risk_level=CRITICAL — only an agent with the Commander rank can accept the mission.
7 | Only a mission can be assigned In status NEW. After assignment: status=ASSIGNED.
8 | Only a task can be started in status ASSIGNED. After: status=IN_PROGRESS.
9 | Only a task can be finished. IN_PROGRESS and changed to status failed or completed
10 | Only a task can be canceled in status NEW or ASSIGNED — otherwise an error.

## Run instructions
### Running Docker
```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
-e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

```