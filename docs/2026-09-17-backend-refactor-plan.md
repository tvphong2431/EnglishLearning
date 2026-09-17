# Backend Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the current FastAPI backend into a clear layer-based architecture, remove `/process`, keep session storage in RAM, and preserve current behavior for session creation and answer checking.

**Architecture:** Keep the existing layers `api`, `schemas`, `services`, `models`, `adapters`, and `config`. HTTP handling stays in `api`, Pydantic request/response types stay in `schemas`, business orchestration moves into `services`, internal data objects stay in `models`, and external-library integration stays in `adapters`.

**Tech Stack:** Python 3.11, FastAPI, Pydantic, pytest, yt-dlp, openai-whisper, youtube-transcript-api.

**Spec:** `docs/superpowers/specs/2026-09-17-backend-refactor-design.md`

## Global Constraints

- Remove `/process` completely.
- `POST /sessions` becomes the only entry point for creating a dictation session.
- `POST /sessions/{session_id}/check` checks an answer.
- Sessions remain stored in RAM for now.
- Do not add a database or repository layer in this refactor.
- Do not add answer normalization, Show Answer, forced alignment, or Whisper optimizations.
- Do not change audio-download or transcript-generation behavior.
- `Sentence.text` must never be included in the session-create API response.
- All remaining relevant tests must pass after the refactor.

---

### Task 1: Introduce an internal `Session` model

**Files:**
- Create: `app/models/session.py`
- Modify: `app/services/session_service.py`
- Modify: `tests/unit/test_session_service.py`

**Interfaces:**
- Consumes: `Sentence` from `app.models.transcript`
- Produces: `Session(video_id: str, sentences: list[Sentence])`
- Produces: `sessions: dict[str, Session]`
- Produces: `create_session(video_id: str, sentences: list[Sentence]) -> str`
- Produces: `get_session(session_id: str) -> Session | None`

- [ ] **Step 1: Change the unit test so it expects `Session` instead of a raw dict**

```python
from app.models.session import Session


def test_create_session():
    sessions.clear()

    sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    session_id = create_session(
        video_id="abc123",
        sentences=sentences,
    )

    session = get_session(session_id)

    assert isinstance(session_id, str)
    assert isinstance(session, Session)
    assert session.video_id == "abc123"
    assert session.sentences == sentences
```

Keep the existing missing-session test:

```python
def test_get_session_returns_none_when_not_found():
    sessions.clear()

    result = get_session("not-exist")

    assert result is None
```

- [ ] **Step 2: Run the test and verify the new expectation fails**

Run:

```powershell
python -m pytest tests/unit/test_session_service.py -v
```

Expected: the create-session test fails because the service still stores/returns a raw `dict`.

- [ ] **Step 3: Add the internal model**

Create `app/models/session.py`:

```python
from dataclasses import dataclass

from app.models.transcript import Sentence


@dataclass
class Session:
    video_id: str
    sentences: list[Sentence]
```

- [ ] **Step 4: Refactor the RAM store to use `Session`**

Update `app/services/session_service.py`:

```python
from uuid import uuid4

from app.models.session import Session
from app.models.transcript import Sentence


sessions: dict[str, Session] = {}


def create_session(
    video_id: str,
    sentences: list[Sentence],
) -> str:
    session_id = str(uuid4())

    sessions[session_id] = Session(
        video_id=video_id,
        sentences=sentences,
    )

    return session_id


def get_session(session_id: str) -> Session | None:
    return sessions.get(session_id)
```

- [ ] **Step 5: Run the unit test and verify it passes**

```powershell
python -m pytest tests/unit/test_session_service.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add app/models/session.py app/services/session_service.py tests/unit/test_session_service.py
git commit -m "refactor: add internal session model"
```

---

### Task 2: Move session orchestration into `session_service`

**Files:**
- Modify: `app/services/session_service.py`
- Modify: `tests/unit/test_session_service.py`

**Interfaces:**
- Consumes: `extract_youtube_video_id(url: str) -> str`
- Consumes: `build_sentences(video_id: str) -> list[Sentence]`
- Produces: `create_dictation_session(youtube_url: str) -> tuple[str, Session]`
- Produces: `check_answer(session_id: str, sentence_id: int, answer: str) -> bool`

- [ ] **Step 1: Add a failing test for `create_dictation_session`**

Add to `tests/unit/test_session_service.py`:

