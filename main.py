import os
import traceback
import subprocess

import logging

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

os.environ['PYTHONPATH'] = "/home/deck/homebrew/plugins/decky-dictation/bin/vosk"
os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"
os.environ["XDG_SESSION_TYPE"] = "wayland"
os.environ["DISPLAY"] = ":1" # FIXME: the steam ui seems to be 0 and the actual game 1. can we detect current window in focus maybe?

class Plugin:
    # Begins dictation
    async def begin(self):
        try:
            logger.info("Begin dictation")
            subprocess.Popen("/home/deck/homebrew/plugins/decky-dictation/bin/nerd-dictation/nerd-dictation begin --vosk-model-dir=/home/deck/homebrew/plugins/decky-dictation/bin/nerd-dictation/model --numbers-min-value 2 --numbers-no-suffix --full-sentence --numbers-as-digits --numbers-use-separator --timeout 4 --punctuate-from-previous-timeout 2 &", shell=True, stdout=std_out_file, stderr=std_err_file)
        except Exception:
            await Plugin.end(self)
            logger.info(traceback.format_exc())
        return

    # Ends dictation
    async def end(self):
        try:
            logger.info("End dictation")
            subprocess.Popen("/home/deck/homebrew/plugins/decky-dictation/bin/nerd-dictation/nerd-dictation end", shell=True, stdout=std_out_file, stderr=std_err_file)
        except Exception:
            logger.info(traceback.format_exc())
        return

    async def _main(self):
        return

    async def _unload(self):
        logger.info("Unload was called")
        await Plugin.end(self)
        return
