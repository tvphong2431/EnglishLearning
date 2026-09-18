# Frontend MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng frontend React + Vite + TypeScript cho EnglishLearning, kết nối với FastAPI để tạo session, luyện dictation, check answer, show answer, phát lại từng câu và chuyển câu trước/sau.

**Architecture:** Frontend nằm trong `frontend/` ngang hàng với `backend/`. `App.tsx` giữ `session`; `Home` tạo session; `Dictation` quản lý trạng thái luyện câu; `YouTubePlayer` trực tiếp dùng YouTube IFrame Player API; mọi HTTP request đi qua `src/services/api.ts`. Backend chỉ thay đổi để cho phép CORS từ `http://localhost:5173`.

**Tech Stack:** React, Vite, TypeScript, CSS Modules, Vitest, React Testing Library, YouTube IFrame Player API, FastAPI.

**Spec:** `docs/superpowers/specs/2026-09-18-frontend-mvp-design.md`

## Global Constraints

- Frontend dùng React + Vite + TypeScript.
- Styling dùng CSS Modules; không dùng Tailwind CSS.
- Không dùng React Router trong MVP.
- Không dùng Redux, Zustand, Context hoặc state-management library cho global state.
- Không dùng wrapper library cho YouTube player; dùng trực tiếp YouTube IFrame Player API.
- Frontend development origin là `http://localhost:5173`.
- Backend development origin là `http://localhost:8000`.
- Frontend đọc backend URL từ `VITE_API_BASE_URL`; component không hard-code backend URL.
- Frontend không được nhận `Sentence.text` trong create-session response.
- Refresh trang làm mất session hiện tại và quay về Home.
- Correct/Incorrect không tự chuyển câu.
- Show Answer chỉ gọi backend khi đáp án của câu hiện tại chưa được load.
- Previous bị disable ở câu đầu; Next bị disable ở câu cuối.
- Khi chuyển câu, reset `answer`, `isCorrect`, `shownAnswer`, và `error`.
- YouTubePlayer phát `start → start + duration`; chưa thêm buffer timestamp.
- Backend regression tests hiện có phải tiếp tục pass.
- Các lệnh `git add`/`git commit` trong plan giả định terminal đang ở repository root; nếu đang ở `frontend/` hoặc `backend/`, quay về root trước khi commit.

---

## File Map

### Frontend files created

```text
frontend/
├── .env.example
├── package.json
├── vite.config.ts
├── src/
│   ├── test/
│   │   └── setup.ts
│   ├── types/
│   │   └── session.ts
│   ├── services/
│   │   ├── api.ts
│   │   └── api.test.ts
│   ├── components/
│   │   └── YouTubePlayer/
│   │       ├── YouTubePlayer.tsx
│   │       ├── YouTubePlayer.test.tsx
│   │       └── YouTubePlayer.module.css
│   ├── pages/
│   │   ├── Home/
│   │   │   ├── Home.tsx
│   │   │   ├── Home.test.tsx
│   │   │   └── Home.module.css
│   │   └── Dictation/
│   │       ├── Dictation.tsx
│   │       ├── Dictation.test.tsx
│   │       └── Dictation.module.css
│   ├── App.tsx
│   ├── App.test.tsx
│   ├── App.module.css
│   └── main.tsx
```

### Backend files modified

```text
backend/app/main.py
backend/tests/integration/test_session_endpoint.py
```

---

### Task 1: Scaffold React + Vite + TypeScript and test harness

**Files:**
- Create: `frontend/` using the Vite React TypeScript template
- Modify: `frontend/package.json`
- Modify: `frontend/vite.config.ts`
- Create: `frontend/src/test/setup.ts`
- Create: `frontend/.env.example`
- Delete: Vite demo assets/styles that are no longer used

**Interfaces:**
- Consumes: Node.js + npm installed locally.
- Produces: a buildable React TypeScript app with `npm run test:run` and `npm run build` available to later tasks.

- [ ] **Step 1: Create the Vite project**

From the repository root:

```powershell
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

Expected: `frontend/package.json`, `frontend/src/App.tsx`, `frontend/src/main.tsx`, and TypeScript config files are created.

- [ ] **Step 2: Install the frontend test dependencies**

```powershell
npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event @types/youtube
```

- [ ] **Step 3: Add test scripts to `frontend/package.json`**

Keep the Vite-generated scripts and add:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run"
  }
}
```

- [ ] **Step 4: Configure Vitest in `frontend/vite.config.ts`**

Replace the file with:

```ts
import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
  },
})
```

- [ ] **Step 5: Create the shared test setup**

Create `frontend/src/test/setup.ts`:

```ts
import "@testing-library/jest-dom/vitest"
```

- [ ] **Step 6: Add the frontend environment example**

Create `frontend/.env.example`:

```text
VITE_API_BASE_URL=http://localhost:8000
```

