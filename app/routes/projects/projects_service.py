from app.dto.projects import ProjectDto
from app.dto.assignation import AssignDto

from app.common.db_connectors.neo4j_conn import Neo4jConnector
from typing import Dict

async def findProjectService(project_id: str):
    try:
        connector = Neo4jConnector()
        response = connector.get_node('Project', 'project_id', project_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def deleteProjectService(project_id: str):
    try:
        connector = Neo4jConnector()
        response = connector.delete_node('Project', 'project_id', project_id)
        print(f"Response from Neo4j: {response}")
        if response:
            return {"success": f"Project {project_id} deleted successfully."}
        else:
            return {"error": f"Project {project_id} could not be deleted."}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def getProjectService():
    try:
        connector = Neo4jConnector()
        response = connector.get_all_nodes('Project')
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def getProjectColabService(project_id: str):
    try:
        connector = Neo4jConnector()
        response = connector.get_nodes_with_indirect_relationship('User', 'TASK_ASSIGNED_TO', 'Task', 'PROJECT_HAS_TASK', 'Project','project_id', project_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def getProjectTasksService(project_id):
    try:
        connector = Neo4jConnector()
        response = connector.get_nodes_with_direct_relationship('Task', 'PROJECT_HAS_TASK', 'Project','project_id', project_id)
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def getCandidateTasksService():
    try:
        connector = Neo4jConnector()
        response = connector.get_nodes_without_relationship('Task', 'PROJECT_HAS_TASK')
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
async def addProjectService(req: ProjectDto):
    try:
        connector = Neo4jConnector()
        connector.create_node('Project', req.dict())
        #TO DO: crear la relacion OWNS con el user que ejecuto la creacion del proyecto
        return {"inserted_id": req.dict()}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}

async def updateProjectService(req: ProjectDto):
    try:
        connector = Neo4jConnector()
        properties = req.dict()
        value = properties['project_id']
        connector.update_node('Project','project_id',value, properties)
        return {"updated": value, "properties": properties}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}
    
    
async def addProjectTaskService(req: AssignDto, project_id):
    try:
        connector = Neo4jConnector()
        params = req.dict()
        end_node = params['related_to']
        relationship = 'PROJECT_HAS_TASK'
        connector.create_relationship('Project', 'project_id', project_id, relationship,'Task', 'task_id', end_node)
        return {"assignation": f'Project {project_id} -- {relationship} -- {end_node}'}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error, please try again later."}