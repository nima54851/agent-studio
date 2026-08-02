"""音频混音处理器"""
import os
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MixResult:
    success: bool
    output_path: str
    duration: float
    file_size_kb: float
    error: Optional[str] = None


class AudioMixer:
    """FFmpeg 驱动的音频混音处理器"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg = ffmpeg_path
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        try:
            subprocess.run([self.ffmpeg, "-version"],
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("FFmpeg not found. Install: apt install ffmpeg")

    def mix(
        self,
        input_file: str,
        output_file: str,
        fade_in: float = 0.0,
        fade_out: float = 0.0,
        normalize: bool = False,
        volume: float = 1.0,
        bitrate: str = "320k"
    ) -> MixResult:
        """混音处理主方法"""
        filters = []

        if fade_in > 0:
            filters.append(f"afade=t=in:st=0:d={fade_in}")

        if fade_out > 0:
            # 获取文件时长
            duration = self._get_duration(input_file)
            fade_start = max(0, duration - fade_out)
            filters.append(f"afade=t=out:st={fade_start}:d={fade_out}")

        if normalize:
            filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")

        if volume != 1.0:
            filters.append(f"volume={volume}")

        filter_str = ",".join(filters) if filters else None

        cmd = [self.ffmpeg, "-y", "-i", input_file]

        if filter_str:
            cmd += ["-af", filter_str]

        cmd += [
            "-ar", "44100",
            "-ab", bitrate,
            "-ac", "2",
            output_file
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            duration = self._get_duration(output_file)
            size_kb = os.path.getsize(output_file) / 1024

            return MixResult(
                success=True,
                output_path=output_file,
                duration=duration,
                file_size_kb=size_kb
            )
        except subprocess.CalledProcessError as e:
            return MixResult(
                success=False,
                output_path=output_file,
                duration=0,
                file_size_kb=0,
                error=e.stderr
            )

    def concatenate(
        self,
        input_files: List[str],
        output_file: str,
        crossfade_duration: float = 1.0
    ) -> MixResult:
        """拼接多段音频（带交叉淡入淡出）"""
        # 创建临时文件列表
        concat_list = self.output_dir / "concat_list.txt"
        with open(concat_list, "w") as f:
            for file in input_files:
                f.write(f"file '{file}'\n")

        cmd = [
            self.ffmpeg, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-af", f"acrossfade=d={crossfade_duration}",
            output_file
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            concat_list.unlink()
            return MixResult(
                success=True,
                output_path=output_file,
                duration=self._get_duration(output_file),
                file_size_kb=os.path.getsize(output_file) / 1024
            )
        except subprocess.CalledProcessError as e:
            return MixResult(
                success=False,
                output_path=output_file,
                duration=0,
                file_size_kb=0,
                error=e.stderr
            )

    def extract_waveform(self, input_file: str, output_image: str) -> bool:
        """提取波形图（用于可视化）"""
        cmd = [
            self.ffmpeg, "-y",
            "-i", input_file,
            "-filter_complex",
            "compand,showwavespic=s=800x200:colors=white",
            "-frames:v", "1",
            output_image
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _get_duration(self, file: str) -> float:
        """获取音频时长（秒）"""
        cmd = [
            self.ffmpeg, "-i", file,
            "-f", "null", "-"
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            # 解析 Duration
            import re
            match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})',
                           result.stderr)
            if match:
                h, m, s, cs = match.groups()
                return int(h) * 3600 + int(m) * 60 + int(s) + int(cs) / 100
        except Exception:
            pass
        return 0.0

    @property
    def output_dir(self) -> Path:
        from pathlib import Path
        d = Path("/tmp/music_output")
        d.mkdir(parents=True, exist_ok=True)
        return d
