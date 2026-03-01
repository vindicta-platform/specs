This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.agent/workflows/jd-bugfix.md
.agent/workflows/sd-implement.md
.agent/workflows/sse-code-review.md
.github/workflows/docs.yml
.gitignore
.specify/memory/constitution.md
.specify/templates/plan-template.md
.specify/templates/spec-template.md
.specify/templates/tasks-template.md
docs/index.md
features/integrity.feature
features/steps/integrity_steps.py
mkdocs.yml
pyproject.toml
README.md
src/warscribe_system/health.py
src/warscribe/__init__.py
src/warscribe/core/__init__.py
src/warscribe/core/schema/__init__.py
src/warscribe/core/schema/action.py
src/warscribe/core/schema/transcript.py
src/warscribe/core/schema/unit.py
src/warscribe/integrity.py
src/warscribe/parser/__init__.py
src/warscribe/parser/api.py
src/warscribe/parser/chat_parser.py
src/warscribe/parser/db.py
src/warscribe/parser/downloader.py
src/warscribe/parser/ingest_text.py
src/warscribe/parser/orchestrator.py
src/warscribe/parser/query_engine.py
src/warscribe/parser/retry_embeddings.py
src/warscribe/parser/transcriber.py
src/warscribe/parser/utils.py
src/warscribe/parser/warscribe_llm.py
src/warscribe/parser/worker.py
tests/test_scribe.py
```

# Files

## File: .agent/workflows/jd-bugfix.md
```markdown
---`ndescription: Bug fix workflow for learning developers`n---`n1. Reproduce the bug with an automated test`n2. execute `/speckit.plan` for the fix`n3. execute `/speckit.tasks``n4. execute `/speckit.implement``n5. Verify fix and delete reproduction test if temporary
```

## File: .agent/workflows/sd-implement.md
```markdown
---`ndescription: Feature implementation from specification to PR`n---`n1. Read the feature specification in `.specify/specs/``n2. execute `/speckit.plan``n3. execute `/speckit.tasks``n4. execute `/speckit.implement`
```

## File: .agent/workflows/sse-code-review.md
```markdown
---`ndescription: Comprehensive code review with mentoring feedback`n---`n1. execute `git diff` against target branch`n2. Perform static analysis check`n3. Provide feedback on architecture, performance, and constitution compliance
```

## File: .github/workflows/docs.yml
```yaml
name: docs
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

## File: .gitignore
```
__pycache__/
*.pyc
.DS_Store
.env
node_modules/
coverage/
.pytest_cache/
dist/
build/
```

## File: docs/index.md
```markdown
# WARScribe System Documentation

Welcome to the **WARScribe System** documentation — notation, parsing, and transcript reconstruction for the Vindicta Platform.

## Modules

- **WARScribe Core**: Core notation models and domain logic.
- **WARScribe Parser**: Standalone parser for the Wargame Notation System (WNS).
- **Transcript Toolkit**: Tools for battle transcript handling and replay.

## Links

- [GitHub Repository](https://github.com/vindicta-platform/warscribe-system)
- [WARScribe Whitepaper](https://github.com/vindicta-platform/vindicta-foundation/blob/main/docs/concepts/warscribe-whitepaper.md)
```

## File: features/integrity.feature
```
Feature: System Integrity Check

  Scenario: Agent reports system integrity
    Given the Warscribe System is active
    When I request an integrity check
    Then the system status should be "operational"
    And the response should contain a timestamp
```

## File: features/steps/integrity_steps.py
```python
from behave import given, when, then
from warscribe.integrity import verify_integrity
import datetime

@given('the Warscribe System is active')
def step_impl(context):
    pass

@when('I request an integrity check')
def step_impl(context):
    context.response = verify_integrity()

@then('the system status should be "operational"')
def step_impl(context):
    assert context.response['status'] == 'operational'

@then('the response should contain a timestamp')
def step_impl(context):
    assert 'timestamp' in context.response
    assert isinstance(context.response['timestamp'], str)
```

## File: mkdocs.yml
```yaml
site_name: WARScribe System
site_description: Notation, Parsing, and Transcripts for the Vindicta Platform.
site_author: Vindicta Platform Contributors
site_url: https://vindicta-platform.github.io/warscribe-system/

repo_name: vindicta-platform/warscribe-system
repo_url: https://github.com/vindicta-platform/warscribe-system

theme:
  name: material
  palette:
    - scheme: slate
      primary: blue
      accent: light blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
    - scheme: default
      primary: blue
      accent: light blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
  font:
    text: Outfit
    code: JetBrains Mono

nav:
  - Home: index.md

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.details
  - attr_list
  - md_in_html

plugins:
  - search
```

## File: pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "warscribe-system"
version = "0.1.0"
description = "Unified Scribe System: Action Notation, Parsing, and Game State Reconstruction"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "vindicta-foundation",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "pytest>=8.0.0",
]


[tool.hatch.build.targets.wheel]
packages = ["src/warscribe"]

[tool.hatch.metadata]
allow-direct-references = true

[tool.uv.sources]
vindicta-foundation = { path = "../vindicta-foundation", editable = true }

[tool.mypy]
strict = true
python_version = "3.12"

[tool.ruff]
line-length = 88
target-version = "py312"
```

## File: README.md
```markdown
# WarScribe System

Unified system for Warhammer 40k action notation, parsing, and game state reconstruction.

## Structure

