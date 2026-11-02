import os
import sys
from pathlib import Path

API = Path(__file__).resolve().parent.parent / "api"
os.environ.setdefault("DATABASE_URL", "postgresql://x:x@localhost/x")   # never connected: startup is skipped
sys.path.insert(0, str(API))
os.chdir(API)   # main.py serves ./static

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    return TestClient(main.app)   # no `with`: the lifespan (database) does not run


@pytest.fixture
def ai(monkeypatch):
    """Replaces the model call. Set ai.reply to what the model should return; ai.prompt and ai.max_tokens record the call."""
    class Fake:
        reply = None
        prompt = ""
        max_tokens = None

        def __call__(self, prompt, max_tokens=8000):
            self.prompt, self.max_tokens = prompt, max_tokens

            class Usage:
                input_tokens, output_tokens = 1, 2
            return self.reply, Usage()

    fake = Fake()
    monkeypatch.setattr(main, "ask_json", fake)
    return fake
