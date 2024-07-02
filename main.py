import os

# import zipfile
# Old package.json remote binary config
# "remote_binary": [
# {
#     "name": "vosk-model-small-en-us-0.15.zip",
#     "url": "https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip",
#     "sha256hash": "30f26242c4eb449f948e42cb302dd7a686cb29a3423a8367f99ff41780942498"
# }
# ],
import traceback
import subprocess

import logging

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin


logging.basicConfig(
    filename="/tmp/decky-dictation.log",
    format="Decky Dictation: %(asctime)s %(levelname)s %(message)s",
    filemode="w+",
    force=True,
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
std_out_file = open("/tmp/decky-dictation-std-out.log", "w")
std_err_file = open("/tmp/decky-dictation-std-err.log", "w")

plugin_path = os.environ["DECKY_PLUGIN_DIR"]
model_path = f"{plugin_path}/bin/vosk-model-small-en-us-0.15"
os.environ["PYTHONPATH"] = f"{plugin_path}/bin/vosk"
os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"
os.environ["XDG_SESSION_TYPE"] = "wayland"
os.environ["DISPLAY"] = (
    ":1"  # FIXME: the steam ui seems to be 0 and the actual game 1. can we detect current window in focus maybe?
)


class Plugin:
    process = None
    # Begins dictation
    async def begin(self, push_to_dictate: bool):
        try:
            if not os.path.exists(model_path):
                logger.info("Model directory not found")
                return
            if self.process is not None:
                if self.process.poll() is None:
                    logger.info("Dictation currently running, exiting early")
                    return
            logger.info("Begin dictation")
            timeout = ("--timeout 4", "")[push_to_dictate]
            self.process = subprocess.Popen(
                f'"{plugin_path}/bin/nerd-dictation/nerd-dictation" begin --vosk-model-dir="{model_path}" --numbers-min-value 2 --numbers-no-suffix --full-sentence --numbers-as-digits --numbers-use-separator {timeout} --punctuate-from-previous-timeout 2',
                shell=True,
                stdout=std_out_file,
                stderr=std_err_file,
            )
        except Exception:
            await Plugin.end(self)
            logger.info(traceback.format_exc())
        return

    # Ends dictation
    async def end(self):
        try:
            logger.info("End dictation")
            if self.process is not None:
                self.process.kill()

        except Exception:
            logger.info(traceback.format_exc())
        return

    async def _main(self):
        # model_zip_path = f"{plugin_path}/bin/vosk-model-small-en-us-0.15.zip"
        # if os.path.isfile(model_zip_path) and not os.path.exists(model_path):
        #     with zipfile.ZipFile(model_zip_path, "r") as zip_ref:
        #         zip_ref.extractall(f"{plugin_path}/bin")
        #     logger.info("Model was unzipped")
        #     os.remove(model_zip_path)
        if not os.path.exists(model_path):
            logger.info("Model directory not found")
        return

    async def _unload(self):
        logger.info("Unload was called")
        await Plugin.end(self)
        return
