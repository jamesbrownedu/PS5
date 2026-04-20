# Wxter AI Project Structure

This is the target layout for a free, local-first `Wxter AI` build using:

- `FastAPI` for uploads, parsing, chat, and streaming
- `Ollama` for local text + vision models
- `LangChain` for model orchestration and context flow
- `React + Vite + TypeScript` for the desktop web client

## Recommended root layout

```text
wxter-ai/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- deps.py
|   |   |   \-- routes/
|   |   |       |-- chat.py
|   |   |       |-- files.py
|   |   |       |-- health.py
|   |   |       \-- sessions.py
|   |   |-- core/
|   |   |   |-- config.py
|   |   |   |-- constants.py
|   |   |   \-- logging.py
|   |   |-- models/
|   |   |   |-- chat.py
|   |   |   |-- files.py
|   |   |   \-- session.py
|   |   |-- services/
|   |   |   |-- ingestion/
|   |   |   |   |-- html_parser.py
|   |   |   |   |-- image_ocr.py
|   |   |   |   |-- pdf_parser.py
|   |   |   |   |-- text_parser.py
|   |   |   |   |-- zip_parser.py
|   |   |   |   \-- router.py
|   |   |   |-- llm/
|   |   |   |   |-- chat_chain.py
|   |   |   |   |-- prompt_builder.py
|   |   |   |   |-- stream.py
|   |   |   |   |-- text_model.py
|   |   |   |   \-- vision_model.py
|   |   |   \-- retrieval/
|   |   |       |-- chunker.py
|   |   |       |-- context_builder.py
|   |   |       \-- session_memory.py
|   |   |-- utils/
|   |   |   |-- files.py
|   |   |   |-- hashing.py
|   |   |   \-- paths.py
|   |   \-- main.py
|   \-- tests/
|       |-- test_chat.py
|       |-- test_ingestion.py
|       \-- test_uploads.py
|-- frontend/
|   |-- public/
|   |   |-- fonts/
|   |   |   \-- baloo-2/
|   |   \-- icons/
|   |-- src/
|   |   |-- app/
|   |   |   |-- App.tsx
|   |   |   |-- layout.tsx
|   |   |   \-- routes.tsx
|   |   |-- components/
|   |   |   |-- chat/
|   |   |   |   |-- ChatInput.tsx
|   |   |   |   |-- ChatMessage.tsx
|   |   |   |   \-- ChatPanel.tsx
|   |   |   |-- shell/
|   |   |   |   |-- Header.tsx
|   |   |   |   |-- Sidebar.tsx
|   |   |   |   \-- Workspace.tsx
|   |   |   \-- upload/
|   |   |       |-- Dropzone.tsx
|   |   |       |-- FileCard.tsx
|   |   |       \-- UploadPanel.tsx
|   |   |-- hooks/
|   |   |   |-- useChatStream.ts
|   |   |   \-- useFileUpload.ts
|   |   |-- lib/
|   |   |   |-- api.ts
|   |   |   |-- format.ts
|   |   |   \-- stream.ts
|   |   |-- styles/
|   |   |   |-- globals.css
|   |   |   \-- theme.css
|   |   |-- types/
|   |   |   |-- chat.ts
|   |   |   \-- files.ts
|   |   \-- main.tsx
|   |-- package.json
|   |-- tsconfig.json
|   \-- vite.config.ts
|-- data/
|   |-- cache/
|   |-- extracted/
|   |-- sessions/
|   |-- temp/
|   |-- uploads/
|   \-- vectorstore/
|-- prompts/
|   |-- system.txt
|   |-- summarizer.txt
|   \-- vision.txt
|-- scripts/
|   |-- dev.ps1
|   |-- pull-models.ps1
|   |-- run-backend.ps1
|   \-- run-frontend.ps1
|-- docs/
|   |-- api.md
|   |-- architecture.md
|   \-- ui-spec.md
|-- .env.example
|-- requirements.txt
\-- README.md
```

## Why this structure

- `backend/app/api/routes/`: keeps HTTP concerns separate from parsing and model logic.
- `backend/app/services/ingestion/`: each file type gets its own parser, so PDF, OCR, HTML, and ZIP handling stay isolated and testable.
- `backend/app/services/llm/`: keeps Ollama text and vision calls separate from request routing.
- `backend/app/services/retrieval/`: this is where chunking and per-session context assembly live.
- `frontend/public/fonts/baloo-2/`: self-host the `Baloo 2` font instead of depending on a CDN.
- `data/`: keeps uploaded files and derived text outside the source tree.

## Backend responsibilities

- `chat.py`: accepts user prompts, builds context, and streams tokens back.
- `files.py`: handles upload, validation, parsing, and extraction jobs.
- `health.py`: confirms API, OCR, and Ollama availability.
- `sessions.py`: stores current chat/file session state.
- `router.py`: picks the correct parser based on file extension or MIME type.
- `context_builder.py`: combines extracted text, summaries, and recent chat turns into the final LLM prompt.

## Frontend responsibilities

- `Workspace.tsx`: wide desktop shell with left navigation, center chat, and right-side upload/context panel.
- `ChatPanel.tsx`: streaming response surface with glassmorphism styling.
- `UploadPanel.tsx`: drag-and-drop file upload area with file status and extraction previews.
- `theme.css`: dark palette, glass borders, blur layers, and `Baloo 2` typography tokens.

## Notes

- `Ollama` itself is not a Python package dependency for setup purposes only; it also needs the local desktop/runtime install running on the machine.
- `pytesseract` also requires the native `Tesseract OCR` binary installed and available on `PATH`.
- Keep the current root `app.py` only as a temporary prototype. The real implementation should move into `backend/app/main.py`.
