<div align="center">

# 🎓 LectureIQ

### Turn any lecture into study notes, quizzes, and spoken assessments — powered by GenAI.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)]()

**[🚀 Live Demo](#)** · **[📖 Docs Below](#-table-of-contents)** · **[🐛 Report a Bug](../../issues)**

</div>

---

## 📌 What is LectureIQ?

Upload a lecture — **PDF, DOCX, or PPTX** — and LectureIQ's AI pipeline turns it into a complete study experience: your file becomes AI-written study notes, which unlock an MCQ challenge and a speaking challenge, which together produce a final performance report.

No manual note-taking. No hand-written quizzes. Just upload, and let the AI do the rest — grounded strictly in *your* lecture content, nothing invented, nothing outside it.

<div align="center">

| 📚 Study Notes | 🧠 MCQ Challenge | 🎙️ Speaking Challenge | 📊 Report Card |
|:---:|:---:|:---:|:---:|
| Summary, key concepts, definitions & examples | Timed multiple-choice questions | Verbal answers, transcribed & evaluated | Strengths, gaps & score breakdown |

</div>

---

## 📖 Table of Contents

<details open>
<summary>Click to expand</summary>

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🧰 Tech Stack](#-tech-stack)
- [⚡ Getting Started](#-getting-started)
- [🔌 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [☁️ Deployment](#️-deployment)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

</details>

---

## ✨ Features

- 📄 **Multi-format ingestion** — PDF, DOCX, and PPTX lectures, parsed and chunked automatically
- 🔍 **RAG-grounded generation** — every question, note, and evaluation is retrieved from *your* lecture content via a Chroma vector store, not the model's general knowledge
- 📝 **Structured study notes** — auto-generated lecture summary, key concepts, definitions, important points, and examples, exportable as a clean PDF
- 🧠 **Adaptive MCQ engine** — timed multiple-choice quizzes generated fresh from lecture content, with verbatim-validated answer keys
- 🎙️ **Speaking assessment** — record a spoken answer, get it transcribed (Groq Whisper) and evaluated for accuracy against the lecture
- 📊 **AI performance reports** — per-test strengths & recommendations, generated from your actual results — not hardcoded feedback
- 🎨 **Modern glass-UI frontend** — built entirely in Streamlit, no separate JS frontend required

---

## 🏗️ Architecture

<div align="center">

**User** uploads a lecture through the **Streamlit Frontend**, which talks to the **FastAPI Backend** over a REST API.

Inside the backend, the lecture flows through a **Document Loader → Chunker → Sentence-Transformer Embeddings → Chroma Vector Store** pipeline. From there, relevant lecture context is retrieved and passed to the **Groq LLM** (`gpt-oss-20b`), which powers study-note generation, MCQ generation, and speaking-question generation. Spoken answers are transcribed separately via **Groq Whisper** before being fed back into the LLM for evaluation. Study notes can additionally be exported as a **PDF** through ReportLab.

</div>

| Layer | Responsibility |
|:---|:---|
| 🎨 Frontend (Streamlit) | UI, user interaction, and calling the backend API — contains **zero AI logic** |
| ⚙️ Backend (FastAPI) | Document parsing, chunking, retrieval, LLM orchestration, scoring, PDF export |
| 🗂️ Chroma Vector Store | Stores lecture embeddings for retrieval-augmented generation |
| 🤖 Groq LLM | Generates notes, questions, evaluations, and reports — grounded only in retrieved lecture context |
| 🎧 Groq Whisper | Transcribes spoken answers for the speaking challenge |

---

## 🧰 Tech Stack

<table>
<tr>
<td valign="top" width="33%">

**Backend**
- FastAPI
- LangChain
- Chroma (vector store)
- Sentence Transformers
- Pydantic

</td>
<td valign="top" width="33%">

**AI / GenAI**
- Groq LLM (`openai/gpt-oss-20b`)
- Groq Whisper (speech-to-text)
- RAG (retrieval-augmented generation)
- Structured JSON output + local validation

</td>
<td valign="top" width="33%">

**Frontend & Tooling**
- Streamlit
- ReportLab (PDF generation)
- PyMuPDF / python-docx / python-pptx
- `uv` (dependency management)

</td>
</tr>
</table>

---

## ⚡ Getting Started

**Prerequisites:** Python 3.12+, and a Groq API key (available from the Groq console).

1. **Clone the repository** to your machine and set up your environment file with your Groq API key.
2. **Install and run the backend** — install the dependencies listed in `backend/requirements.txt` (or sync via `uv` if you're using that workflow), then launch the FastAPI app with Uvicorn. Once running, the backend is reachable locally and its health can be checked at the `/health` endpoint.
3. **Install and run the frontend** — install the dependencies listed in `frontend/requirements.txt`, then launch the Streamlit app. It will open in your browser automatically.
4. **Try it out** — upload a lecture file (PDF, DOCX, or PPTX) and walk through the full flow: Study Notes → MCQ Challenge → Speaking Challenge → Final Report.

---

## 🔌 API Reference

<details>
<summary><strong>Click to expand full endpoint table</strong></summary>

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload a lecture file (PDF/DOCX/PPTX) |
| `POST` | `/generate-notes` | Generate structured study notes |
| `POST` | `/generate-notes-pdf` | Generate a downloadable PDF of the notes |
| `GET` | `/download/notes-pdf` | Download the generated PDF |
| `POST` | `/quiz/start` | Start an MCQ quiz |
| `GET` | `/quiz/current` | Get the current quiz question |
| `POST` | `/quiz/answer` | Submit an answer |
| `GET` | `/quiz/result` | Get final quiz score |
| `POST` | `/quiz/report` | Generate an AI-written MCQ performance report |
| `POST` | `/speaking/question` | Generate a speaking-challenge question for a topic |
| `POST` | `/speaking/transcribe` | Transcribe a recorded/uploaded audio answer |
| `POST` | `/speaking/evaluate` | Evaluate a transcribed answer for accuracy |
| `POST` | `/speaking/report` | Generate an AI-written speaking performance report |

Interactive Swagger documentation is available at the `/docs` path once the backend is running.

</details>

---

## 📁 Project Structure

- **`backend/`** — the FastAPI application
  - `main.py` — all API routes
  - `document_loader.py` — PDF/DOCX/PPTX parsing
  - `schemas/` — Pydantic models for every request/response shape
  - `services/` — RAG pipeline, LLM calls, quiz logic, speaking evaluation, PDF generation
- **`frontend/`** — the Streamlit application
  - `app.py` — entrypoint
  - `api_client.py` — every backend call, centralized in one place
  - `state.py` — session-state schema and shared UI helpers
  - `styles.py` — the design system (colors, typography, CSS)
  - `components/` — navigation and footer
  - `views/` — Home, Upload, Study Notes, MCQ, Speaking, and Report pages
- **`data/chroma/`** — the vector store, generated at runtime

---

## ☁️ Deployment

| Component | Platform | Notes |
|:---|:---|:---|
| Backend | 🤗 Hugging Face Spaces (Docker) | Enough RAM headroom for local embeddings |
| Frontend | ☁️ Streamlit Community Cloud | Points at the live backend URL via a secret |

> ⚠️ **Note:** this deployment setup targets a single-session demo (no per-user isolation on the backend). Fine for showcasing — not intended for concurrent multi-user production traffic without a backend refactor.

---

## 🗺️ Roadmap

- [ ] Per-session state isolation for real multi-user support
- [ ] Retrieval quality evaluation (groundedness / hit-rate metrics)
- [ ] Adjustable MCQ difficulty
- [ ] Support for additional lecture formats (video transcripts)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome — feel free to check the issues page.

The general flow: fork the repository, create a feature branch, commit your changes with a clear message, push the branch, and open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

<div align="center">

Made with 🎓 + 🤖 by **[Your Name]**

</div>
