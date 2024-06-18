from app.dto.skills import SkillDto
from app.dto.assignation import AssignDto

from app.common.db_connectors.neo4j_conn import Neo4jConnector
from typing import Dict


async def getSkillsService():
    try:
        connector = Neo4jConnector()
        response = connector.get_all_nodes('Skill')
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def addSkillService(req: SkillDto):
    try:
        connector = Neo4jConnector()
        connector.create_node('Skill', req.dict())
        return {"inserted_id": req.dict()}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def updateSkillService(req: SkillDto):
    try:
        connector = Neo4jConnector()
        properties = req.dict()
        value = properties['skill_id']
        connector.update_node('Skill','skill_id',value, properties)
        return {"updated": value, "properties": properties}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
