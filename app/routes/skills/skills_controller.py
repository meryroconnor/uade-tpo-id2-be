from fastapi import APIRouter, Depends, HTTPException, Query, Body
#from app.common.auth.auth_bearer import JWTBearer
from app.dto.assignation import AssignDto
from app.dto.skills import SkillDto

from typing import Optional, Dict
from app.routes.skills.skills_service import addSkillService, getSkillsService, updateSkillService

router = APIRouter()
entity = "skills"

@router.get("/", tags=[entity])
async def getSkills():
    result = await getSkillsService()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
        
@router.put("/", tags=[entity])
async def updateSkill(req: SkillDto):
    result = await updateSkillService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", tags=[entity])
async def addSkill(req: SkillDto):
    result = await addSkillService(req)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


