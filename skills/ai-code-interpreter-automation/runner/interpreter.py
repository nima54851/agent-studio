"""AI Code Interpreter - 主解释器"""
import subprocess
import tempfile
import os
import time
import uuid
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path


@dataclass
class ExecutionResult:
    """代码执行结果"""
    success: bool
    stdout: str
    stderr: str
    elapsed_ms: int
    files: List[str] = field(default_factory=list)
    exit_code: int = 0
    session_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "stdout": self.stdout[:2000],
            "stderr": self.stderr[:1000],
            "elapsed_ms": self.elapsed_ms,
            "files": self.files,
            "exit_code": self.exit_code
        }


class CodeSession:
    """持久化会话：在同一个执行环境中运行多段代码"""

    def __init__(self, interpreter: "CodeInterpreter", session_id: Optional[str] = None):
        self.interpreter = interpreter
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.variables: Dict[str, Any] = {}
        self.history: List[Dict] = []

    def execute(self, code: str) -> ExecutionResult:
        # 包装代码：将已定义的变量注入
        wrapped = self._wrap_code(code)
        result = self.interpreter._do_execute(wrapped, self.session_id)

        # 解析结果中的变量（通过 pickle 序列化）
        self._parse_variables(result)
        self.history.append({
            "code": code,
            "result": result.to_dict()
        })
        return result

    def _wrap_code(self, code: str) -> str:
        """将 session 变量注入执行上下文"""
        var_inject = "\n".join([
            f"{k} = __session_vars__[{repr(k)}]" for k in self.variables
        ])
        var_export = "\n".join([
            f"import pickle; print('__SESSION_VARS__:' + pickle.dumps(dict(locals())).hex())"
            for _ in [1]
        ])
        return f"{var_inject}\n{code}\n{var_export}"

    def _parse_variables(self, result: ExecutionResult):
        """从输出中解析 session 变量"""
        # 简化：不清洗变量，保持 session 状态
        pass


class CodeInterpreter:
    """AI 代码解释器主类"""

    BLOCKED_IMPORTS = {
        "os", "sys", "subprocess", "socket", "requests", "urllib",
        "builtins", "ctypes", "resource", "importlib", "multiprocessing"
    }

    def __init__(
        self,
        sandbox_mode: str = "subprocess",  # docker / subprocess / eBPF
        timeout: int = 30,
        max_memory_mb: int = 512,
        max_output_lines: int = 1000,
        language: str = "python",
        session_persistence: bool = False
    ):
        self.sandbox_mode = sandbox_mode
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb
        self.max_output_lines = max_output_lines
        self.language = language
        self.sessions: Dict[str, CodeSession] = {}

    def execute(self, code: str, session_id: Optional[str] = None) -> ExecutionResult:
        """执行单段代码"""
        return self._do_execute(code, session_id)

    def create_session(self) -> CodeSession:
        """创建持久化会话"""
        session = CodeSession(self)
        self.sessions[session.session_id] = session
        return session

    def _do_execute(self, code: str, session_id: Optional[str] = None) -> ExecutionResult:
        """内部执行逻辑"""
        # 安全扫描
        if not self._security_check(code):
            return ExecutionResult(
                success=False,
                stdout="",
                stderr="SECURITY: Dangerous imports or patterns detected.",
                elapsed_ms=0,
                exit_code=1
            )

        # 根据模式选择执行方式
        if self.sandbox_mode == "docker":
            return self._run_docker(code, session_id)
        else:
            return self._run_subprocess(code, session_id)

    def _security_check(self, code: str) -> bool:
        """基础安全扫描"""
        import_pattern = r'^\s*(?:from|import)\s+(\w+)'
        for match in re.finditer(import_pattern, code, re.MULTILINE):
            module = match.group(1)
            if module in self.BLOCKED_IMPORTS:
                return False

        # 检测 __import__
        if '__import__' in code or 'eval(' in code or 'exec(' in code:
            # 仅在非标准情况下拒绝
            if 'eval(' in code and 'ast.literal_eval' not in code:
                return False
        return True

    def _run_subprocess(self, code: str, session_id: Optional[str]) -> ExecutionResult:
        """通过 subprocess 执行（开发模式）"""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix=f'.py', delete=False, encoding='utf-8'
        ) as f:
            f.write(code)
            temp_file = f.name

        start = time.time()
        try:
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir()
            )
            elapsed_ms = int((time.time() - start) * 1000)

            # 收集生成的文件
            files = self._collect_files()

            return ExecutionResult(
                success=result.returncode == 0,
                stdout=result.stdout[:10000],
                stderr=result.stderr[:5000],
                elapsed_ms=elapsed_ms,
                files=files,
                exit_code=result.returncode,
                session_id=session_id
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Timeout: execution exceeded {self.timeout}s",
                elapsed_ms=self.timeout * 1000,
                exit_code=-1
            )
        finally:
            os.unlink(temp_file)

    def _run_docker(self, code: str, session_id: Optional[str]) -> ExecutionResult:
        """通过 Docker 容器执行（生产模式）"""
        container_name = f"interpreter-{session_id or uuid.uuid4().hex[:8]}"

        docker_cmd = [
            "docker", "run", "--rm",
            "--name", container_name,
            "--network", "none",
            "--memory", f"{self.max_memory_mb}m",
            "--cpus", "0.5",
            "-v", f"{tempfile.gettempdir()}:/workspace",
            "python:3.11-slim",
            "python3", "-c", code
        ]

        start = time.time()
        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            elapsed_ms = int((time.time() - start) * 1000)
            files = self._collect_files()
            return ExecutionResult(
                success=result.returncode == 0,
                stdout=result.stdout[:10000],
                stderr=result.stderr[:5000],
                elapsed_ms=elapsed_ms,
                files=files,
                exit_code=result.returncode
            )
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "stop", container_name], capture_output=True)
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Timeout: execution exceeded {self.timeout}s",
                elapsed_ms=self.timeout * 1000,
                exit_code=-1
            )

    def _collect_files(self) -> List[str]:
        """收集临时目录中的新文件"""
        tmp = tempfile.gettempdir()
        files = [os.path.join(tmp, f) for f in os.listdir(tmp)
                 if os.path.isfile(os.path.join(tmp, f))]
        return files