Create the local development file without committing it:

```powershell
Copy-Item .env.example .env
```

Ensure `frontend/.gitignore` contains `.env` while allowing `.env.example` to remain tracked.

- [ ] **Step 7: Remove the Vite demo UI**

Delete the generated demo files if present:

```text
src/App.css
src/index.css
src/assets/react.svg
public/vite.svg
```

Replace `src/App.tsx` temporarily with a compile-safe shell:

```tsx
function App() {
  return <div>English Learning</div>
}

export default App
```

Replace `src/main.tsx` with:

```tsx
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import App from "./App"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- [ ] **Step 8: Verify the scaffold**

```powershell
npm run test:run -- --passWithNoTests
npm run build
```

Expected: Vitest exits with code 0 even though no feature tests exist yet, and `npm run build` exits with code 0.

- [ ] **Step 9: Commit**

```powershell
git add frontend
git commit -m "chore: scaffold frontend app"
```

---

### Task 2: Allow the Vite frontend to call FastAPI with CORS

**Files:**
- Modify: `backend/app/main.py`
- Modify: `backend/tests/integration/test_session_endpoint.py`

**Interfaces:**
- Consumes: FastAPI app from `app.main`.
- Produces: preflight requests from `http://localhost:5173` are accepted by FastAPI.

- [ ] **Step 1: Write the failing CORS integration test**

Append to `backend/tests/integration/test_session_endpoint.py`:

```python

def test_cors_allows_frontend_origin():
    response = client.options(
        "/sessions",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )
```

- [ ] **Step 2: Run the test and verify RED**

From `backend/`:

```powershell
python -m pytest tests/integration/test_session_endpoint.py::test_cors_allows_frontend_origin -v
```

Expected: FAIL because the response does not contain the expected `access-control-allow-origin` header.

- [ ] **Step 3: Add FastAPI CORS middleware**

In `backend/app/main.py`, add:

```python
from fastapi.middleware.cors import CORSMiddleware
```

Immediately after `app = FastAPI()` add:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Do not use `allow_origins=["*"]`.

- [ ] **Step 4: Run the CORS test and verify GREEN**

```powershell
python -m pytest tests/integration/test_session_endpoint.py::test_cors_allows_frontend_origin -v
```

Expected: PASS.

- [ ] **Step 5: Run backend regression tests**

```powershell
python -m pytest -v
```

Expected: all selected backend tests pass with zero failures.

- [ ] **Step 6: Commit**

```powershell
git add backend/app/main.py backend/tests/integration/test_session_endpoint.py
git commit -m "feat: allow frontend development origin"
```

---

### Task 3: Add frontend TypeScript types and API client

**Files:**
- Create: `frontend/src/types/session.ts`
- Create: `frontend/src/services/api.ts`
- Create: `frontend/src/services/api.test.ts`

**Interfaces:**
- Consumes: FastAPI endpoints `POST /sessions`, `POST /sessions/{session_id}/check`, and `GET /sessions/{session_id}/sentences/{sentence_id}/answer`.
- Produces:
  - `createSession(url: string): Promise<Session>`
  - `checkAnswer(sessionId: string, sentenceId: number, answer: string): Promise<CheckAnswerResponse>`
  - `showAnswer(sessionId: string, sentenceId: number): Promise<ShowAnswerResponse>`

- [ ] **Step 1: Define the public frontend types**

Create `frontend/src/types/session.ts`:

```ts
export type SentenceInfo = {
  id: number
  start: number
  duration: number
  word_count: number
}

export type Session = {
  session_id: string
  video_id: string
  sentences: SentenceInfo[]
}

export type CheckAnswerResponse = {
  correct: boolean
}

export type ShowAnswerResponse = {
  answer: string
}
```

- [ ] **Step 2: Write failing API-client tests**

Create `frontend/src/services/api.test.ts`:

```ts
import { beforeEach, describe, expect, it, vi } from "vitest"
import { checkAnswer, createSession, showAnswer } from "./api"

const session = {
  session_id: "session-123",
  video_id: "abc123",
  sentences: [
    {
      id: 0,
      start: 10.26,
      duration: 0.44,
      word_count: 2,
    },
  ],
}

describe("api", () => {
  beforeEach(() => {
    vi.restoreAllMocks()
    vi.stubEnv("VITE_API_BASE_URL", "http://localhost:8000")
    vi.stubGlobal("fetch", vi.fn())
  })

  it("creates a session with the YouTube URL", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => session,
    } as Response)

    await expect(
      createSession("https://www.youtube.com/watch?v=abc123"),
    ).resolves.toEqual(session)

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/sessions",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          url: "https://www.youtube.com/watch?v=abc123",
        }),
      }),
    )
  })

  it("checks an answer", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ correct: true }),
    } as Response)

    await expect(
      checkAnswer("session-123", 0, "You ready"),
    ).resolves.toEqual({ correct: true })

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/sessions/session-123/check",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          sentence_id: 0,
          answer: "You ready",
        }),
      }),
    )
  })

  it("loads the answer", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ answer: "You ready?" }),
    } as Response)

    await expect(showAnswer("session-123", 0)).resolves.toEqual({
      answer: "You ready?",
    })

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/sessions/session-123/sentences/0/answer",
      expect.objectContaining({ method: "GET" }),
    )
  })

  it("throws the backend error message", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      status: 404,
      json: async () => ({
        code: "SESSION_NOT_FOUND",
        message: "Session not found.",
      }),
    } as Response)

    await expect(showAnswer("missing", 0)).rejects.toThrow(
      "Session not found.",
    )
  })
})
```

