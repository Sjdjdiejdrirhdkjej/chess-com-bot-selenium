import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock out heavy dependencies that might not be available or needed for this simple test
sys.modules['selenium'] = MagicMock()
sys.modules['selenium.common'] = MagicMock()
sys.modules['selenium.common.exceptions'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.common'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools'] = MagicMock()
sys.modules['selenium.webdriver.common.devtools.v119'] = MagicMock()
sys.modules['selenium.webdriver.chrome'] = MagicMock()
sys.modules['selenium.webdriver.chrome.options'] = MagicMock()
sys.modules['selenium.webdriver.chrome.service'] = MagicMock()
sys.modules['selenium.webdriver.common.by'] = MagicMock()
sys.modules['selenium.webdriver.support'] = MagicMock()
sys.modules['selenium.webdriver.support.ui'] = MagicMock()
sys.modules['selenium.webdriver.support.expected_conditions'] = MagicMock()
sys.modules['selenium.webdriver.remote'] = MagicMock()
sys.modules['selenium.webdriver.remote.webdriver'] = MagicMock()
sys.modules['stockfish'] = MagicMock()
sys.modules['typer'] = MagicMock()

# Since importing main.py has top-level side effects (like checking for stockfish and calling input()/exit(1)),
# we need to mock these out before importing main.
with patch('builtins.input', return_value=''), patch('builtins.exit', MagicMock()):
    import main

class TestIsDocker(unittest.TestCase):
    def test_is_docker_with_hub_host(self):
        with patch.dict(os.environ, {"hub_host": "some_host"}):
            self.assertTrue(main.is_docker())

    def test_is_docker_without_hub_host(self):
        # Create an environment copy without 'hub_host'
        env_copy = os.environ.copy()
        if 'hub_host' in env_copy:
            del env_copy['hub_host']

        with patch.dict(os.environ, env_copy, clear=True):
            self.assertFalse(main.is_docker())

if __name__ == '__main__':
    unittest.main()
