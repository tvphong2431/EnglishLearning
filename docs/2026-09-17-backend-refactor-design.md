# Backend Refactor Design

## Goal

Refactor backend thành layer-based architecture rõ ràng mà không thay đổi
behavior hiện tại của ứng dụng.

Sau refactor:

- `/process` bị loại bỏ.
- `POST /sessions` là entry point để tạo bài dictation.
- `POST /sessions/{session_id}/check` dùng để kiểm tra đáp án.
- Session vẫn được lưu trong RAM.
- Chưa thêm database.
- Chưa thêm answer normalization.
- Chưa thêm Show Answer.

## Architecture

Backend được chia thành các layer:

app/
├── main.py
├── errors.py
│
├── api/
│   └── session.py
│
├── schemas/
│   └── session.py
│
├── models/
│   ├── transcript.py
│   └── session.py
│
├── services/
│   ├── session_service.py
│   ├── transcript_service.py
│   └── youtube_service.py
│
├── adapters/
│   ├── audio_adapter.py
│   ├── whisper_adapter.py
│   └── youtube_adapter.py
│
└── config/
    └── settings.py

## Layer Responsibilities

### api

Chịu trách nhiệm HTTP:

- nhận request
- gọi service
- trả response

API không trực tiếp xử lý Whisper, yt-dlp hoặc transcript.

### schemas

Chứa các Pydantic model dùng cho request/response:

- CreateSessionRequest
- CreateSessionResponse
- SentenceInfo
- CheckAnswerRequest
- CheckAnswerResponse

### models

Chứa dữ liệu nội bộ của backend.

Sentence:

- text
- start
- duration
- word_count

Session:

- video_id
- sentences

Session được định nghĩa dưới dạng dataclass:

    @dataclass
    class Session:
        video_id: str
        sentences: list[Sentence]

### services

Chứa business logic.

session_service:

- tạo session
- lấy session
- điều phối việc tạo dictation session
- kiểm tra đáp án

transcript_service:

- tạo Sentence[]
- xử lý transcript hoặc Whisper

youtube_service:

- xử lý và validate YouTube URL
- lấy video_id

### adapters

Chứa code giao tiếp với hệ thống hoặc thư viện bên ngoài:

youtube_adapter:
- YouTube Transcript API

audio_adapter:
- yt-dlp
- FFmpeg

whisper_adapter:
- Whisper

### config

Chứa configuration như:

- Deno path
- PO token server URL

### main.py

Chỉ chịu trách nhiệm:

- tạo FastAPI app
- include router
- đăng ký error handler

## Session Storage

Trong MVP, session tiếp tục được lưu trong RAM.

Thay vì:

    sessions: dict[str, dict]

sử dụng:

    sessions: dict[str, Session]

session_id là UUID và được dùng làm key.

Database hoặc repository layer sẽ được thiết kế sau khi refactor hoàn tất.

## Create Session Flow

Frontend gửi:

    POST /sessions

với YouTube URL.

Flow:

Frontend
→ api/session.py
→ session_service.create_dictation_session()
→ youtube_service.extract_youtube_video_id()
→ transcript_service.build_sentences()
→ adapters nếu cần
→ list[Sentence]
→ tạo Session
→ lưu sessions[session_id]
→ trả response

Frontend chỉ nhận:

- session_id
- video_id
- sentence id
- start
- duration
- word_count

Sentence.text không được gửi frontend.

## Check Answer Flow

Frontend gửi:

    POST /sessions/{session_id}/check

Request body:

    {
        "sentence_id": 0,
        "answer": "You ready?"
    }

Flow:

api/session.py
→ session_service.check_answer()
→ get_session(session_id)
→ lấy Sentence theo sentence_id
→ lấy Sentence.text
→ so sánh với answer
→ trả true hoặc false

Response:

    {
        "correct": true
    }

Trong đợt refactor này, việc so sánh vẫn giữ behavior hiện tại:
so sánh string trực tiếp.

Normalization sẽ được thêm sau.

## Files Removed

Xóa:

    app/api/process.py
    tests/integration/test_process.py

Nếu không còn dependency nào sử dụng chúng thì cũng xóa:

    app/schemas/transcript.py
    app/schemas/youtube.py

## Tests

Giữ hai nhóm:

    tests/unit/
    tests/integration/

Unit test kiểm tra riêng từng model, service và adapter.

Integration test kiểm tra:

- session API
- transcript flow
- audio adapter external behavior
- YouTube adapter external behavior

Các test trùng trách nhiệm sẽ được gộp lại.

Sau refactor, toàn bộ test còn hợp lệ phải pass.

## Out of Scope

Đợt refactor này không thêm:

- database
- repository layer
- answer normalization
- Show Answer
- frontend
- forced alignment
- optimization mới cho Whisper
- thay đổi logic download audio

Mục tiêu duy nhất là làm rõ cấu trúc và trách nhiệm của backend hiện tại.