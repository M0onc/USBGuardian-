from sqlalchemy.ext.asyncio import AsyncSession
from ..models.policy import PolicyTable
from ..database import get_db

class PolicyManager:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_policy(self, policy_data):
        policy = PolicyTable(
            name=policy_data.name,
            rules=policy_data.rules,
            action=policy_data.action,
            target_groups=policy_data.target_groups
        )
        self.db.add(policy)
        await self.db.commit()
        await self._sync_to_agents(policy)  # 同步到边缘节点
        return {"id": policy.id, "status": "deployed"}

    async def _sync_to_agents(self, policy):
        # 通过Redis发布策略更新
        import redis
        r = redis.Redis(host='redis')
        r.publish("policy_updates", policy.json())