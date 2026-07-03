from pydantic import BaseModel


class VideoMetadata(BaseModel):

    title: str

    description: str

    hashtags: list[str]


class Metadata(BaseModel):

    long_video: VideoMetadata

    shorts: list[VideoMetadata]