- [ ] **Step 3: Run the tests and verify RED**

From `frontend/`:

```powershell
npm run test:run -- src/services/api.test.ts
```

Expected: FAIL because `src/services/api.ts` does not exist yet.

- [ ] **Step 4: Implement the API client**

Create `frontend/src/services/api.ts`:

```ts
import type {
  CheckAnswerResponse,
  Session,
  ShowAnswerResponse,
} from "../types/session"

type ApiErrorBody = {
  code?: string
  message?: string
}

function getApiBaseUrl(): string {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

  if (!apiBaseUrl) {
    throw new Error("VITE_API_BASE_URL is not configured.")
  }

  return apiBaseUrl
}

async function requestJson<T>(
  path: string,
  init: RequestInit,
): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
    },
  })

  const body = (await response.json().catch(() => null)) as
    | T
    | ApiErrorBody
    | null

  if (!response.ok) {
    const errorBody = body as ApiErrorBody | null
    throw new Error(
      errorBody?.message ?? `Request failed with status ${response.status}.`,
    )
  }

  return body as T
}

export function createSession(url: string): Promise<Session> {
  return requestJson<Session>("/sessions", {
    method: "POST",
    body: JSON.stringify({ url }),
  })
}

export function checkAnswer(
  sessionId: string,
  sentenceId: number,
  answer: string,
): Promise<CheckAnswerResponse> {
  return requestJson<CheckAnswerResponse>(
    `/sessions/${sessionId}/check`,
    {
      method: "POST",
      body: JSON.stringify({
        sentence_id: sentenceId,
        answer,
      }),
    },
  )
}

export function showAnswer(
  sessionId: string,
  sentenceId: number,
): Promise<ShowAnswerResponse> {
  return requestJson<ShowAnswerResponse>(
    `/sessions/${sessionId}/sentences/${sentenceId}/answer`,
    {
      method: "GET",
    },
  )
}
```

- [ ] **Step 5: Run the API tests and verify GREEN**

```powershell
npm run test:run -- src/services/api.test.ts
```

Expected: 4 tests pass.

- [ ] **Step 6: Commit**

```powershell
git add frontend/src/types/session.ts frontend/src/services/api.ts frontend/src/services/api.test.ts
git commit -m "feat: add frontend api client"
```

---

### Task 4: Build the Home page

**Files:**
- Create: `frontend/src/pages/Home/Home.tsx`
- Create: `frontend/src/pages/Home/Home.test.tsx`
- Create: `frontend/src/pages/Home/Home.module.css`

**Interfaces:**
- Consumes: `createSession(url)` from `src/services/api.ts`.
- Produces: `Home({ onSessionCreated })`, where `onSessionCreated(session: Session): void` sends the created session to `App.tsx`.

- [ ] **Step 1: Write the Home component tests**

Create `frontend/src/pages/Home/Home.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"
import { createSession } from "../../services/api"
import Home from "./Home"

vi.mock("../../services/api", () => ({
  createSession: vi.fn(),
}))

const session = {
  session_id: "session-123",
  video_id: "abc123",
  sentences: [
    {
      id: 0,
      start: 10.26,
      duration: 0.44,
      word_count: 2,
    },
  ],
}

describe("Home", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("sends the URL and returns the created session", async () => {
    const user = userEvent.setup()
    const onSessionCreated = vi.fn()
    vi.mocked(createSession).mockResolvedValue(session)

    render(<Home onSessionCreated={onSessionCreated} />)

    await user.type(
      screen.getByLabelText("YouTube URL"),
      "https://www.youtube.com/watch?v=abc123",
    )
    await user.click(screen.getByRole("button", { name: "Start" }))

    expect(createSession).toHaveBeenCalledWith(
      "https://www.youtube.com/watch?v=abc123",
    )
    expect(onSessionCreated).toHaveBeenCalledWith(session)
  })

  it("shows a loading state while creating the session", async () => {
    const user = userEvent.setup()
    let resolveRequest!: (value: typeof session) => void

    vi.mocked(createSession).mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveRequest = resolve
        }),
    )

    render(<Home onSessionCreated={vi.fn()} />)

    await user.type(
      screen.getByLabelText("YouTube URL"),
      "https://www.youtube.com/watch?v=abc123",
    )
    await user.click(screen.getByRole("button", { name: "Start" }))

    expect(
      screen.getByRole("button", { name: "Creating session..." }),
    ).toBeDisabled()

    resolveRequest(session)
    expect(
      await screen.findByRole("button", { name: "Start" }),
    ).toBeEnabled()
  })

  it("shows the backend error message", async () => {
    const user = userEvent.setup()
    vi.mocked(createSession).mockRejectedValue(
      new Error("Invalid YouTube URL."),
    )

    render(<Home onSessionCreated={vi.fn()} />)

    await user.type(
      screen.getByLabelText("YouTube URL"),
      "https://example.com/not-youtube",
    )
    await user.click(screen.getByRole("button", { name: "Start" }))

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Invalid YouTube URL.",
    )
  })
})
```

