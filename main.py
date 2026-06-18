from fastapi import FastAPI
import uvicorn

from database.db_connection import DB_connection
from routes import agent_routes
from routes import mission_routes
from routes import report_routes

connection = DB_connection()
app = FastAPI()

app.include_router(agent_routes.router, prefix="/agents")
app.include_router(mission_routes.router, prefix="/missions")
app.include_router(report_routes.router, prefix="/reports")

if __name__ == "__main__":
    connection.create_database()
    connection.create_tables()
    uvicorn.run("main:app", port=8000, reload=True)