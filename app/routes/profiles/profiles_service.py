from app.dto.profiles import ProfileDto
from app.dto.assignation import AssignDto

from app.common.db_connectors.neo4j_conn import Neo4jConnector
from typing import Dict


async def getProfileService():
    try:
        connector = Neo4jConnector()
        response = connector.get_all_nodes('User')
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def findProfileService(user_id: str):
    try:
        connector = Neo4jConnector()
        response = connector.get_node('User', 'user_id', user_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def addProfileService(req: ProfileDto):
    try:
        connector = Neo4jConnector()
        connector.create_node('User', req.dict())
        return {"inserted_id": req.dict()}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def updateProfileService(req: ProfileDto):
    try:
        connector = Neo4jConnector()
        properties = req.dict()
        value = properties['user_id']
        connector.update_node('User','user_id',value, properties)
        return {"updated": value, "properties": properties}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
    
async def addProfileSkillService(req: AssignDto, user_id):
    try:
        connector = Neo4jConnector()
        params = req.dict()
        end_node = params['related_to']
        relationship = 'HAS_SKILL'
        connector.create_relationship('User', 'user_id', user_id, relationship,'Skill', 'skill_id', end_node)
        return {"assignation": f'User {user_id} -- {relationship} --> {end_node}'}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def getProfileSkillsService(user_id):
    try:
        connector = Neo4jConnector()
        response = connector.get_nodes_with_direct_relationship('Skill', 'HAS_SKILL', 'User','user_id', user_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}