- [ ] **Step 2: Run the Home tests and verify RED**

```powershell
npm run test:run -- src/pages/Home/Home.test.tsx
```

Expected: FAIL because `Home.tsx` does not exist.

- [ ] **Step 3: Implement `Home.tsx`**

Create `frontend/src/pages/Home/Home.tsx`:

```tsx
import { useState, type FormEvent } from "react"
import { createSession } from "../../services/api"
import type { Session } from "../../types/session"
import styles from "./Home.module.css"

type HomeProps = {
  onSessionCreated: (session: Session) => void
}

function Home({ onSessionCreated }: HomeProps) {
  const [url, setUrl] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const session = await createSession(url)
      onSessionCreated(session)
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to create session.",
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className={styles.page}>
      <div className={styles.card}>
        <h1>English Learning</h1>
        <p>Paste a YouTube URL to start a dictation session.</p>

        <form className={styles.form} onSubmit={handleSubmit}>
          <label htmlFor="youtube-url">YouTube URL</label>
          <div className={styles.controls}>
            <input
              id="youtube-url"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              required
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? "Creating session..." : "Start"}
            </button>
          </div>
        </form>

        {error && <p role="alert" className={styles.error}>{error}</p>}
      </div>
    </section>
  )
}

export default Home
```

- [ ] **Step 4: Add Home styles**

Create `frontend/src/pages/Home/Home.module.css`:

```css
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem;
}

.card {
  width: min(760px, 100%);
  background: white;
  border: 1px solid #dbe3ef;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 12px 30px rgb(15 23 42 / 8%);
}

.form {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.controls {
  display: flex;
  gap: 0.75rem;
}

.controls input {
  flex: 1;
  min-width: 0;
  padding: 0.8rem 1rem;
}

.controls button {
  padding: 0.8rem 1.25rem;
}

.error {
  margin-top: 1rem;
  color: #b42318;
}
```

- [ ] **Step 5: Run the Home tests and verify GREEN**

```powershell
npm run test:run -- src/pages/Home/Home.test.tsx
```

Expected: 3 tests pass.

- [ ] **Step 6: Commit**

```powershell
git add frontend/src/pages/Home
git commit -m "feat: add session start page"
```

---

### Task 5: Build the direct YouTube IFrame player component

**Files:**
- Create: `frontend/src/components/YouTubePlayer/YouTubePlayer.tsx`
- Create: `frontend/src/components/YouTubePlayer/YouTubePlayer.test.tsx`
- Create: `frontend/src/components/YouTubePlayer/YouTubePlayer.module.css`

**Interfaces:**
- Consumes props: `videoId: string`, `start: number`, `duration: number`.
- Produces: embedded YouTube player that seeks to `start`, plays, pauses after `duration`, and exposes Replay through its own button.

- [ ] **Step 1: Write the player behavior test**

Create `frontend/src/components/YouTubePlayer/YouTubePlayer.test.tsx`:

```tsx
import { act, render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { afterEach, beforeEach, expect, it, vi } from "vitest"
import YouTubePlayer from "./YouTubePlayer"

const seekTo = vi.fn()
const playVideo = vi.fn()
const pauseVideo = vi.fn()
const destroy = vi.fn()

class FakePlayer {
  constructor(
    _element: HTMLElement,
    options: YT.PlayerOptions,
  ) {
    options.events?.onReady?.({
      target: this,
    } as unknown as YT.PlayerEvent)
  }

  seekTo = seekTo
  playVideo = playVideo
  pauseVideo = pauseVideo
  destroy = destroy
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.clearAllMocks()
  vi.stubGlobal("YT", {
    Player: FakePlayer,
  })
})

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

it("plays only the requested sentence segment and can replay it", async () => {
  const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime })

  render(
    <YouTubePlayer
      videoId="abc123"
      start={10.26}
      duration={0.44}
    />,
  )

  await waitFor(() => {
    expect(seekTo).toHaveBeenCalledWith(10.26, true)
  })
  expect(playVideo).toHaveBeenCalled()

  act(() => {
    vi.advanceTimersByTime(440)
  })
  expect(pauseVideo).toHaveBeenCalled()

  seekTo.mockClear()
  playVideo.mockClear()

  await user.click(screen.getByRole("button", { name: "Replay" }))

  expect(seekTo).toHaveBeenCalledWith(10.26, true)
  expect(playVideo).toHaveBeenCalled()
})
```

