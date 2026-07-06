from pathlib import Path
from typing import Optional

from openai.types import Metadata
from pydantic import BaseModel
from pydantic import Field
from app.models.short import Shorts
from app.models.timeline import Timeline
from app.models.transcript import Transcript
from app.models.subtitle import Subtitle
from app.models.video_parts import VideoParts




class JobContext(BaseModel):
    youtube_url: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    subtitle: Optional[Subtitle] = None
    local_audio: Optional[Path] = None
    subtitle_json_file: Optional[Path] = None
    downloaded_video: Optional[Path] = None
    subtitle_ass_file: Optional[Path] = None
    transcript: Optional[Transcript] = None
    subtitle_file: Path | None = None
    output_video: Optional[Path] = None
    shorts: Shorts | None = None
    transcript_file: Optional[Path] = None
    video_with_new_audio: Optional[Path] = None
    timeline: Timeline | None = None
    metadata_ai: Metadata | None = None
    final_audio: Path | None = None
    final_subtitle: Path | None = None
    video_parts: VideoParts | None = None
    background_video: Path | None = None
    audio_duration: float | None = None
    background_video_url: str | None = None
    output_long_videos: list[Path] = Field(default_factory=list)
    output_short_videos: list[Path] = Field(default_factory=list)
