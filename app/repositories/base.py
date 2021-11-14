import abc
import logging
from typing import Generic, TypeVar, Type, Optional, Any

from pydantic import BaseModel

IN_SCHEMA = TypeVar('IN_SCHEMA', bound=BaseModel)
SCHEMA = TypeVar('SCHEMA', bound=BaseModel)
COLLECTION = TypeVar('COLLECTION')

log = logging.getLogger(__name__)


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, COLLECTION]):
    def __init__(self, db_session, db_name: str, collection: str):
        self._db_session = db_session[db_name][collection]

    @property
    @abc.abstractmethod
    def _collection(self) -> Type[COLLECTION]:
        pass

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        pass

    async def create(self, document: IN_SCHEMA) -> SCHEMA:
        db_document = self._collection(**document.dict())
        insert_result = await self._db_session.insert_one(db_document.dict())
        if inserted_document := await self.find_by_id(insert_result.inserted_id):
            return inserted_document
        else:
            log.warning(f'There was an error when trying to insert {document}')
            raise Exception(f'Could not create object')

    async def find_by_id(self, _id) -> Optional[SCHEMA]:
        if document_found := await self._db_session.find_one({"_id": _id}):
            return document_found
        else:
            log.info(f'Could not find object using _id: {_id}')
            return None

    async def find_by_key(self, key: str, value: Any) -> Optional[SCHEMA]:
        if skill_found := await self._db_session.find_one({key: value}):
            return self._schema(**skill_found)
        else:
            log.info(f'Could not find object using key {key}')
            return None
