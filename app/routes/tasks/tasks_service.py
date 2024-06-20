from app.dto.tasks import TasksDto
from app.dto.assignation import AssignDto

from app.common.db_connectors.neo4j_conn import Neo4jConnector
from typing import Dict

async def getTasksService():
    try:
        connector = Neo4jConnector()
        response = connector.get_all_nodes('Task')
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def findTaskService(task_id: str):
    try:
        connector = Neo4jConnector()
        response = connector.get_node('Task', 'task_id', task_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def getTaskResponsibleService(task_id):
    try:
        connector = Neo4jConnector()
        response = connector.get_nodes_with_direct_relationship('User', 'TASK_ASSIGNED_TO', 'Task','task_id', task_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def getTaskCandidatesService(query_params: Dict):
    try:
        connector = Neo4jConnector()
        availability = query_params['availability']
        skill_id = query_params['skill_id']
        response = connector.get_nodes_with_property_greater_than_and_relationship('User', 'availability',availability, 'HAS_SKILL', 'Skill','skill_id', skill_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def addTaskService(req: TasksDto):
    try:
        connector = Neo4jConnector()
        connector.create_node('Task', req.dict())
        return {"inserted_id": req.dict()}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def updateTaskService(req: TasksDto):
    try:
        connector = Neo4jConnector()
        properties = req.dict()
        value = properties['task_id']
        connector.update_node('Task','task_id',value, properties)
        return {"updated": value, "properties": properties}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def addTaskAssignationService(req: AssignDto, task_id):
    try:
        connector = Neo4jConnector()
        params = req.dict()
        end_node = params['related_to']
        relationship = 'TASK_ASSIGNED_TO'
        
        # Create Relationship
        connector.create_relationship('Task', 'task_id', task_id, relationship, 'User', 'user_id', end_node)
        
        # Retrieve the user's current availability and the task duration
        user_node = connector.get_node('User', 'user_id', end_node)['n']
        task_node = connector.get_node('Task', 'task_id', task_id)['n']
        user_availability = user_node['availability']
        task_duration = task_node['duration']
        
        # Calculate the new availability
        new_availability = user_availability - task_duration
        
        # Update the user's availability
        connector.update_node('User', 'user_id', end_node, {'availability': new_availability})
        
        return {"assignation": f'User {end_node} -- {relationship} -- {task_id}'}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
