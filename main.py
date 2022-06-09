from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException, status
from models import Gender, Role, UpdateUser, User


app = FastAPI()

db: List[User] = [
    User(
        id=UUID("aceb061f-d432-40cf-b46f-843067538319"),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("03067250-3253-4ae8-91a4-97b0e3f338fb"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]

@app.get("/", tags=["Root"], status_code=status.HTTP_200_OK)
async def root():
    return {"Hello": "Mundo"}

@app.get("/api/v1/users", tags=["User"], status_code=status.HTTP_200_OK)
async def get_users():
    return {"count": len(db), "data": db}

@app.post("/api/v1/users", tags=["User"], status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    for db_user in db:
        if db_user.id == user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with ID {user.id} already exists.")
    db.append(user)
    return {"data": user, "msg": "User created successfully."}

@app.delete("/api/v1/users/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def delete_user(user_id: UUID):
    for db_user in db:
        if user_id == db_user.id:
            db.remove(db_user)
            return {"data": {}, "msg": "User deleted successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} was not found.")

@app.put("/api/v1/users/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def update_user(user_id: UUID, user_data: UpdateUser):
    for db_user in db:
        if db_user.id == user_id:
            db_user.first_name = user_data.first_name if user_data.first_name else db_user.first_name
            db_user.last_name = user_data.last_name if user_data.last_name else db_user.last_name
            db_user.middle_name = user_data.middle_name if user_data.middle_name else db_user.middle_name
            db_user.roles = user_data.roles if user_data.roles else db_user.roles
            return {"data": db_user, "msg": f"User with ID {user_id} updated successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} was not found.")