- [ ] **Step 2: Run the player test and verify RED**

```powershell
npm run test:run -- src/components/YouTubePlayer/YouTubePlayer.test.tsx
```

Expected: FAIL because `YouTubePlayer.tsx` does not exist.

- [ ] **Step 3: Implement the YouTube IFrame API loader and player**

Create `frontend/src/components/YouTubePlayer/YouTubePlayer.tsx`:

```tsx
import { useCallback, useEffect, useRef } from "react"
import styles from "./YouTubePlayer.module.css"

type YouTubePlayerProps = {
  videoId: string
  start: number
  duration: number
}

let youtubeApiPromise: Promise<void> | null = null

function loadYouTubeApi(): Promise<void> {
  if (window.YT?.Player) {
    return Promise.resolve()
  }

  if (youtubeApiPromise) {
    return youtubeApiPromise
  }

  youtubeApiPromise = new Promise((resolve) => {
    const previousReady = window.onYouTubeIframeAPIReady

    window.onYouTubeIframeAPIReady = () => {
      previousReady?.()
      resolve()
    }

    if (!document.getElementById("youtube-iframe-api")) {
      const script = document.createElement("script")
      script.id = "youtube-iframe-api"
      script.src = "https://www.youtube.com/iframe_api"
      document.body.appendChild(script)
    }
  })

  return youtubeApiPromise
}

function YouTubePlayer({
  videoId,
  start,
  duration,
}: YouTubePlayerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const playerRef = useRef<YT.Player | null>(null)
  const pauseTimerRef = useRef<number | null>(null)
  const startRef = useRef(start)
  const durationRef = useRef(duration)

  const clearPauseTimer = useCallback(() => {
    if (pauseTimerRef.current !== null) {
      window.clearTimeout(pauseTimerRef.current)
      pauseTimerRef.current = null
    }
  }, [])

  const playCurrentSegment = useCallback(
    (player: YT.Player | null = playerRef.current) => {
      if (!player) {
        return
      }

      clearPauseTimer()
      player.seekTo(startRef.current, true)
      player.playVideo()

      pauseTimerRef.current = window.setTimeout(() => {
        player.pauseVideo()
      }, durationRef.current * 1000)
    },
    [clearPauseTimer],
  )

  useEffect(() => {
    startRef.current = start
    durationRef.current = duration
    playCurrentSegment()
  }, [start, duration, playCurrentSegment])

  useEffect(() => {
    let cancelled = false

    loadYouTubeApi().then(() => {
      if (cancelled || !containerRef.current) {
        return
      }

      if (!window.YT) {
        return
      }

      playerRef.current = new window.YT.Player(containerRef.current, {
        videoId,
        playerVars: {
          playsinline: 1,
        },
        events: {
          onReady: (event) => {
            playerRef.current = event.target
            playCurrentSegment(event.target)
          },
        },
      })
    })

    return () => {
      cancelled = true
      clearPauseTimer()
      playerRef.current?.destroy()
      playerRef.current = null
    }
  }, [videoId, clearPauseTimer, playCurrentSegment])

  return (
    <div className={styles.wrapper}>
      <div ref={containerRef} className={styles.player} />
      <button type="button" onClick={() => playCurrentSegment()}>
        Replay
      </button>
    </div>
  )
}

export default YouTubePlayer
```

Add the Window callback type near the top of the same file, after imports:

```ts
declare global {
  interface Window {
    YT?: typeof YT
    onYouTubeIframeAPIReady?: () => void
  }
}
```

- [ ] **Step 4: Add player styles**

Create `frontend/src/components/YouTubePlayer/YouTubePlayer.module.css`:

```css
.wrapper {
  display: grid;
  gap: 0.75rem;
}

.player {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #0f172a;
}

.wrapper button {
  justify-self: start;
  padding: 0.65rem 1rem;
}
```

- [ ] **Step 5: Run the player test and verify GREEN**

```powershell
npm run test:run -- src/components/YouTubePlayer/YouTubePlayer.test.tsx
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add frontend/src/components/YouTubePlayer
git commit -m "feat: add youtube sentence player"
```

---

### Task 6: Build the Dictation page behavior

**Files:**
- Create: `frontend/src/pages/Dictation/Dictation.tsx`
- Create: `frontend/src/pages/Dictation/Dictation.test.tsx`
- Create: `frontend/src/pages/Dictation/Dictation.module.css`