```python
@pytest.mark.unit
def test_create_dictation_session(monkeypatch):
    sessions.clear()

    fake_sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    monkeypatch.setattr(
        "app.services.session_service.extract_youtube_video_id",
        lambda url: "abc123",
    )

    monkeypatch.setattr(
        "app.services.session_service.build_sentences",
        lambda video_id: fake_sentences,
    )

    session_id, session = create_dictation_session(
        "https://www.youtube.com/watch?v=abc123"
    )

    assert isinstance(session_id, str)
    assert session.video_id == "abc123"
    assert session.sentences == fake_sentences
    assert get_session(session_id) == session
```

- [ ] **Step 2: Run only this test and verify it fails because the function does not exist**

```powershell
python -m pytest tests/unit/test_session_service.py::test_create_dictation_session -v
```

Expected: FAIL because `create_dictation_session` is missing.

- [ ] **Step 3: Add the minimal orchestration function**

In `app/services/session_service.py`, import:

```python
from app.services.transcript_service import build_sentences
from app.services.youtube_service import extract_youtube_video_id
```

Add:

```python
def create_dictation_session(youtube_url: str) -> tuple[str, Session]:
    video_id = extract_youtube_video_id(youtube_url)
    sentences = build_sentences(video_id)

    session_id = create_session(
        video_id=video_id,
        sentences=sentences,
    )

    session = get_session(session_id)

    return session_id, session
```

Because the session was just created, `session` is expected to be a `Session` object in this flow.

- [ ] **Step 4: Run the create-dictation-session test and verify it passes**

```powershell
python -m pytest tests/unit/test_session_service.py::test_create_dictation_session -v
```

Expected: PASS.

- [ ] **Step 5: Add a failing test for `check_answer`**

```python
@pytest.mark.unit
def test_check_answer_returns_true_for_matching_answer():
    sessions.clear()

    sentences = [
        Sentence(
            text="You ready?",
            start=10.26,
            duration=0.44,
            word_count=2,
        )
    ]

    session_id = create_session("abc123", sentences)

    result = check_answer(
        session_id=session_id,
        sentence_id=0,
        answer="You ready?",
    )

    assert result is True
```

- [ ] **Step 6: Run the test and verify it fails because `check_answer` does not exist**

```powershell
python -m pytest tests/unit/test_session_service.py::test_check_answer_returns_true_for_matching_answer -v
```

Expected: FAIL.

- [ ] **Step 7: Add the minimal `check_answer` implementation**

```python
def check_answer(
    session_id: str,
    sentence_id: int,
    answer: str,
) -> bool:
    session = get_session(session_id)
    sentence = session.sentences[sentence_id]

    return answer == sentence.text
```

Do not add normalization in this refactor.

- [ ] **Step 8: Run the session-service unit tests**

```powershell
python -m pytest tests/unit/test_session_service.py -v
```

Expected: PASS.

- [ ] **Step 9: Commit**

```powershell
git add app/services/session_service.py tests/unit/test_session_service.py
git commit -m "refactor: move session orchestration into service"
```

---

### Task 3: Make `api/session.py` a thin HTTP layer

**Files:**
- Modify: `app/api/session.py`
- Modify: `app/main.py`
- Modify: `tests/integration/test_session_endpoint.py`
- Use: `app/schemas/session.py`

**Interfaces:**
- Consumes: `create_dictation_session(youtube_url: str) -> tuple[str, Session]`
- Consumes: `check_answer(session_id: str, sentence_id: int, answer: str) -> bool`
- Produces: `POST /sessions`
- Produces: `POST /sessions/{session_id}/check`

- [ ] **Step 1: Update the session-create integration test so it patches the service boundary**

Use the existing `TestClient` setup, but patch `session_service.create_dictation_session` instead of patching `transcript_service.build_sentences` from the API layer:

```python
@pytest.mark.integration
def test_create_session_endpoint(monkeypatch):
    sessions.clear()

    fake_session = Session(
        video_id="uVGV8LG3HHM",
        sentences=[
            Sentence(
                text="You ready?",
                start=10.26,
                duration=0.44,
                word_count=2,
            )
        ],
    )

    monkeypatch.setattr(
        "app.api.session.session_service.create_dictation_session",
        lambda youtube_url: ("session-123", fake_session),
    )

    request_body = {
        "youtube_url": "https://www.youtube.com/watch?v=uVGV8LG3HHM"
    }

    response = client.post(
        "/sessions",
        json=request_body,
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body == {
        "session_id": "session-123",
        "video_id": "uVGV8LG3HHM",
        "sentences": [
            {
                "id": 0,
                "start": 10.26,
                "duration": 0.44,
                "word_count": 2,
            }
        ],
    }

    assert "text" not in response_body["sentences"][0]
```

