from fastapi import APIRouter, Depends, HTTPException, Query, Body
#from app.common.auth.auth_bearer import JWTBearer
from app.dto.assignation import AssignDto
from app.dto.projects import ProjectDto

from typing import Optional, Dict
from app.routes.projects.projects_service import addProjectService, getProjectService, updateProjectService, addProjectTaskService, getProjectColabService, getProjectTasksService,getCandidateTasksService

router = APIRouter()
entity = "projects"

@router.get("/", tags=[entity])
async def getProjects():
    result = await getProjectService()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/collaborators", tags=[entity])
async def getProjectColaborators(project_id: str = Query(...)):
    query_params = {}
    query_params["project_id"] = project_id
    
    result = await getProjectColabService(query_params)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/candidatesTasks", tags=[entity])
async def getTaskCandidates():    
    result = await getCandidateTasksService()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/tasks", tags=[entity])
async def getProjectTasks(project_id: str = Query(...)):
    query_params = {}
    query_params["project_id"] = project_id
    
    result = await getProjectTasksService(query_params)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
        
@router.put("/", tags=[entity])
async def updateProject(req: ProjectDto):
    result = await updateProjectService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", tags=[entity])
async def addProject(req: ProjectDto):
    result = await addProjectService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/assign", tags=[entity])
async def addProjectTask(req: AssignDto):
    result = await addProjectTaskService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