- `warscribe.core`: Domain models and schemas (Units, Actions, Transcripts).
- `warscribe.parser`: Logic for ingesting chat logs and reconstructing game state.

## Documentation

> **📌 Important:** The WARScribe notation standard and parsing logic are documented in [**vindicta-foundation**](https://github.com/vindicta-platform/vindicta-foundation/blob/main/docs/concepts/warscribe.md).

## Usage


This package is part of the Vindicta Platform.
```

## File: src/warscribe_system/health.py
```python
import time

def check_health() -> dict:
    """Returns the health status of the service."""
    return {'status': 'ok', 'realm': 'warscribe-system', 'timestamp': time.time()}
```

## File: src/warscribe/__init__.py
```python

```

## File: src/warscribe/core/__init__.py
```python

```

## File: src/warscribe/core/schema/__init__.py
```python

```

## File: src/warscribe/core/schema/action.py
```python
"""
Action models for WARScribe notation.

Core action types per ROADMAP v0.1.0:
- Move
- Shoot
- Charge
- Fight
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, Field

from warscribe.core.schema.unit import UnitReference
from vindicta_foundation.models.base import VindictaModel


class ActionType(str, Enum):
    """Types of actions that can be recorded."""

    MOVE = "move"
    SHOOT = "shoot"
    CHARGE = "charge"
    FIGHT = "fight"
    ADVANCE = "advance"
    FALL_BACK = "fall_back"
    CONSOLIDATE = "consolidate"
    PILE_IN = "pile_in"
    HEROIC_INTERVENTION = "heroic_intervention"
    STRATAGEM = "stratagem"
    ABILITY = "ability"
    OBJECTIVE = "objective"


class ActionResult(str, Enum):
    """Result of an action."""

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"


class BaseAction(VindictaModel):
    """Base class for all actions."""

    # id, created_at inherited from VindictaModel
    action_type: ActionType

    # Timing
    turn: int = Field(..., ge=1, description="Turn number")
    phase: str = Field(..., description="Game phase (e.g., 'movement', 'shooting')")
    # timestamp inherited from VindictaModel (created_at) or specific game time? 
    # VindictaModel has created_at, but actions might have a specific in-game timestamp.
    # We'll keep a specific timestamp field if it represents game time, or map it.
    # WARScribe usually implies "when it happened in real time" which created_at covers.
    # But let's keep 'timestamp' for backward compat if needed, or map it.
    # For now, we'll rely on VindictaModel's created_at, but existing clients might expect 'timestamp'.
    # We can add a property or just keep it as a field if it differs.
    # Let's assume created_at is sufficient for "when recorded", but if we import old logs, we might need a specific field.
    # Re-adding timestamp field explicitly if it serves a distinct domain purpose (e.g. video timestamp).
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Actor
    actor: UnitReference = Field(..., description="The unit performing the action")

    # Result
    result: ActionResult = ActionResult.PENDING

    # Notes
    notes: Optional[str] = Field(None, description="Optional notes about the action")


class RelativeDistance(BaseModel):
    """Distance change relative to another unit.
    
    Sub-component, not a standalone entity, so BaseModel is fine, 
    but VindictaModel gives consistent config. Let's stick to BaseModel for lightweight struct.
    """

    target_unit_id: UUID = Field(..., description="ID of the reference unit")
    target_unit_name: Optional[str] = None
    delta_inches: float = Field(
        ..., description="Change in distance (negative = closer)"
    )
    final_distance: Optional[float] = Field(
        None, ge=0, description="Final distance to target"
    )


class MoveAction(BaseAction):
    """A movement action."""

    action_type: ActionType = ActionType.MOVE

    # Movement details (ALWAYS positive - actual distance moved)
    distance_inches: float = Field(
        ..., ge=0, description="Distance moved in inches (always positive)"
    )
    start_position: Optional[tuple[float, float]] = None
    end_position: Optional[tuple[float, float]] = None

    # Movement modifiers
    is_advance: bool = False
    is_fall_back: bool = False
    terrain_crossed: list[str] = Field(default_factory=list)

    # Relational distances (can be negative = moved closer)
    relative_distances: list[RelativeDistance] = Field(
        default_factory=list,
        description="Distance changes relative to other units (negative = closer)",
    )


class ShootAction(BaseAction):
    """A shooting action."""

    action_type: ActionType = ActionType.SHOOT

    # Target
    target: UnitReference = Field(..., description="Unit being shot at")

    # Weapon info
    weapon_name: str = Field(..., description="Weapon used")
    shots: int = Field(..., ge=1, description="Number of shots")

    # Dice results
    hits: int = Field(0, ge=0)
    wounds: int = Field(0, ge=0)
    saves_failed: int = Field(0, ge=0)
    damage_dealt: int = Field(0, ge=0)
    models_killed: int = Field(0, ge=0)


class ChargeAction(BaseAction):
    """A charge action."""

    action_type: ActionType = ActionType.CHARGE

    # Target(s)
    targets: list[UnitReference] = Field(
        ..., min_length=1, description="Charge targets"
    )

    # Dice
    charge_roll: tuple[int, int] = Field(..., description="2D6 charge roll")
    distance_needed: float = Field(..., ge=0, description="Distance to closest target")

    # Result
    made_charge: bool = False


class FightAction(BaseAction):
    """A fight (melee) action."""

    action_type: ActionType = ActionType.FIGHT

    # Target
    target: UnitReference = Field(..., description="Unit being fought")

    # Weapon info
    weapon_name: str = Field(..., description="Melee weapon used")
    attacks: int = Field(..., ge=1, description="Number of attacks")

    # Dice results
    hits: int = Field(0, ge=0)
    wounds: int = Field(0, ge=0)
    saves_failed: int = Field(0, ge=0)
    damage_dealt: int = Field(0, ge=0)
    models_killed: int = Field(0, ge=0)


# Union type for all actions
Action = Union[MoveAction, ShootAction, ChargeAction, FightAction]
```

## File: src/warscribe/core/schema/transcript.py
```python
"""
Game transcript model for WARScribe.

A transcript is a complete record of a game,
including all actions and metadata.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from warscribe.core.schema.action import Action
from warscribe.core.schema.unit import UnitReference
from vindicta_foundation.models.base import VindictaModel


class Player(BaseModel):
    """A player in a game."""

    name: str = Field(..., description="Player name")
    faction: str = Field(..., description="Faction played")
    subfaction: Optional[str] = Field(None, description="Subfaction/chapter")

    # Army list (simplified for v0.1.0)
    units: List[UnitReference] = Field(default_factory=list)
    points_total: int = Field(0, ge=0)


class GameTranscript(VindictaModel):
    """
    A complete game transcript.

    Records all actions in chronological order,
    along with game metadata and final results.
    """

    # id, created_at inherited from VindictaModel

    # Game metadata
    edition: str = Field("10th", description="Game edition (10th, 11th)")
    points_limit: int = Field(2000, description="Points limit for the game")
    mission: str = Field("unknown", description="Mission name")
    deployment: str = Field("unknown", description="Deployment type")

    # Players
    player1: Player
    player2: Player

    # Game state
    current_turn: int = Field(1, ge=1)
    active_player: int = Field(1, ge=1, le=2)

    # Actions (chronological)
    actions: list[Action] = Field(default_factory=list)

    # Scoring
    player1_vp: int = Field(0, ge=0)
    player2_vp: int = Field(0, ge=0)

    # Game result
    winner: Optional[int] = Field(
        None, ge=1, le=2, description="1 or 2, None if ongoing"
    )
    conceded: bool = Field(False, description="True if game ended by concession")

    # Timestamps
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    # Notes
    notes: Optional[str] = None

    def add_action(self, action: Action) -> None:
        """Add an action to the transcript."""
        self.actions.append(action)

    def get_actions_for_turn(self, turn: int) -> list[Action]:
        """Get all actions for a specific turn."""
        return [a for a in self.actions if a.turn == turn]

    def get_actions_by_unit(self, unit_id: UUID) -> list[Action]:
        """Get all actions by a specific unit."""
        return [a for a in self.actions if a.actor.id == unit_id]

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "GameTranscript":
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)
```

## File: src/warscribe/core/schema/unit.py
```python
"""
Unit reference model for WARScribe notation.

Provides a way to reference units on the battlefield
without duplicating full unit data.
"""

