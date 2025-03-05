import asyncio
import decky
import os
from dictator import Dictator
# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`

# required by pulse audio because of a non-standard shell
os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"


class Plugin:
    def __init__(self):
        self.dictator = Dictator()

    async def begin_dictation(self, push_to_dictate: bool):
        try:
            decky.logger.info("Starting dictation process...")
            await self.dictator.begin_dictation(push_to_dictate)
            decky.logger.info("Dictation process started successfully")
        except Exception as e:
            await self.end_dictation()
            decky.logger.error(f"Failed to start dictation: {str(e)}")
            raise

    async def end_dictation(self):
        try:
            await self.dictator.end_dictation()
        except Exception:
            decky.logger.error("Failed to stop dictation")

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.loop = asyncio.get_event_loop()
        decky.logger.info("Hello World!")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Stopping dictation and cleaning up...")
        await self.end_dictation()
        decky.logger.info("Cleanup complete")

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Performing final cleanup...")
        decky.logger.info("Uninstall cleanup complete")
