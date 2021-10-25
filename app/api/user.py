from typing import List

from fastapi import HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.crud.user import db as user_db
from app.schema.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_description="Add new user", response_model=User)
async def create_user(user: User):
    user = jsonable_encoder(user)
    new_user = await user_db.insert_user(user)
    created_user = await user_db.find_one_inserted(new_user)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=created_user)


@router.get("/",
            response_description="List all users",
            response_model=List[User])
async def list_users():
    return await user_db.find_users()


@router.get("/{user_id}",
            response_description="Get a single user",
            response_model=User)
async def show_user(user_id: str):
    if (user := await user_db.find_one(user_id)) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.put("/{user_id}", response_description="Update a user",
            response_model=User)
async def update_user(user_id: str, user: User):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await user_db.update_one(user_id, user)

        if update_result.modified_count == 1:
            if (updated_user := await user_db.find_one(user_id)) is not None:
                return updated_user

    if (existing_user := await user_db.find_one(user_id)) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.delete("/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str):
    delete_result = await user_db.delete_one(user_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
