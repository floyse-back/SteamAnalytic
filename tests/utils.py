from pydantic import BaseModel


def transform_to_dto(model:BaseModel,orm):
    return model.model_validate(orm).model_dump()