**Interfaces:**
- Consumes: `session: Session`, `checkAnswer`, `showAnswer`, and `YouTubePlayer`.
- Produces: complete single-session dictation interaction with check, show answer, replay, previous, and next.

- [ ] **Step 1: Write the Dictation component tests**

Create `frontend/src/pages/Dictation/Dictation.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"
import { checkAnswer, showAnswer } from "../../services/api"
import type { Session } from "../../types/session"
import Dictation from "./Dictation"

vi.mock("../../services/api", () => ({
  checkAnswer: vi.fn(),
  showAnswer: vi.fn(),
}))

vi.mock("../../components/YouTubePlayer/YouTubePlayer", () => ({
  default: () => <div data-testid="youtube-player" />,
}))

const session: Session = {
  session_id: "session-123",
  video_id: "abc123",
  sentences: [
    {
      id: 0,
      start: 10.26,
      duration: 0.44,
      word_count: 2,
    },
    {
      id: 1,
      start: 12.0,
      duration: 1.2,
      word_count: 3,
    },
  ],
}

describe("Dictation", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("sends the current sentence and typed answer", async () => {
    const user = userEvent.setup()
    vi.mocked(checkAnswer).mockResolvedValue({ correct: true })

    render(<Dictation session={session} />)

    await user.type(screen.getByLabelText("Your answer"), "You ready")
    await user.click(screen.getByRole("button", { name: "Check Answer" }))

    expect(checkAnswer).toHaveBeenCalledWith(
      "session-123",
      0,
      "You ready",
    )
    expect(await screen.findByText("Correct")).toBeInTheDocument()
  })

  it("keeps an incorrect answer editable", async () => {
    const user = userEvent.setup()
    vi.mocked(checkAnswer).mockResolvedValue({ correct: false })

    render(<Dictation session={session} />)

    const input = screen.getByLabelText("Your answer")
    await user.type(input, "Wrong words")
    await user.click(screen.getByRole("button", { name: "Check Answer" }))

    expect(await screen.findByText("Incorrect")).toBeInTheDocument()
    expect(input).toHaveValue("Wrong words")
  })

  it("shows the answer and does not request it twice for the same sentence", async () => {
    const user = userEvent.setup()
    vi.mocked(showAnswer).mockResolvedValue({ answer: "You ready?" })

    render(<Dictation session={session} />)

    const button = screen.getByRole("button", { name: "Show Answer" })
    await user.click(button)

    expect(await screen.findByText("You ready?")).toBeInTheDocument()
    expect(showAnswer).toHaveBeenCalledWith("session-123", 0)

    await user.click(button)
    expect(showAnswer).toHaveBeenCalledTimes(1)
  })

  it("resets sentence state when moving to the next sentence", async () => {
    const user = userEvent.setup()
    vi.mocked(checkAnswer).mockResolvedValue({ correct: false })
    vi.mocked(showAnswer).mockResolvedValue({ answer: "You ready?" })

    render(<Dictation session={session} />)

    await user.type(screen.getByLabelText("Your answer"), "Wrong words")
    await user.click(screen.getByRole("button", { name: "Check Answer" }))
    await user.click(screen.getByRole("button", { name: "Show Answer" }))
    await user.click(screen.getByRole("button", { name: "Next" }))

    expect(screen.getByLabelText("Your answer")).toHaveValue("")
    expect(screen.queryByText("Incorrect")).not.toBeInTheDocument()
    expect(screen.queryByText("You ready?")).not.toBeInTheDocument()
    expect(screen.getByText("Sentence 2 / 2")).toBeInTheDocument()
  })

  it("disables navigation at the first and last sentence", async () => {
    const user = userEvent.setup()

    render(<Dictation session={session} />)

    expect(screen.getByRole("button", { name: "Previous" })).toBeDisabled()
    expect(screen.getByRole("button", { name: "Next" })).toBeEnabled()

    await user.click(screen.getByRole("button", { name: "Next" }))

    expect(screen.getByRole("button", { name: "Previous" })).toBeEnabled()
    expect(screen.getByRole("button", { name: "Next" })).toBeDisabled()
  })
})
```

- [ ] **Step 2: Run the Dictation tests and verify RED**

```powershell
npm run test:run -- src/pages/Dictation/Dictation.test.tsx
```

Expected: FAIL because `Dictation.tsx` does not exist.

- [ ] **Step 3: Implement `Dictation.tsx`**

Create `frontend/src/pages/Dictation/Dictation.tsx`:

