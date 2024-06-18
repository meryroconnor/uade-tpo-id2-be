from fastapi import APIRouter, Depends, HTTPException, Query, Body
# from app.common.auth.auth_bearer import JWTBearer
from typing import Optional, Dict
from app.dto.activities import ActivitiesDto
from app.routes.activities.activities_service import getActivitiesService, addActivityService, addLikeService,updateActivityService, findActivityService


router = APIRouter()
entity = "activities"

@router.get("/", tags=[entity])
async def getActivities(user_id: Optional[int] = Query(None), task_id: Optional[str] = Query(None), project_id: Optional[str] = Query(None)):
    query_params = {}
    if user_id is not None:
        query_params["user_id"] = user_id
    if task_id is not None:
        query_params["task_id"] = task_id
    if project_id is not None:
        query_params["project_id"] = project_id
        
    result = await getActivitiesService(query_params)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", tags=[entity])
async def addActivity(req: ActivitiesDto):
    result = await addActivityService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/{activity_id}/like", tags=[entity])
async def addLike(activity_id: str, user_id: str):
    result = await addLikeService(activity_id, user_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.put("/{activity_id}", tags=[entity])
async def updateActivity(activity_id: str, activity_data: dict = Body(...)):
    result = await updateActivityService(activity_id, activity_data)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{activity_id}", tags=[entity])
async def findActivity(activity_id: str):
    result = await findActivityService(activity_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
