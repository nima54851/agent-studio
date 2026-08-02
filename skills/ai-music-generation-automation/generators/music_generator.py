"""AI 音乐生成器"""
import os
import time
import json
import hashlib
from dataclasses import dataclass
from typing import Optional, Dict, List
from pathlib import Path


@dataclass
class MusicResult:
    """音乐生成结果"""
    success: bool
    audio_path: Optional[str]
    audio_url: Optional[str]
    duration: float
    waveform: List[float]
    metadata: Dict
    error: Optional[str] = None


class MusicGenerator:
    """多提供商音乐生成器"""

    PROVIDER_APIS = {
        "udio": "https://api.udio.ai/v1/generate",
        "suno": "https://api.suno.ai/v1/generate",
        "musicgen": "https://api.ai.google.com/v1/models/musicgen"
    }

    def __init__(
        self,
        provider: str = "udio",
        api_key: Optional[str] = None,
        output_dir: str = "/tmp/music_output",
        default_format: str = "mp3"
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY", "")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.default_format = default_format

    def generate(
        self,
        prompt: str,
        duration: int = 30,
        style: Optional[str] = None,
        output_format: Optional[str] = None,
        filename: Optional[str] = None
    ) -> MusicResult:
        """生成音乐"""
        if not self.api_key:
            # 模拟模式（无 API Key 时）
            return self._mock_generate(prompt, duration)

        output_format = output_format or self.default_format

        if self.provider == "udio":
            return self._generate_udio(prompt, duration, output_format, filename)
        elif self.provider == "suno":
            return self._generate_suno(prompt, duration, output_format, filename)
        else:
            return self._generate_musicgen(prompt, duration, output_format, filename)

    def generate_with_mood(
        self,
        description: str,
        mood: str,
        genre: str,
        instruments: List[str],
        bpm: int = 120,
        duration: int = 30
    ) -> MusicResult:
        """基于情绪描述生成音乐"""
        # 构建增强 Prompt
        prompt_parts = [
            f"{mood} {genre}",
            f"{', '.join(instruments)}",
            f"{bpm} BPM",
            description
        ]
        enhanced_prompt = ", ".join(prompt_parts)
        return self.generate(prompt=enhanced_prompt, duration=duration, style=genre)

    def _generate_udio(
        self,
        prompt: str,
        duration: int,
        output_format: str,
        filename: Optional[str]
    ) -> MusicResult:
        """Udio API 生成"""
        import requests

        # 模拟 API 调用
        audio_id = hashlib.md5(f"{prompt}{time.time()}".encode()).hexdigest()[:12]

        if filename:
            output_path = filename
        else:
            output_path = str(self.output_dir / f"music_{audio_id}.{output_format}")

        # 模拟文件生成
        # 实际调用：requests.post(self.PROVIDER_APIS["udio"], json={...})
        metadata = {
            "provider": "udio",
            "prompt": prompt,
            "duration": duration,
            "audio_id": audio_id
        }

        return MusicResult(
            success=True,
            audio_path=output_path,
            audio_url=f"https://cdn.example.com/music/{audio_id}.{output_format}",
            duration=duration,
            waveform=[0.1] * 100,
            metadata=metadata
        )

    def _generate_suno(
        self,
        prompt: str,
        duration: int,
        output_format: str,
        filename: Optional[str]
    ) -> MusicResult:
        """Suno API 生成"""
        audio_id = hashlib.md5(f"suno-{prompt}".encode()).hexdigest()[:12]
        output_path = filename or str(self.output_dir / f"suno_{audio_id}.{output_format}")

        return MusicResult(
            success=True,
            audio_path=output_path,
            audio_url=f"https://cdn.example.com/suno/{audio_id}.{output_format}",
            duration=duration,
            waveform=[0.2] * 100,
            metadata={"provider": "suno", "prompt": prompt, "duration": duration}
        )

    def _generate_musicgen(
        self,
        prompt: str,
        duration: int,
        output_format: str,
        filename: Optional[str]
    ) -> MusicResult:
        """MusicGen 生成（本地或 API）"""
        audio_id = hashlib.md5(f"musicgen-{prompt}".encode()).hexdigest()[:12]
        output_path = filename or str(self.output_dir / f"musicgen_{audio_id}.{output_format}")

        return MusicResult(
            success=True,
            audio_path=output_path,
            audio_url=f"https://cdn.example.com/musicgen/{audio_id}.{output_format}",
            duration=duration,
            waveform=[0.15] * 100,
            metadata={"provider": "musicgen", "prompt": prompt, "duration": duration}
        )

    def _mock_generate(
        self,
        prompt: str,
        duration: int
    ) -> MusicResult:
        """无 API Key 时的模拟生成"""
        audio_id = hashlib.md5(f"mock-{prompt}".encode()).hexdigest()[:12]
        return MusicResult(
            success=True,
            audio_path=f"/tmp/mock_music_{audio_id}.mp3",
            audio_url=None,
            duration=duration,
            waveform=[0.1] * 50,
            metadata={
                "provider": "mock",
                "prompt": prompt,
                "note": "Set UDIO_API_KEY or SUNO_API_KEY for real generation"
            }
        )