```tsx
import { useState } from "react"
import YouTubePlayer from "../../components/YouTubePlayer/YouTubePlayer"
import { checkAnswer, showAnswer } from "../../services/api"
import type { Session } from "../../types/session"
import styles from "./Dictation.module.css"

type DictationProps = {
  session: Session
}

function Dictation({ session }: DictationProps) {
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState(0)
  const [answer, setAnswer] = useState("")
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null)
  const [shownAnswer, setShownAnswer] = useState<string | null>(null)
  const [isChecking, setIsChecking] = useState(false)
  const [isShowingAnswer, setIsShowingAnswer] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const currentSentence = session.sentences[currentSentenceIndex]
  const isFirstSentence = currentSentenceIndex === 0
  const isLastSentence =
    currentSentenceIndex === session.sentences.length - 1

  function resetSentenceState() {
    setAnswer("")
    setIsCorrect(null)
    setShownAnswer(null)
    setError(null)
  }

  function moveToSentence(nextIndex: number) {
    setCurrentSentenceIndex(nextIndex)
    resetSentenceState()
  }

  async function handleCheckAnswer() {
    setIsChecking(true)
    setError(null)

    try {
      const result = await checkAnswer(
        session.session_id,
        currentSentence.id,
        answer,
      )
      setIsCorrect(result.correct)
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to check answer.",
      )
    } finally {
      setIsChecking(false)
    }
  }

  async function handleShowAnswer() {
    if (shownAnswer !== null) {
      return
    }

    setIsShowingAnswer(true)
    setError(null)

    try {
      const result = await showAnswer(
        session.session_id,
        currentSentence.id,
      )
      setShownAnswer(result.answer)
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to show answer.",
      )
    } finally {
      setIsShowingAnswer(false)
    }
  }

  return (
    <section className={styles.page}>
      <div className={styles.playerColumn}>
        <YouTubePlayer
          videoId={session.video_id}
          start={currentSentence.start}
          duration={currentSentence.duration}
        />
      </div>

      <div className={styles.practiceColumn}>
        <div className={styles.headingRow}>
          <strong>
            Sentence {currentSentenceIndex + 1} / {session.sentences.length}
          </strong>
          <span>{currentSentence.word_count} words</span>
        </div>

        <label htmlFor="answer">Your answer</label>
        <textarea
          id="answer"
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          rows={5}
        />

        <div className={styles.actions}>
          <button
            type="button"
            onClick={handleCheckAnswer}
            disabled={isChecking}
          >
            {isChecking ? "Checking..." : "Check Answer"}
          </button>

          <button
            type="button"
            onClick={handleShowAnswer}
            disabled={isShowingAnswer}
          >
            {isShowingAnswer ? "Loading answer..." : "Show Answer"}
          </button>
        </div>

        {isCorrect === true && (
          <p role="status" className={styles.correct}>Correct</p>
        )}
        {isCorrect === false && (
          <p role="status" className={styles.incorrect}>Incorrect</p>
        )}
        {shownAnswer !== null && (
          <p className={styles.answer}>Answer: {shownAnswer}</p>
        )}
        {error && <p role="alert" className={styles.error}>{error}</p>}

        <div className={styles.navigation}>
          <button
            type="button"
            disabled={isFirstSentence}
            onClick={() => moveToSentence(currentSentenceIndex - 1)}
          >
            Previous
          </button>
          <button
            type="button"
            disabled={isLastSentence}
            onClick={() => moveToSentence(currentSentenceIndex + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </section>
  )
}

export default Dictation
```

- [ ] **Step 4: Add Dictation styles**

Create `frontend/src/pages/Dictation/Dictation.module.css`:

```css
.page {
  width: min(1180px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 2rem 0;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
  gap: 1.5rem;
}

.playerColumn,
.practiceColumn {
  background: white;
  border: 1px solid #dbe3ef;
  border-radius: 16px;
  padding: 1rem;
}

.practiceColumn {
  display: grid;
  gap: 0.9rem;
}

.headingRow,
.actions,
.navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.practiceColumn textarea {
  width: 100%;
  resize: vertical;
  padding: 0.8rem;
}

.actions button,
.navigation button {
  padding: 0.7rem 1rem;
}

.correct {
  color: #067647;
}

.incorrect,
.error {
  color: #b42318;
}

.answer {
  padding: 0.8rem;
  background: #eff6ff;
  border-radius: 8px;
}

@media (max-width: 820px) {
  .page {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 5: Run the Dictation tests and verify GREEN**

```powershell
npm run test:run -- src/pages/Dictation/Dictation.test.tsx
```

Expected: 5 tests pass.

- [ ] **Step 6: Commit**

```powershell
git add frontend/src/pages/Dictation
git commit -m "feat: add dictation practice page"
```

---

### Task 7: Wire App state, apply global shell styles, and verify the full MVP

**Files:**
- Modify: `frontend/src/App.tsx`
- Create: `frontend/src/App.test.tsx`
- Create: `frontend/src/App.module.css`
- Verify: `frontend/src/main.tsx`

**Interfaces:**
- Consumes: `Home`, `Dictation`, and `Session`.
- Produces: app-level flow `session == null → Home`, `session != null → Dictation` with in-memory-only session state.

- [ ] **Step 1: Write the App state-transition test**

Create `frontend/src/App.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { expect, it, vi } from "vitest"
import App from "./App"

