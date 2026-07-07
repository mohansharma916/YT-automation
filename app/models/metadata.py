from pydantic import BaseModel, Field


####################################################
# Long Video Metadata
####################################################

class LongVideoMetadata(BaseModel):

    part: int = 0

    start: float = 0

    end: float = 0

####################################################
# Short Metadata
####################################################

class ShortMetadata(BaseModel):

    index: int = 0

    start: float = 0

    end: float = 0

####################################################
# Root Metadata
####################################################

class Metadata(BaseModel):

    long_videos: list[LongVideoMetadata] = Field(
        default_factory=list,
    )

    shorts: list[ShortMetadata] = Field(
        default_factory=list,
    )