from typing import Optional

from pydantic import Field
from vindicta_foundation.models.base import VindictaModel


class UnitReference(VindictaModel):
    """
    A reference to a unit in a game.

    Used in actions to identify which unit is acting or being targeted.
    Can include optional extra context like remaining wounds/models.
    """

    # id is inherited from VindictaModel
    name: str = Field(..., description="Unit name (e.g., 'Intercessor Squad A')")
    faction: str = Field(..., description="Faction name")

    # Optional context (filled in when relevant)
    wounds_remaining: Optional[int] = Field(None, description="Current wounds")
    models_remaining: Optional[int] = Field(None, description="Current models")

    # Position (optional, for spatial tracking)
    position_x: Optional[float] = Field(None, description="X coordinate")
    position_y: Optional[float] = Field(None, description="Y coordinate")

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"{self.name} ({self.faction})"

    def short_ref(self) -> str:
        """Short reference string for compact notation."""
        return f"{self.name[:10]}..."[:12] if len(self.name) > 12 else self.name
```

## File: src/warscribe/integrity.py
```python
import datetime

def verify_integrity():
    """
    Performs a self-check of the Warscribe System domain.
    """
    return {
        "status": "operational",
        "timestamp": datetime.datetime.now().isoformat(),
        "metrics": {
            "scribe_status": "online",
            "active_ledgers": 0
        }
    }
```

## File: src/warscribe/parser/__init__.py
```python