- [ ] **Step 2: Update the `/check` integration test so the API delegates to the service**

```python
@pytest.mark.integration
def test_check_answer_returns_true_when_correct(monkeypatch):
    monkeypatch.setattr(
        "app.api.session.session_service.check_answer",
        lambda session_id, sentence_id, answer: True,
    )

    request_body = {
        "sentence_id": 0,
        "answer": "You ready?",
    }

    response = client.post(
        "/sessions/session-123/check",
        json=request_body,
    )

    assert response.status_code == 200
    assert response.json() == {
        "correct": True,
    }
```

- [ ] **Step 3: Run the API tests and verify they fail against the old endpoint structure**

```powershell
python -m pytest tests/integration/test_session_endpoint.py -v
```

Expected: at least one test FAILS because the API still performs orchestration itself or the router is not wired in the intended place.

- [ ] **Step 4: Refactor `app/api/session.py`**

Use:

```python
from fastapi import APIRouter

from app.schemas.session import (
    CheckAnswerRequest,
    CheckAnswerResponse,
    CreateSessionRequest,
    CreateSessionResponse,
    SentenceInfo,
)
from app.services import session_service


router = APIRouter()


@router.post(
    "/sessions",
    response_model=CreateSessionResponse,
)
def create_dictation_session(request: CreateSessionRequest):
    session_id, session = session_service.create_dictation_session(
        request.youtube_url
    )

    sentence_infos = []

    for index, sentence in enumerate(session.sentences):
        sentence_infos.append(
            SentenceInfo(
                id=index,
                start=sentence.start,
                duration=sentence.duration,
                word_count=sentence.word_count,
            )
        )

    return CreateSessionResponse(
        session_id=session_id,
        video_id=session.video_id,
        sentences=sentence_infos,
    )


@router.post(
    "/sessions/{session_id}/check",
    response_model=CheckAnswerResponse,
)
def check_answer(
    session_id: str,
    request: CheckAnswerRequest,
):
    correct = session_service.check_answer(
        session_id=session_id,
        sentence_id=request.sentence_id,
        answer=request.answer,
    )

    return CheckAnswerResponse(
        correct=correct,
    )
```

- [ ] **Step 5: Make `main.py` only assemble the app**

Ensure `app/main.py` imports and includes the router:

```python
from fastapi import FastAPI

from app.api.session import router as session_router


app = FastAPI()

app.include_router(session_router)
```

Preserve the existing AppError handler registration already present in `main.py`; do not move or redesign it in this task.

- [ ] **Step 6: Run the session API integration tests**

```powershell
python -m pytest tests/integration/test_session_endpoint.py -v
```

Expected: PASS.

- [ ] **Step 7: Run session-service unit tests too**

