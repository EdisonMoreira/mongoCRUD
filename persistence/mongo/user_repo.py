from persistence.repository import UserRepository
from domain.user import User
from persistence.mongo.client import get_user_collection
from uuid import UUID

class MongoUserRepository(UserRepository):

    def __init__(self):
        self.collection = get_user_collection()

    async def list(self) -> list[User]:
        users: list[User] = []

        async for doc in self.collection.find():

            # 1. Converter o ID (que está como string no banco) para UUID
            doc["id"] = UUID(doc["id"])
            
            # 2. Remover o "_id" interno do MongoDB para não dar erro no Pydantic
            # (pois o seu modelo User não tem campo _id, tem id)
            if "_id" in doc:
                del doc["_id"]

            # 3. Usar **doc para passar TUDO o que veio do banco para o User
            # O Pydantic vai preencher os campos conhecidos e guardar o resto nos extras
            users.append(User(**doc))
        return users

    async def create(self, user: User) -> None:

        # É NESTA LINHA EXATA que o Banco e a Collection são criados

        await self.collection.insert_one({
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "released": user.released,
            "year": user.year
        })

