"""Manages voice dictation processes using nerd-dictation, adapted as a Decky plugin."""

import os
import asyncio
import decky
from pathlib import Path

# Base paths (from dictator.py)
BIN_PATH = Path(decky.DECKY_PLUGIN_DIR) / "bin"
LOG_DIR = Path(decky.DECKY_PLUGIN_LOG_DIR)

# Application-specific paths (from dictator.py)
NERD_DICTATION_PATH = BIN_PATH / "nerd-dictation/nerd-dictation"
NERD_DICTATION_COOKIE_PATH = Path(decky.DECKY_PLUGIN_RUNTIME_DIR) / "nerd-dictation-cookie"
VOSK_DIR = BIN_PATH / "vosk_libraries"
MODEL_DIR = BIN_PATH / "vosk-model-small-en-us-0.15"
DOTOOL_DIR = BIN_PATH / "dotool"

# Log files (from dictator.py)
STD_OUT_FILE = open(LOG_DIR / "decky-dictation-std-out.log", "w")
STD_ERR_FILE = open(LOG_DIR / "decky-dictation-std-err.log", "w")

# Environment setup (from dictator.py)
if str(DOTOOL_DIR) not in os.environ["PATH"].split(":"):
    os.environ["PATH"] = f"{DOTOOL_DIR}:{os.environ['PATH']}"
pythonpath = os.environ.get('PYTHONPATH', '').split(':')
if str(VOSK_DIR) not in pythonpath:
    os.environ["PYTHONPATH"] = f"{VOSK_DIR}:{os.environ.get('PYTHONPATH', '')}"

class Dictator():
    """A Decky plugin managing nerd-dictation, matching the original Dictator API."""

    def __init__(self):
        self.process = None
        self.last_start_time = 0
        self.debounce_interval = 1.0  # 1 second debounce, from dictator2.py

    async def begin_dictation(self, push_to_dictate: bool) -> None:
        """Start a new dictation process with specified mode, matching dictator.py signature."""
        current_time = asyncio.get_event_loop().time()  # Async-friendly time, from dictator2.py
        if self.process or (current_time - self.last_start_time < self.debounce_interval):
            decky.logger.warning("Dictation already running or debounced, ignoring request")
            return

        try:
            timeout_arg = ["--timeout", "4"] if push_to_dictate else []
            command = [
                str(NERD_DICTATION_PATH), "begin",
                f"--cookie={NERD_DICTATION_COOKIE_PATH}",
                f"--vosk-model-dir={MODEL_DIR}",
                "--simulate-input-tool", "DOTOOL",
                "--full-sentence",
                "--numbers-min-value", "2",
                "--numbers-no-suffix",
                "--numbers-as-digits",
                "--numbers-use-separator",
                "--punctuate-from-previous-timeout", "2",
            ]
            if timeout_arg:
                command.extend(timeout_arg)

            decky.logger.info("Starting dictation process...")
            self.process = await asyncio.create_subprocess_exec(
                *command,
                stdout=STD_OUT_FILE,
                stderr=STD_ERR_FILE,
            )
            self.last_start_time = current_time
            decky.logger.info(f"Dictation process started with PID: {self.process.pid}")
            asyncio.create_task(self._monitor_process())  # Async monitoring
        except Exception as e:
            decky.logger.error(f"Failed to start dictation: {str(e)}")
            self.process = None
            raise

    async def end_dictation(self) -> None:
        """Stop the current dictation process."""
        if not self.process or self.process.returncode is not None:
            self.process = None  # Cleanup if already exited
            return

        try:
            decky.logger.info("Stopping dictation process...")
            end_command = [
                str(NERD_DICTATION_PATH), "end",
                f"--cookie={NERD_DICTATION_COOKIE_PATH}"
            ]
            end_process = await asyncio.create_subprocess_exec(
                *end_command,
                stdout=STD_OUT_FILE,
                stderr=STD_ERR_FILE
            )
            await asyncio.wait_for(end_process.wait(), timeout=1.0)  # Graceful stop with timeout
            await asyncio.wait_for(self.process.wait(), timeout=0.5)
            decky.logger.info("Dictation process stopped")
        except asyncio.TimeoutError:
            decky.logger.warning("nerd-dictation end timed out, forcing termination...")
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=0.5)
            except asyncio.TimeoutError:
                decky.logger.warning("Graceful termination failed, forcing kill...")
                self.process.kill()
                await self.process.wait()
        except Exception as e:
            decky.logger.error(f"Error stopping dictation: {str(e)}")
            try:
                self.process.kill()
                await self.process.wait()
            except Exception:
                pass  # Ignore if already gone
        finally:
            self.process = None  # Always reset, from both

    async def _monitor_process(self):
        """Monitor and clean up the dictation process."""
        if self.process:
            await self.process.wait()  # Wait for natural exit (e.g., timeout)
            self.process = None


# Optional cleanup for log files (from dictator.py)
def __del__():
    if not STD_OUT_FILE.closed:
        STD_OUT_FILE.close()
    if not STD_ERR_FILE.closed:
        STD_ERR_FILE.close()