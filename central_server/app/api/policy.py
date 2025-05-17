from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List
from ..services.policy_manager import PolicyManager
from ..security.auth import validate_scope

router = APIRouter()
security = HTTPBearer()

# 策略数据模型
class PolicyCreate(BaseModel):
    name: str
    rules: List[str]
    action: str = "block"
    target_groups: List[str]

@router.post("/policies", dependencies=[Security(security, scopes=["policy:write"])])
async def create_policy(policy: PolicyCreate, 
                      pm: PolicyManager = Depends(PolicyManager)):
    """创建并下发安全策略"""
    return await pm.create_policy(policy)

@router.get("/devices/risk-summary")
async def get_risk_summary(pm: PolicyManager = Depends(PolicyManager)):
    """获取全网风险概览"""
    return {
        "high_risk": await pm.count_devices_by_risk("high"),
        "devices_total": await pm.get_total_devices()
    }