import sys
from unittest.mock import MagicMock
import time
import asyncio

sys.modules['selenium'] = MagicMock()
sys.modules['selenium.common'] = MagicMock()
sys.modules['selenium.common.exceptions'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.common'] = MagicMock()
sys.modules['selenium.webdriver.common.by'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools.v119'] = MagicMock()
sys.modules['selenium.webdriver.chrome'] = MagicMock()
sys.modules['selenium.webdriver.chrome.options'] = MagicMock()
sys.modules['selenium.webdriver.chrome.service'] = MagicMock()
sys.modules['selenium.webdriver.support'] = MagicMock()
sys.modules['selenium.webdriver.support.ui'] = MagicMock()
sys.modules['selenium.webdriver.remote'] = MagicMock()
sys.modules['selenium.webdriver.remote.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.support.expected_conditions'] = MagicMock()
sys.modules['stockfish'] = MagicMock()
sys.modules['typer'] = MagicMock()

import main

main.C.exit_delay = 1
main.next_game_auto_ = False

async def mock_actions(*args, **kwargs):
    return False

main.actions = mock_actions
main.setup_driver = MagicMock()

async def run_benchmark():
    start_time = time.time()

    async def bg_task():
        iterations = 0
        while time.time() - start_time < 1.5:
            await asyncio.sleep(0.1)
            iterations += 1
        return iterations

    task = asyncio.create_task(bg_task())

    # Let bg task start
    await asyncio.sleep(0.1)

    t0 = time.time()
    await main.main_()
    t1 = time.time()

    iterations = await task

    print(f"main_ took {t1 - t0:.2f} seconds")
    print(f"Background task iterations: {iterations}")

asyncio.run(run_benchmark())
