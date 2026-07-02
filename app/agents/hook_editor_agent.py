from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.models.job_context import JobContext
from app.services.audio_editor import AudioEditor


class HookEditorAgent(BaseAgent):

    name = "HookEditorAgent"

    def __init__(self):

        self.editor = AudioEditor()

    def execute(
        self,
        context: JobContext,
    ):

        output = Path("output/audio_with_hook.wav")

        self.editor.create_hook_audio(
            context.local_audio,
            context.hook.start,
            context.hook.end,
            output,
        )

        context.local_audio = output

        return self.success(context)