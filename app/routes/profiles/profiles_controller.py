from fastapi import APIRouter, Depends, HTTPException, Query, Body
#from app.common.auth.auth_bearer import JWTBearer
from app.dto.assignation import AssignDto
from app.dto.profiles import ProfileDto

from typing import Optional, Dict
from app.routes.profiles.profiles_service import findProfileService, addProfileService, getProfileService, updateProfileService, addProfileSkillService

router = APIRouter()
entity = "profiles"

@router.get("/", tags=[entity])
async def getProfile():
    result = await getProfileService()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
        
@router.put("/", tags=[entity])
async def updateProject(req: ProfileDto):
    result = await updateProfileService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", tags=[entity])
async def addProfile(req: ProfileDto):
    result = await addProfileService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{user_id}", tags=[entity])
async def findProfile(user_id: str):
    result = await findProfileService(user_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/{user_id}/skills", tags=[entity])
async def addProfileSkill(req: AssignDto, user_id):
    result = await addProfileSkillService(req, user_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
