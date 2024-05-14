from typing import Annotated

from pydantic import BaseModel, Field


class PostUpdateRequest(BaseModel):
    pk: Annotated[int, Field(alias="postId", serialization_alias="pk")]
    title: Annotated[str, Field(alias="postTitle", serialization_alias="title")]
    description: Annotated[str, Field(alias="postDescription", serialization_alias="description")]
    is_published: Annotated[bool, Field(alias="postStatus", serialization_alias="is_published")]
