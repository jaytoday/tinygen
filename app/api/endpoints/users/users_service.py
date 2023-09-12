from pydantic import BaseModel
from supabase_py import create_client, Client
from app.config import settings
from app.entities.user import User

supabase: Client = create_client(settings.get_db_url(), settings.SUPABASE_KEY)

class UsersService:
    class GetUsersRes(BaseModel):
        users: list[User]

    async def get_users(self) -> GetUsersRes:
        res = await supabase.from_("users").select("*").eq("is_deleted", 0)
        orm_users = res.data

        users: list[User] = []
        for orm_user in orm_users:
            users.append(User.model_validate(orm_user))

        return self.GetUsersRes(users=users)
