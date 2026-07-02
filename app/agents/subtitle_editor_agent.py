import json
from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.subtitle_editor import SubtitleEditor


class SubtitleEditorAgent(BaseAgent):

    name = "SubtitleEditorAgent"

    def __init__(self):

        self.editor = SubtitleEditor()

    def execute(
        self,
        context: JobContext,
    ):

        subtitle = self.editor.create_hook_subtitle(
            subtitle=context.subtitle,
            hook_start=context.hook.start,
            hook_end=context.hook.end,
        )

        context.subtitle = subtitle

        output = Path("subtitles/final_subtitle.json")

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                subtitle.model_dump(),
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        context.subtitle_file = output

        return self.success(context)