vi.mock("./pages/Home/Home", () => ({
  default: ({
    onSessionCreated,
  }: {
    onSessionCreated: (session: {
      session_id: string
      video_id: string
      sentences: []
    }) => void
  }) => (
    <button
      type="button"
      onClick={() =>
        onSessionCreated({
          session_id: "session-123",
          video_id: "abc123",
          sentences: [],
        })
      }
    >
      Create fake session
    </button>
  ),
}))

vi.mock("./pages/Dictation/Dictation", () => ({
  default: ({ session }: { session: { video_id: string } }) => (
    <div>Dictation for {session.video_id}</div>
  ),
}))

it("switches from Home to Dictation after a session is created", async () => {
  const user = userEvent.setup()

  render(<App />)

  await user.click(
    screen.getByRole("button", { name: "Create fake session" }),
  )

  expect(screen.getByText("Dictation for abc123")).toBeInTheDocument()
})
```

- [ ] **Step 2: Run the App test and verify RED**

```powershell
npm run test:run -- src/App.test.tsx
```

Expected: FAIL because `App.tsx` still renders only the temporary scaffold.

- [ ] **Step 3: Implement app-level session state**

Replace `frontend/src/App.tsx` with:

```tsx
import { useState } from "react"
import styles from "./App.module.css"
import Dictation from "./pages/Dictation/Dictation"
import Home from "./pages/Home/Home"
import type { Session } from "./types/session"

function App() {
  const [session, setSession] = useState<Session | null>(null)

  return (
    <main className={styles.app}>
      {session === null ? (
        <Home onSessionCreated={setSession} />
      ) : (
        <Dictation session={session} />
      )}
    </main>
  )
}

export default App
```

- [ ] **Step 4: Add app shell styles**

Create `frontend/src/App.module.css`:

```css
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  color: #132238;
  background: #f5f7fb;
}

:global(button),
:global(input),
:global(textarea) {
  font: inherit;
}

:global(button) {
  cursor: pointer;
}

:global(button:disabled) {
  cursor: not-allowed;
  opacity: 0.55;
}

.app {
  min-height: 100vh;
}
```

- [ ] **Step 5: Run the App test and verify GREEN**

```powershell
npm run test:run -- src/App.test.tsx
```

Expected: PASS.

- [ ] **Step 6: Run the full frontend automated verification**

From `frontend/`:

```powershell
npm run test:run
npm run build
```

Expected: all frontend tests pass and TypeScript/Vite build succeeds.

- [ ] **Step 7: Run backend regression tests again**

From `backend/`:

```powershell
python -m pytest -v
```

Expected: all selected backend tests pass with zero failures.

- [ ] **Step 8: Run the real frontend ↔ backend flow in the browser**

Terminal 1, from `backend/` with the Python virtual environment active:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Terminal 2, from `frontend/`:

```powershell
npm run dev
```

Open:

```text
http://localhost:5173
```

Manually verify this exact sequence:

```text
1. Home loads.
2. Enter a valid YouTube URL.
3. Start becomes loading/disabled while POST /sessions is pending.
4. Successful response switches to Dictation without a page reload.
5. The YouTube player loads the session video.
6. The current sentence segment seeks to start and pauses after duration.
7. Replay repeats the same segment.
8. Check Answer shows Correct for a normalized correct answer.
9. Check Answer shows Incorrect for a wrong answer and keeps the typed text.
10. Show Answer displays Sentence.text returned by the backend.
11. Previous is disabled on the first sentence.
12. Next changes sentence and clears answer/result/shown answer.
13. Next is disabled on the last sentence.
14. Backend error messages appear as text instead of breaking the page.
15. Refreshing the browser returns to Home because session state is memory-only.
```

If browser autoplay blocks the first automatic `playVideo()` call, record that browser behavior separately; do not add a timestamp buffer or a new playback library as part of this MVP task.

- [ ] **Step 9: Commit the app wiring**

```powershell
git add frontend/src/App.tsx frontend/src/App.test.tsx frontend/src/App.module.css frontend/src/main.tsx
git commit -m "feat: connect frontend dictation flow"
```

- [ ] **Step 10: Push the completed branch**

```powershell
git push
```

---

## Final Verification Checklist

Before opening or merging a Pull Request, verify all of the following with fresh commands:

```powershell
# frontend
cd frontend
npm run test:run
npm run build

# backend
cd ..\backend
python -m pytest -v

# repository
cd ..
git status
```

Expected final repository state:

```text
frontend tests: 0 failures
frontend build: success
backend tests: 0 failures
git status: working tree clean
```

The browser manual flow in Task 7 must also be completed once with a real YouTube URL before the feature branch is considered ready to merge.
