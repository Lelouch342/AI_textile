# 🧵 AI-Driven Textile Design Generator

## 🪡 Overview

This project aims to develop an **AI-driven design system** that generates **high-resolution, production-ready textile surface designs** inspired by **India’s rich craft traditions**.

Users can create **custom prints and embroidery motifs** by giving **text or visual prompts** — including regional and craft-specific terminology such as *Ajrakh*, *Kalamkari*, *Chikankari*, and *Kantha*.  
The goal is to **bridge traditional Indian aesthetics** with **modern AI and design workflows**, enabling designers and artisans to create culturally rooted textile designs quickly and intuitively.

---

## 🌸 Core Objectives

1. **AI-Based Textile Generation**  
   Generate textile surface patterns and embroidery motifs using AI image generation models.

2. **Cultural Authenticity**  
   Support Indian craft styles, motifs, and color schemes using curated datasets and craft-specific terminology.

3. **Multilingual Support**  
   Accept text prompts in multiple Indian languages, automatically interpreting craft-related terms.

4. **Visual + Text Input**  
   Allow users to upload a reference image or sketch along with textual instructions.

5. **Production-Ready Output**  
   Ensure outputs are high-resolution, clean, and suitable for direct textile production or digital printing.

---

## 🚧 Current Prototype Status (Working)

### ✅ Implemented So Far

- **FastAPI Backend**
  - Accepts text prompts and sends them to the **Hugging Face Inference API**.
  - Uses the model [`stabilityai/stable-diffusion-xl-base-1.0`](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0).
  - Returns the generated image as a **Base64-encoded string**.
  - CORS enabled for local frontend testing.
  - Secure environment variable management using `.env`.

- **React Frontend (Vite + CSS Modules)**
  - Clean UI for prompt input and image display.
  - “Generate” button with a loading state.
  - Displays AI-generated design image.
  - Uses simple CSS Modules instead of Tailwind for styling.

- **Integration**
  - End-to-end tested: frontend → backend → Hugging Face → image displayed.
  - Currently works for free-tier Hugging Face models (with some restrictions).

---

## 🧠 Planned Next Steps

| Feature | Description |
|----------|--------------|
| **LLM Integration** | Use a lightweight LLM (e.g., Mistral or Llama) to enhance text prompts with craft-specific context before generation. |
| **RAG System** | Build a Retrieval-Augmented Generation setup trained on Indian craft and textile metadata for accurate style reproduction. |
| **Local Image Generation** | Use Hugging Face `diffusers` library for free local model inference instead of paid API. |
| **Multilingual Input** | Integrate a translation layer (e.g., MarianMT) for Hindi, Marathi, Tamil, etc. |
| **Design Tools** | Add color palette selection, motif size control, and pattern repetition options. |
| **UI Enhancements** | Build a gallery and export tool for downloading high-res outputs. |

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React + Vite + CSS Modules |
| **Backend** | FastAPI (Python) |
| **AI Model API** | Hugging Face Inference API |
| **Environment Variables** | python-dotenv |
| **Planned (Future)** | Hugging Face `diffusers`, LangChain, Transformers |
| **Runtime** | Node.js 18+ / Python 3.10+ |

---

## 🧩 Project Structure

```
project-root/
│
├── backend/
│   ├── main.py               # FastAPI backend
│   ├── .env                  # Contains HF_API_KEY
│   ├── requirements.txt
│   └── __init__.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.module.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🧰 Environment Setup

### 🐍 Backend Setup (FastAPI)

#### 1. Create Virtual Environment
```bash
cd backend
python -m venv .venv
```

#### 2. Activate Virtual Environment
**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv requests
```

#### 4. Add Hugging Face API Key
Create a `.env` file in `/backend`:
```
HF_API_KEY=your_huggingface_api_key_here
```

#### 5. Run Backend
```bash
uvicorn main:app --reload
```

Backend runs at **http://localhost:8000**

---

### ⚛️ Frontend Setup (React + Vite)

#### 1. Navigate to Frontend
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Run Development Server
```bash
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## 🔗 Connecting Frontend and Backend

The frontend makes a POST request to:
```
http://localhost:8000/generate
```

Example body:
```json
{
  "prompt": "Ajrakh block print pattern in indigo and maroon"
}
```

The backend calls the Hugging Face API, retrieves an image, encodes it as Base64, and returns:
```json
{
  "image": "data:image/png;base64,...."
}
```

---

## 🧵 Future System Architecture (Planned)

```
         ┌────────────────────────────┐
         │  Frontend (React + Vite)   │
         │  - Prompt input UI         │
         │  - Image preview           │
         │  - Craft & color options   │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  FastAPI Backend           │
         │  - Input validation        │
         │  - Craft-aware LLM (RAG)   │
         │  - Diffusers pipeline      │
         │  - Local / HF inference    │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │  AI Models                 │
         │  - Stable Diffusion XL     │
         │  - Craft Embedding (RAG)   │
         │  - Text-to-Image Pipeline  │
         └────────────────────────────┘
```

---

## 🖼️ Preview (Coming Soon)
*Example of generated textile patterns and motifs will be added here.*

---

## ✨ Author
**Aditya Oke**

---

## 🧭 License
This project is open-sourced under the MIT License.
