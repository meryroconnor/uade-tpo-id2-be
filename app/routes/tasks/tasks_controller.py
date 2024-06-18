from fastapi import APIRouter, Depends, HTTPException, Query, Body
# from app.common.auth.auth_bearer import JWTBearer
from app.dto.tasks import TasksDto
from app.dto.assignation import AssignDto
from typing import Optional, Dict
from app.routes.tasks.tasks_service import addTaskService, getTasksService, updateTaskService, addTaskAssignationService, getTaskResponsibleService, getTaskCandidatesService

router = APIRouter()
entity = "tasks"

@router.get("/", tags=[entity])
async def getTasks():
    result = await getTasksService()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/reponsible", tags=[entity])
async def getTaskResponsible(task_id: str = Query(...)):
    query_params = {}
    query_params["task_id"] = task_id
    
    result = await getTaskResponsibleService(query_params)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/candidates", tags=[entity])
async def getTaskCandidates(required_availability: int = Query(...), skill_id: str = Query(...)):
    query_params = {}
    query_params["availability"] = required_availability
    query_params["skill_id"] = skill_id
    
    result = await getTaskCandidatesService(query_params)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", tags=[entity])
async def addActivity(req: TasksDto):
    result = await addTaskService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.put("/", tags=[entity])
async def updateActivity(req: TasksDto):
    result = await updateTaskService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/assign", tags=[entity])
async def addTaskAssignation(req: AssignDto):
    result = await addTaskAssignationService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result