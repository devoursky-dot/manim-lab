from __future__ import annotations
import asyncio
from pathlib import Path
from os import PathLike
import edge_tts
from manim import logger
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover._typing import VoiceoverData
from manim_voiceover.services.base import SpeechService, initialize_speech_service, path_to_string


class EdgeService(SpeechService):
    """SpeechService class for Microsoft Edge's online TTS service via edge-tts."""

    def __init__(
        self,
        voice: str = "ko-KR-InJoonNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        **kwargs: object,
    ):
        initialize_speech_service(self, kwargs)
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "edge",
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume,
            "pitch": self.pitch,
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path_to_string(path)

        output_file = str(Path(cache_dir) / audio_path)

        async def _speak():
            communicate = edge_tts.Communicate(
                input_text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume,
                pitch=self.pitch,
            )
            await communicate.save(output_file)

        try:
            asyncio.run(_speak())
        except Exception as e:
            logger.error(f"EdgeService generation error: {e}")
            raise e

        json_dict: VoiceoverData = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
        return json_dict
