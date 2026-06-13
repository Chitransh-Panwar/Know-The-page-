# 🌐 Know the Page

> A Chrome extension that lets you **chat with any webpage or YouTube video** using AI. Ask questions, get answers — no copy-pasting, no tab switching.

<br/>

## 📸 Screenshots<img width="1663" height="922" alt="Screenshot 2026-06-13 at 10 07 19 AM" src="https://github.com/user-attachments/assets/63f6defe-d1c6-40bc-ad8a-d3e698733daf" />
<img width="1668" height="901" alt="Screenshot 2026-06-13 at 10 08 54 AM" src="https://github.com/user-attachments/assets/e1ab8642-d290-43ea-83e6-9b77fb3d112f" />




<br/>

## ✨ Features

- 🎬 **YouTube RAG** — fetches video transcript, builds a vector index, and answers questions with full chat memory
- 🌍 **Webpage Q&A** — scrapes any webpage using Playwright (with BeautifulSoup fallback) and answers questions about its content
- 💬 **Chat history** — remembers context across multiple questions in the same session
- 🔄 **New session** — reset conversation with one click
- 🌐 **Multilingual** — supports transcripts in English, Hindi, Spanish, French, German, Portuguese, Arabic, Russian, Japanese, Korean, Chinese, Italian and more
- ⚡ **Side panel UI** — opens inline in Chrome, no new tabs

<br/>

## 🏗️ Architecture

```
Chrome Extension (JS)
        │
        ▼
  FastAPI Backend (Python)
        │
        ├── YouTube URL? ──► Fetch Transcript ──► FAISS Vector Store ──► RAG Chain ──► Answer
        │
        └── Other URL? ────► Playwright Scrape ──► Truncate Text ──► LLM Chain ──► Answer
```

<br/>

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Extension | Chrome MV3, JavaScript |
| Backend | FastAPI, Python |
| YT Transcript | youtube-transcript-api |
| Vector Store | FAISS |
| Embeddings | OpenAI `text-embedding-3-small` via OpenRouter |
| LLM | OpenRouter API |
| Scraper | Playwright + BeautifulSoup4 |
| Framework | LangChain |

<br/>

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- Google Chrome
- An [OpenRouter](https://openrouter.ai) API key

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/know-the-page.git
cd know-the-page
```

---

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

---

### 3. Add your API key

Create a `.env` file inside the `backend/` folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

> Get your free API key at [openrouter.ai/keys](https://openrouter.ai/keys)

---

### 4. (Optional) Add YouTube cookies

Some YouTube videos may require authentication to fetch transcripts when running from a server IP.

- Install the **"Get cookies.txt LOCALLY"** Chrome extension
- Go to [youtube.com](https://youtube.com) while logged in
- Export cookies and save as `cookies.txt` inside the `backend/` folder

> ⚠️ Never share or commit your `cookies.txt` — it is already in `.gitignore`

---

### 5. Start the backend

```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

---

### 6. Load the Chrome extension

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer Mode** (top right toggle)
3. Click **Load Unpacked**
4. Select the `extension/` folder from this repo
5. Click the extension icon in the toolbar — the side panel opens!

<br/>

## 📁 Project Structure

```
know-the-page/
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── sidepanel.html
│   └── popup.js
│
└── backend/
    ├── main.py           ← FastAPI server
    ├── yt_rag.py         ← YouTube RAG bot with chat memory
    ├── retriever.py      ← Transcript fetcher + FAISS index builder
    ├── scraper.py        ← Playwright + BS4 page scraper
    ├── requirements.txt
    └── .env              ← your API key (never commit this)
```

<br/>

## 🚀 Usage

1. Start the backend server
2. Open Chrome and navigate to any webpage or YouTube video
3. Click the **Know the Page** extension icon
4. Type your question in the side panel and hit send
5. Ask follow-up questions — the bot remembers the conversation!
6. Click **New Session** to start fresh

<br/>

## ⚠️ Known Limitations

- Some websites block scrapers (Cloudflare-protected, paywalled, or auth-required pages) — the extension will show a friendly error message
- YouTube videos with no captions (not even auto-generated) cannot be processed
- The backend must be running locally for the extension to work

<br/>

## 🤝 Contributing

Contributions are welcome! Here are some areas where help would be amazing:

### 🔧 Open contribution areas

| Area | Description |
|---|---|
| **Scraper improvements** | Better handling of JS-heavy or bot-protected sites. Consider Playwright stealth mode or alternative scraping strategies |
| **RAG for webpages** | Currently uses text truncation for webpages — a full RAG pipeline for long articles/docs would improve accuracy |
| **Deployment** | A clean Docker setup or one-click deploy to Railway/Render with Playwright support |
| **More languages** | Add more transcript language codes to the multilingual support list |
| **Extension UI** | Improve the side panel design, add markdown rendering for responses |
| **Caching** | Cache FAISS indexes per video ID so repeated questions on the same video are faster |
| **Error UX** | More specific error messages for different failure cases |

### How to contribute

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "add: your feature"`
4. Push and open a Pull Request

Please open an issue first for major changes so we can discuss the approach.

<br/>

## 📄 License

MIT License — feel free to use, modify, and distribute.

<br/>

## 👨‍💻 Author

Built by **Chitransh Panwar** — B.Tech CSE @ JIIT Noida

[![GitHub](https://img.shields.io/badge/GitHub-Chitransh--Panwar-181717?style=flat&logo=github)](https://github.com/Chitransh-Panwar)

---

<p align="center">If you found this useful, give it a ⭐ — it helps a lot!</p>