```

## File: src/warscribe/parser/api.py
```python
"""
Warscribe API — FastAPI gateway for job submission, status, and RAG queries.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from redis import Redis
from rq import Queue

from db import Database
from query_engine import QueryEngine

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
DB_PATH = os.environ.get("DB_PATH", "warscribe.db")

app = FastAPI(title="Warscribe API", version="1.0.0")


def _get_queue():
    conn = Redis.from_url(REDIS_URL)
    return Queue("warscribe", connection=conn)


def _get_db():
    return Database(DB_PATH)


# ── Request / Response Models ──────────────────────────────

class JobRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    question: str
    video_id: Optional[str] = None

class IngestRequest(BaseModel):
    file_path: str
    source_id: Optional[str] = None


# ── Job Endpoints ──────────────────────────────────────────

@app.post("/jobs", status_code=201)
def submit_job(req: JobRequest):
    """Submit a YouTube URL for processing."""
    from worker import task_download

    q = _get_queue()
    rq_job = q.enqueue(task_download, req.url, job_timeout="6h")
    return {"message": "Job enqueued", "rq_job_id": rq_job.id, "url": req.url}


@app.get("/jobs")
def list_jobs():
    """List all warscribe processing jobs."""
    db = _get_db()
    return db.list_jobs()


@app.get("/jobs/{video_id}")
def get_job(video_id: str):
    """Get status of a specific job."""
    db = _get_db()
    job = db.get_job(video_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# ── RAG Query Endpoints ───────────────────────────────────

@app.post("/query")
def rag_query(req: QueryRequest):
    """Query the RAG system with a natural language question."""
    engine = QueryEngine(db_path=DB_PATH)
    answer = engine.query(req.question, video_id=req.video_id)
    return {"question": req.question, "answer": answer, "video_id": req.video_id}


# ── Ingestion Endpoint ────────────────────────────────────

@app.post("/ingest")
def ingest_file(req: IngestRequest):
    """Ingest a text file from the input volume into ChromaDB."""
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {req.file_path}")

    from ingest_text import ingest_text_file
    source_id = req.source_id or os.path.basename(req.file_path)
    count = ingest_text_file(req.file_path, source_id=source_id, db_path=DB_PATH)
    return {"message": f"Ingested {count} chunks", "source_id": source_id}


# ── Health ─────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check endpoint."""
    try:
        conn = Redis.from_url(REDIS_URL)
        conn.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    return {"status": "ok", "redis": redis_ok}
```

## File: src/warscribe/parser/chat_parser.py
```python
from warscribe.core.schema.action import Action, ActionType, ActionResult, BaseAction
from warscribe.core.schema.transcript import GameTranscript, Player
from warscribe.core.schema.unit import UnitReference
from chat_downloader import ChatDownloader
from db import Database
import time

class ChatParser:
    def __init__(self, db_path="warscribe.db"):
        self.db_path = db_path

    def process_chat(self, video_id):
        print(f"Processing chat for {video_id} using ChatDownloader...")
        db = Database(self.db_path)
        url = db.get_job_url(video_id)
        if not url:
            print(f"No URL found for job {video_id}")
            return

        print(f"Fetching chat from {url}...")
        try:
            downloader = ChatDownloader()
            chat = downloader.get_chat(url) # Returns a generator
            
            messages = []
            count = 0
            for message in chat:
                # ChatDownloader returns dicts with various fields.
                # We need: video_id, timestamp (sec), author, message
                
                ts = message.get('time_in_seconds', 0)
                author = message.get('author', {}).get('name', 'Anonymous')
                text = message.get('message', '')
                
                if text:
                    messages.append((video_id, float(ts), author, text))
                    count += 1
                    
                if len(messages) >= 100: # Batch insert
                     db.add_chat_messages(messages)
                     messages = []
                     
            if messages:
                db.add_chat_messages(messages)
                
            print(f"Finished processing chat. Total {count} messages.")
            
        except Exception as e:
            print(f"Error downloading chat: {e}")

if __name__ == "__main__":
    import sys
    # Usage: python src/chat_parser.py <video_id>
    if len(sys.argv) > 1:
        cp = ChatParser()
        cp.process_chat(sys.argv[1])
```

## File: src/warscribe/parser/db.py
```python
import sqlite3
import os
import chromadb
from chromadb.utils import embedding_functions


