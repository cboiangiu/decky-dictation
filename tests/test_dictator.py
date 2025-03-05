import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path so we can import dictator
sys.path.append(str(Path(__file__).parent.parent))

# Simple mock of Decky for testing
class MockDecky:
    def __init__(self):
        self.DECKY_PLUGIN_DIR = Path(__file__).parent.parent / "dev" / "plugin_dir"
        self.DECKY_PLUGIN_LOG_DIR = self.DECKY_PLUGIN_DIR / "logs"
        self.DECKY_PLUGIN_RUNTIME_DIR = self.DECKY_PLUGIN_DIR / "data"
        self.logger = logging.getLogger('mock_decky')

        # Create required directories
        self.DECKY_PLUGIN_LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.DECKY_PLUGIN_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)

sys.modules['decky'] = MockDecky()

from py_modules.dictator import Dictator

async def main():
    # Basic logging setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('dictator_test')

    try:
        logger.info("Testing dictation")
        dictator = Dictator()
        
        # Test push-to-talk mode
        logger.info("Testing push-to-talk mode")
        await dictator.begin_dictation(True)
        await asyncio.sleep(5)  # Let it run for 5 seconds
        await dictator.end_dictation()

        # Test continuous mode
        logger.info("Testing continuous mode")
        await dictator.begin_dictation(False)
        await asyncio.sleep(5)  # Let it run for 5 seconds
        await dictator.end_dictation()

        logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 