```powershell
python -m pytest tests/unit/test_session_service.py tests/integration/test_session_endpoint.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit**

```powershell
git add app/api/session.py app/main.py tests/integration/test_session_endpoint.py
git commit -m "refactor: move session endpoints into api router"
```

---

### Task 4: Remove `/process` and obsolete API schemas

**Files:**
- Delete: `app/api/process.py`
- Delete: `tests/integration/test_process.py`
- Inspect/Delete: `app/schemas/transcript.py`
- Inspect/Delete: `app/schemas/youtube.py`
- Modify: `app/main.py` if it still imports the process router

**Interfaces:**
- Removes: `POST /process`
- Keeps: `POST /sessions`
- Keeps: `POST /sessions/{session_id}/check`

- [ ] **Step 1: Search for remaining imports/usages before deleting schemas**

Run:

```powershell
Get-ChildItem app,tests -Recurse -File | Select-String "TranscriptResponse|YouTubeRequest|api.process|/process"
```

Expected: references should be limited to the old process route/test and the old schema files. If any remaining non-process file still uses `TranscriptResponse` or `YouTubeRequest`, do not delete that schema until the dependency is removed or intentionally migrated.

- [ ] **Step 2: Delete the obsolete process endpoint and its integration test**

```powershell
Remove-Item app/api/process.py
Remove-Item tests/integration/test_process.py
```

- [ ] **Step 3: Remove obsolete router imports from `main.py`**

`main.py` must not import or include a process router after this step.

- [ ] **Step 4: Delete old schemas only if Step 1 showed they have no remaining consumers**

```powershell
Remove-Item app/schemas/transcript.py
Remove-Item app/schemas/youtube.py
```

- [ ] **Step 5: Run focused tests**

```powershell
python -m pytest tests/integration/test_session_endpoint.py tests/unit/test_session_service.py tests/unit/test_transcript_service.py tests/unit/test_youtube_service.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add -A app tests
git commit -m "refactor: remove legacy process endpoint"
```

---

### Task 5: Consolidate duplicate tests and naming

**Files:**
- Inspect: `tests/unit/test_transcript.py`
- Inspect: `tests/unit/test_transcript_model.py`
- Inspect: `tests/unit/test_youtube_adapter.py`
- Inspect: `tests/unit/test_youtube_adapter_errors.py`
- Rename: `tests/integration/test_session_endpoint.py` -> `tests/integration/test_session_api.py`

**Interfaces:**
- No production API changes.
- Produces clearer test ownership: one test file per component/responsibility where practical.

- [ ] **Step 1: Compare the two transcript test files**

Run:

```powershell
Get-Content tests/unit/test_transcript.py
Get-Content tests/unit/test_transcript_model.py
```

If both test only `Sentence`, move all unique `Sentence` model tests into `tests/unit/test_transcript_model.py`, then delete `tests/unit/test_transcript.py`.

- [ ] **Step 2: Compare the YouTube adapter test files**

```powershell
Get-Content tests/unit/test_youtube_adapter.py
Get-Content tests/unit/test_youtube_adapter_errors.py
```

If both test `youtube_adapter.fetch_transcript`, move all unique success/error cases into `tests/unit/test_youtube_adapter.py`, then delete `tests/unit/test_youtube_adapter_errors.py`.

- [ ] **Step 3: Rename the session API integration test file**

```powershell
Move-Item tests/integration/test_session_endpoint.py tests/integration/test_session_api.py
```

- [ ] **Step 4: Run the consolidated unit and integration tests**

```powershell
python -m pytest tests/unit tests/integration/test_session_api.py -v
```

Expected: all non-external tests in these paths PASS; external-marked tests may be deselected according to the existing pytest configuration/command behavior.

- [ ] **Step 5: Commit**

```powershell
git add -A tests
git commit -m "test: consolidate backend test structure"
```

---

### Task 6: Final architecture verification

**Files:**
- Verify only; modify only if a discovered stale import/path is directly caused by this refactor.

**Interfaces:**
- Confirms the final architecture and behavior from the spec.

- [ ] **Step 1: Print the final application tree**

```powershell
tree app /F
tree tests /F
```

Expected application structure:

```text
app/
├── main.py
├── errors.py
├── api/
│   └── session.py
├── schemas/
│   └── session.py
├── models/
│   ├── transcript.py
│   └── session.py
├── services/
│   ├── session_service.py
│   ├── transcript_service.py
│   └── youtube_service.py
├── adapters/
│   ├── audio_adapter.py
│   ├── whisper_adapter.py
│   └── youtube_adapter.py
└── config/
    └── settings.py
```

`__init__.py` files and `__pycache__` directories may also appear and are not architectural components.

- [ ] **Step 2: Verify there are no `/process` references left**

```powershell
Get-ChildItem app,tests -Recurse -File | Select-String "api.process|/process|TranscriptResponse|YouTubeRequest"
```

Expected: no matches, assuming the old schemas were deleted in Task 4.

- [ ] **Step 3: Run the complete non-external suite**

```powershell
python -m pytest -v -m "not external"
```

Expected: PASS.

- [ ] **Step 4: Run the external integration tests separately**

```powershell
python -m pytest tests/integration -v -m "external"
```

Expected: PASS when YouTube/Deno/network dependencies are available. A transient YouTube/Deno external failure is not automatically a refactor regression; compare it with the external adapter behavior already observed in this project.

- [ ] **Step 5: Verify Git state**

```powershell
git status
```

Expected: clean working tree after all task commits, or only intentionally uncommitted documentation changes.

- [ ] **Step 6: Final commit only if verification required a stale-import cleanup**

```powershell
git add -A
git commit -m "refactor: finalize backend architecture cleanup"
```

Do not create this commit if Step 1-5 required no code changes.
