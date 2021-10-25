import logging
from typing import List

from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse

import app.crud.item as item_crud
from app.schema.item import Item, ItemInDB, ItemId

log = logging.getLogger(__name__)

router = APIRouter(
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_description="Add new item", response_model=ItemInDB, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    print(f"attempting to create item with body {item}")
    new_item = await item_crud.insert_item(item)
    return new_item


@router.get("/", response_description="List all items", response_model=List[ItemInDB])
async def list_items():
    return await item_crud.find_items()


@router.get("/{item_id}", response_description="Get a single item", response_model=ItemInDB)
async def show_item(item_id: ItemId):
    if (item := await item_crud.find_by_id(item_id)) is not None:
        return item

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.put("/{item_id}", response_description="Update a item", response_model=ItemInDB)
async def update_item(item_id: ItemId, item: Item):
    if update_result := await item_crud.update_one(item_id, item):
        if update_result.matched_count == 1:
            return await item_crud.find_by_id(item_id)

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@router.delete("/{item_id}", response_description="Delete a item")
async def delete_item(item_id: ItemId):
    delete_result = await item_crud.delete_one(item_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