class Database:
    def __init__(self, db_path="warscribe.db", chroma_path=None):
        self.db_path = db_path
        self._init_db()
        chroma_dir = chroma_path or os.environ.get("CHROMA_PATH", "warscribe_chroma")
        try:
            self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            self.collection = self.chroma_client.get_or_create_collection(name="transcripts", embedding_function=self.embedding_fn)
        except Exception as e:
            print(f"Warning: ChromaDB initialization failed: {e}")
            self.chroma_client = None

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Enable WAL mode for concurrent read access
        c.execute("PRAGMA journal_mode=WAL")
        
        # Jobs table: tracks the overall video processing
        c.execute('''CREATE TABLE IF NOT EXISTS jobs (
            video_id TEXT PRIMARY KEY,
            url TEXT,
            status TEXT, -- 'pending', 'downloading', 'processing', 'completed', 'failed'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Segments table: tracks chunks of the video
        c.execute('''CREATE TABLE IF NOT EXISTS segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            segment_index INTEGER,
            start_time REAL,
            end_time REAL,
            audio_path TEXT,
            transcript TEXT,
            chat_data TEXT,
            warscribe_json TEXT,
            status TEXT, -- 'created', 'transcribed', 'analyzed'
            FOREIGN KEY(video_id) REFERENCES jobs(video_id)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            timestamp REAL,
            author TEXT,
            message TEXT,
            FOREIGN KEY(video_id) REFERENCES jobs(video_id)
        )''')
        
        c.execute("CREATE INDEX IF NOT EXISTS idx_chat_timestamp ON chat_messages(video_id, timestamp)")
        
        conn.commit()
        conn.close()

    def add_job(self, video_id, url):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO jobs (video_id, url, status) VALUES (?, ?, ?)", 
                  (video_id, url, 'pending'))
        conn.commit()
        conn.close()

    def update_job_status(self, video_id, status):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE video_id = ?", 
                  (status, video_id))
        conn.commit()
        conn.close()

    def add_segment(self, video_id, start_time, end_time, audio_path):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO segments (video_id, start_time, end_time, audio_path, status)
                     VALUES (?, ?, ?, ?, ?)''',
                  (video_id, start_time, end_time, audio_path, 'created'))
        segment_id = c.lastrowid
        conn.commit()
        conn.close()
        return segment_id

    def get_segments(self, video_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM segments WHERE video_id = ? ORDER BY start_time", (video_id,))
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def add_chat_messages(self, messages):
        """messages: list of (video_id, timestamp, author, message)"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.executemany("INSERT INTO chat_messages (video_id, timestamp, author, message) VALUES (?, ?, ?, ?)", 
                      messages)
        conn.commit()
        conn.close()
    
    def get_chat_for_segment(self, video_id, start_time, end_time):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM chat_messages WHERE video_id = ? AND timestamp >= ? AND timestamp < ? ORDER BY timestamp", 
                  (video_id, start_time, end_time))
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_job_url(self, video_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT url FROM jobs WHERE video_id = ?", (video_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def get_job_status(self, video_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT status FROM jobs WHERE video_id = ?", (video_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def update_segment_transcript(self, segment_id, transcript):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE segments SET transcript = ?, status = 'transcribed' WHERE id = ?",
                  (transcript, segment_id))
        conn.commit()
        conn.close()

    def update_segment_warscribe(self, segment_id, warscribe_json):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE segments SET warscribe_json = ?, status = 'analyzed' WHERE id = ?",
                  (warscribe_json, segment_id))
        conn.commit()
        conn.close()

    def list_jobs(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM jobs ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_pending_jobs(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM jobs WHERE status = 'pending' ORDER BY created_at ASC")
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_job(self, video_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM jobs WHERE video_id = ?", (video_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None

    def _batch_add(self, ids, documents, metadatas, batch_size=1000):
        total = len(ids)
        for i in range(0, total, batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            try:
                self.collection.add(ids=batch_ids, documents=batch_docs, metadatas=batch_meta)
                print(f"Added batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size} ({len(batch_ids)} docs)")
            except Exception as e:
                print(f"Error adding batch {i//batch_size + 1}: {e}")

    def add_transcript_embeddings(self, video_id, segments):
        if not self.chroma_client:
            print("ChromaDB not initialized, skipping embeddings.")
            return

        if not segments:
            return

        ids = []
        documents = []
        metadatas = []

        for i, seg in enumerate(segments):
            # seg is expected to be a dict from get_segments
            text = seg.get('transcript', '')
            if text and text.strip():
                ids.append(f"{video_id}_{i}")
                documents.append(text)
                metadatas.append({
                    "video_id": video_id, 
                    "start": seg['start_time'], 
                    "end": seg['end_time'],
                    "source": "transcript"
                })
        
        if documents:
            self._batch_add(ids, documents, metadatas)
            print(f"Finished adding {len(documents)} embeddings to ChromaDB.")

    def add_documents(self, source_id, documents, metadatas):
        """
        Generic method to add documents to ChromaDB.
        source_id: unique identifier for the source (e.g. filename)
        documents: list of text strings
        metadatas: list of dicts. If 'source' key is missing, it will be added.
        """
        if not self.chroma_client:
            print("ChromaDB not initialized.")
            return

        if not documents:
            return

        ids = [f"{source_id}_{i}" for i in range(len(documents))]
        
        # Ensure metadata has 'source'
        final_metadatas = []
        for m in metadatas:
            new_m = m.copy()
            if 'source' not in new_m:
                new_m['source'] = source_id
            final_metadatas.append(new_m)

        self._batch_add(ids, documents, final_metadatas)
        print(f"Finished adding {len(documents)} documents from {source_id}")
```

## File: src/warscribe/parser/downloader.py
```python
import os
import subprocess
from db import Database
from utils import find_audio

class Downloader:
    def __init__(self, output_dir="input", db_path="warscribe.db"):
        self.output_dir = output_dir
        self.db_path = db_path
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_video_id(self, url):
        """Extracts video ID from URL using yt-dlp."""
        cmd = ["yt-dlp", "--print", "id", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to get video ID: {result.stderr}")
        return result.stdout.strip()

    def _has_ffmpeg(self):
        """Check if ffmpeg is available on the system."""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def download_audio(self, url, video_id):
        """Downloads audio. Strategy depends on ffmpeg availability."""
        output_template = os.path.join(self.output_dir, f"{video_id}.%(ext)s")
        
        if self._has_ffmpeg():
            # Ideal: extract audio and convert to wav
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format", "wav",
                "--audio-quality", "0",
                "-o", output_template,
                url
            ]
        else:
            # No ffmpeg: download best format directly, no post-processing
            # Use broad format selection that works for both VODs and live streams
            cmd = [
                "yt-dlp",
                "-f", "bestaudio/best",  # bestaudio if separate, else best combined
                "-o", output_template,
                url
            ]
        
        print(f"Downloading audio for {video_id}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Primary download failed: {result.stderr.strip()}")
            print("Retrying with fallback format selection...")
            # Ultimate fallback: just download whatever is available
            cmd_fallback = [
                "yt-dlp",
                "-f", "best",
                "-o", output_template,
                url
            ]
            subprocess.run(cmd_fallback, check=True)
        
        return find_audio(self.output_dir, video_id)

    def process(self, url):
        video_id = self.get_video_id(url)
        print(f"Processing {video_id}...")
        
        # Register job
        db = Database(self.db_path)
        db.add_job(video_id, url)
        db.update_job_status(video_id, 'downloading')
        
        try:
            audio_path = self.download_audio(url, video_id)
            if audio_path:
                print(f"Audio saved: {audio_path}")
                db.update_job_status(video_id, 'downloaded')
            else:
                raise FileNotFoundError(f"No audio file found for {video_id}")
        except Exception as e:
            print(f"Download error: {e}")
            # Check if audio already exists from a prior run
            existing = find_audio(self.output_dir, video_id)
            if existing:
                print(f"Found existing audio: {existing}. Continuing...")
                db.update_job_status(video_id, 'downloaded')
            else:
                db.update_job_status(video_id, 'failed')
        
        return video_id

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        d = Downloader("warscribe-system/input")
        d.process(sys.argv[1])
```

## File: src/warscribe/parser/ingest_text.py
```python
import sys
import os
import argparse
from db import Database

def ingest_text_file(file_path, source_id=None, db_path="warscribe.db"):
    """Ingest a text file into ChromaDB. Returns number of chunks ingested."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
    
    if not chunks:
        print("No content found in file.")
        return 0

    db = Database(db_path)
    filename = os.path.basename(file_path)
    sid = source_id or filename.replace(" ", "_")

    print(f"Ingesting {len(chunks)} chunks from {filename}...")
    
    documents = chunks
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
    
    db.add_documents(sid, documents, metadatas)
    print("Done.")
    return len(chunks)


def ingest_file(file_path):
    """CLI wrapper for backward compatibility."""
    ingest_text_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a text file into Warscribe RAG")
    parser.add_argument("file", help="Path to text file")
    args = parser.parse_args()
    
    ingest_file(args.file)
```

## File: src/warscribe/parser/orchestrator.py
```python
import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from db import Database
from downloader import Downloader
from transcriber import Transcriber
from chat_parser import ChatParser
from warscribe_llm import WarscribeLLM

class Orchestrator:
    def __init__(self, db_path="warscribe.db"):
        self.db = Database(db_path)
        self.downloader = Downloader("input", db_path=db_path)
        self.transcriber = Transcriber(model_size="tiny", device="cpu", db_path=db_path, input_dir="input")
        self.chat_parser = ChatParser(db_path=db_path)
        self.warscribe_llm = WarscribeLLM(db_path=db_path)
    
    def add_job(self, url):
        # Step 1: Download audio
        print("Starting download phase...")
        video_id = self.downloader.process(url)
        
        # Step 2: Parse live chat (independent of download success)
        print("Starting chat parsing...")
        try:
            self.chat_parser.process_chat(video_id)
        except Exception as e:
            print(f"Chat parsing failed (non-fatal): {e}")
        
        # Step 3: Transcribe audio
        print("Starting transcription...")
        self.transcriber.process_job(video_id)
        
        # Step 4: Extract Warscribe events via LLM
        print("Starting Warscribe extraction...")
        self.warscribe_llm.process_job(video_id)
        
        # Step 5: Generate embeddings for RAG
        print("Generating Embeddings...")
        segments = self.db.get_segments(video_id)
        self.db.add_transcript_embeddings(video_id, segments)
        
        print(f"Job finished for {video_id}")

    def run_loop(self):
        # Placeholder for daemon mode
        while True:
            # check pending jobs
            # check processing jobs
            time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        orch = Orchestrator()
        orch.add_job(sys.argv[1])
```

## File: src/warscribe/parser/query_engine.py
```python
import chromadb
from chromadb.utils import embedding_functions
from db import Database
import ollama

class QueryEngine:
    def __init__(self, db_path="warscribe.db", chroma_path="warscribe_chroma", llm_model="llama3.2"):
        self.db = Database(db_path)
        self.llm_model = llm_model
        
        try:
            self.chroma_client = chromadb.PersistentClient(path=chroma_path)
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            self.collection = self.chroma_client.get_collection(name="transcripts", embedding_function=self.embedding_fn)
        except Exception as e:
            print(f"Error initializing ChromaDB for QueryEngine: {e}")
            self.collection = None

    def retrieve(self, query, n_results=5, video_id=None):
        if not self.collection:
            return []
            
        where = None
        if video_id:
            where = {"video_id": video_id}
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        # results['documents'] is list of list (batch)
        if results and results['documents']:
            return results['documents'][0]
        return []

    def query(self, question, video_id=None):
        print(f"Retrieving context for: '{question}'...")
        context_docs = self.retrieve(question, n_results=5, video_id=video_id)
        
        if not context_docs:
            return "No relevant context found in the database."
            
        context_text = "\n\n---\n\n".join(context_docs)
        
        prompt = f"""
You are Warscribe, an AI assistant analyzing YouTube video transcripts.
Answer the user's question based ONLY on the following context.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context_text}

Question: {question}

Answer:
"""
        try:
            print("Querying Ollama...")
            response = ollama.chat(model=self.llm_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

if __name__ == "__main__":
    import sys
    engine = QueryEngine()
    
    if len(sys.argv) > 1:
        question = sys.argv[1]
        video_id = sys.argv[2] if len(sys.argv) > 2 else None
        
        print("\n--- Warscribe RAG Query ---")
        answer = engine.query(question, video_id)
        print("\n=== Answer ===\n")
        print(answer)
        print("\n==============")
    else:
        print("Usage: python src/query_engine.py \"Your question here\" [optional_video_id]")
```

## File: src/warscribe/parser/retry_embeddings.py
```python
import sys
from db import Database

def retry_embeddings(video_id):
    db = Database()
    segments = db.get_segments(video_id)
    
    if not segments:
        print(f"No segments found for {video_id}. Transcription might have failed.")
        return

    print(f"Found {len(segments)} segments. Generating embeddings...")
    db.add_transcript_embeddings(video_id, segments)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        retry_embeddings(sys.argv[1])
    else:
        print("Usage: python src/retry_embeddings.py <video_id>")
```

## File: src/warscribe/parser/transcriber.py
```python
import os
from faster_whisper import WhisperModel
from db import Database
from utils import find_audio

class Transcriber:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8", db_path="warscribe.db", input_dir="input"):
        self.db_path = db_path
        self.input_dir = input_dir
        print(f"Loading Whisper model: {model_size} on {device}...")
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception as e:
            print(f"Failed to load model on {device}: {e}. Falling back to cpu.")
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def process_job(self, video_id):
        print(f"Processing transcription for job: {video_id}")
        db = Database(self.db_path)
        job_status = self._get_job_status(db, video_id)
        
        if job_status not in ['downloaded', 'transcribing']:
            print(f"Job {video_id} is in status '{job_status}'. Skipping.")
            return

        db.update_job_status(video_id, 'transcribing')
        
        audio_path = find_audio(self.input_dir, video_id)
        if not audio_path:
            print(f"Audio file not found for {video_id} in {self.input_dir}")
            db.update_job_status(video_id, 'failed')
            return
        
        print(f"Using audio file: {audio_path}")

        # Resume from last processed segment if any exist
        existing_segments = db.get_segments(video_id)
        last_end_time = 0.0
        if existing_segments:
            last_end_time = existing_segments[-1]['end_time']
            print(f"Resuming transcription from {last_end_time}s")

        try:
             segments, info = self.model.transcribe(audio_path, beam_size=5)
             
             print("Starting transcription loop...")
             for segment in segments:
                 if segment.end <= last_end_time:
                     continue  # skip already-processed segments

                 seg_id = db.add_segment(
                     video_id, segment.start, segment.end, audio_path
                 )
                 db.update_segment_transcript(seg_id, segment.text)
                 print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

             db.update_job_status(video_id, 'transcribed')
             
        except Exception as e:
            print(f"Transcription failed: {e}")
            db.update_job_status(video_id, 'failed')

    def _get_job_status(self, db, video_id):
        return db.get_job_status(video_id)

if __name__ == "__main__":
    import sys
    t = Transcriber()
    if len(sys.argv) > 1:
        t.process_job(sys.argv[1])
```

## File: src/warscribe/parser/utils.py
```python
"""Shared utility functions for the Warscribe system."""

import os
import glob


def find_audio(input_dir, video_id):
    """Find audio file for a video_id regardless of extension.
    
    Searches the input directory for common audio/video extensions,
    falling back to a glob pattern match.
    
    Returns the path if found, else None.
    """
    for ext in ['wav', 'm4a', 'webm', 'opus', 'mp3', 'ogg', 'mp4', 'mkv']:
        path = os.path.join(input_dir, f"{video_id}.{ext}")
        if os.path.exists(path):
            return path
    # Last resort: glob
    pattern = os.path.join(input_dir, f"{video_id}.*")
    matches = [f for f in glob.glob(pattern) if not f.endswith('.json')]
    return matches[0] if matches else None
```

## File: src/warscribe/parser/warscribe_llm.py
```python
import json
from db import Database
import ollama

class WarscribeLLM:
    def __init__(self, model="llama3", db_path="warscribe.db"):
        self.model = model
        self.db_path = db_path

    def process_job(self, video_id):
        print(f"Processing Warscribe extraction for {video_id}...")
        db = Database(self.db_path)
        
        segments = db.get_segments(video_id)
        
        for segment in segments:
            if segment['transcript'] and not segment['warscribe_json']:
                # Need processing
                print(f"Analyzing segment {segment['id']} ({segment['start_time']}-{segment['end_time']})...")
                
                chat_msgs = db.get_chat_for_segment(video_id, segment['start_time'], segment['end_time'])
                chat_text = "\n".join([f"{m['author']}: {m['message']}" for m in chat_msgs])
                
                prompt = self._create_prompt(segment['transcript'], chat_text)
                
                try:
                    response = ollama.chat(model=self.model, messages=[
                        {'role': 'user', 'content': prompt},
                    ])
                    content = response['message']['content']
                    
                    # Try to extract JSON
                    # Validating JSON is tricky with LLMs, usually need strict mode or parsing.
                    # We'll assume the LLM follows instructions or we wrap in try/catch.
                    
                    warscribe_data = content
                    db.update_segment_warscribe(segment['id'], warscribe_data)
                    
                except Exception as e:
                    print(f"LLM failed for segment {segment['id']}: {e}")

    def _create_prompt(self, transcript, chat_text):
        return f"""
Analyze the following YouTube Live Stream segment (Transcript and Chat) and extract "Warscribe" events.
Output strictly valid JSON.

Transcript:
{transcript}

Chat:
{chat_text}

Extract significant events, sentiment, and topics.
JSON Format:
{{
  "events": [
    {{ "type": "topic_change", "description": "...", "timestamp": ... }},
    {{ "type": "highlight", "description": "...", "timestamp": ... }}
  ],
  "summary": "..."
}}
"""

if __name__ == "__main__":
    import sys
    llm = WarscribeLLM()
    if len(sys.argv) > 1:
        llm.process_job(sys.argv[1])
```

## File: src/warscribe/parser/worker.py
```python
"""
Warscribe Worker — RQ task functions for the processing pipeline.
Each task completes one phase and enqueues the next.
"""
import os
import sys

# Ensure src/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from redis import Redis
from rq import Queue

from db import Database
from downloader import Downloader
from transcriber import Transcriber
from chat_parser import ChatParser
from warscribe_llm import WarscribeLLM

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
DB_PATH = os.environ.get("DB_PATH", "warscribe.db")
INPUT_DIR = os.environ.get("INPUT_DIR", "input")

def _get_queue():
    conn = Redis.from_url(REDIS_URL)
    return Queue("warscribe", connection=conn)


def task_download(url: str):
    """Phase 1: Download audio and parse chat."""
    print(f"[WORKER] Starting download for {url}")
    db = Database(DB_PATH)
    downloader = Downloader(INPUT_DIR, db_path=DB_PATH)
    video_id = downloader.process(url)

    # Chat parsing (non-fatal)
    try:
        parser = ChatParser(db_path=DB_PATH)
        parser.process_chat(video_id)
    except Exception as e:
        print(f"[WORKER] Chat parsing failed (non-fatal): {e}")

    # Enqueue next step
    job_status = db.get_job_status(video_id)
    if job_status != "failed":
        q = _get_queue()
        q.enqueue(task_transcribe, video_id, job_timeout="12h")
        print(f"[WORKER] Enqueued transcription for {video_id}")
    else:
        print(f"[WORKER] Download failed for {video_id}, not enqueuing transcription")

    return video_id


def task_transcribe(video_id: str):
    """Phase 2: Transcribe audio with faster-whisper."""
    print(f"[WORKER] Starting transcription for {video_id}")
    model_size = os.environ.get("WHISPER_MODEL", "tiny")
    device = os.environ.get("WHISPER_DEVICE", "cpu")

    transcriber = Transcriber(
        model_size=model_size,
        device=device,
        db_path=DB_PATH,
        input_dir=INPUT_DIR,
    )
    transcriber.process_job(video_id)

    # Enqueue next step
    db = Database(DB_PATH)
    job_status = db.get_job_status(video_id)
    if job_status == "transcribed":
        q = _get_queue()
        q.enqueue(task_llm_embed, video_id, job_timeout="6h")
        print(f"[WORKER] Enqueued LLM+embed for {video_id}")
    else:
        print(f"[WORKER] Transcription ended with status '{job_status}', not enqueuing LLM")

    return video_id


def task_llm_embed(video_id: str):
    """Phase 3: LLM analysis + embedding generation."""
    print(f"[WORKER] Starting LLM analysis for {video_id}")
    db = Database(DB_PATH)

    # LLM warscribe extraction
    llm = WarscribeLLM(db_path=DB_PATH)
    llm.process_job(video_id)

    # Generate embeddings
    print(f"[WORKER] Generating embeddings for {video_id}")
    segments = db.get_segments(video_id)
    db.add_transcript_embeddings(video_id, segments)

    db.update_job_status(video_id, "completed")
    print(f"[WORKER] Job completed for {video_id}")
    return video_id
```

## File: tests/test_scribe.py
```python
import pytest
from uuid import UUID
from datetime import datetime
from warscribe.core.schema.unit import UnitReference
from warscribe.core.schema.action import BaseAction, ActionType
from warscribe.core.schema.transcript import GameTranscript, Player
from vindicta_foundation.models.base import VindictaModel

def test_unit_reference_model():
    unit = UnitReference(name="Intercessors", faction="Space Marines")
    assert isinstance(unit, VindictaModel)
    assert unit.name == "Intercessors"
    assert isinstance(unit.id, UUID)

def test_base_action_model():
    unit = UnitReference(name="Intercessors", faction="Space Marines")
    action = BaseAction(
        action_type=ActionType.MOVE,
        turn=1,
        phase="Movement",
        actor=unit
    )
    assert isinstance(action, VindictaModel)
    assert action.turn == 1
    assert action.actor.name == "Intercessors"

def test_transcript_model():
    p1 = Player(name="Alice", faction="Ultramarines")
    p2 = Player(name="Bob", faction="Necrons")
    
    transcript = GameTranscript(
        player1=p1,
        player2=p2,
        current_turn=1
    )
    
    assert isinstance(transcript, VindictaModel)
    assert transcript.player1.name == "Alice"
    assert transcript.created_at is not None
```

## File: .specify/templates/spec-template.md
```markdown
# [Feature Name]`n`n## User Stories`n- [ ] US1: ...`n`n## Requirements`n- R1: ...`n`n## Acceptance Criteria`n- [ ] AC1: ...
```

## File: .specify/templates/tasks-template.md
```markdown
# Tasks - [Feature Name]`n`n- [ ] T001 Description`n- [ ] T002 Description
```

## File: .specify/memory/constitution.md
```markdown
# WARScribe System Constitution

## Core Principles

### I. MCP-First Mandate...

### II. Spec-Driven Development (SDD)...

### III. Zero-Issue Stability...

### IV. Tech Standards...

### V. Domain Isolation...
```

## File: .specify/templates/plan-template.md
```markdown
# Implementation Plan - [Feature Name]`n`n## Technical Context`n...`n`n## Proposed Changes`n...`n`n## Verification Plan`n...
```
