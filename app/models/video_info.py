from pydantic import BaseModel


class VideoInfo(BaseModel):
    title: str
    video_id: str
    channel: str
    duration: int
    thumbnail: str
    download_path: str