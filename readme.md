---
title: {{title}}
emoji: {{emoji}}
colorFrom: {{colorFrom}}
colorTo: {{colorTo}}
sdk: {{sdk}}
sdk_version: "{{sdkVersion}}"
app_file: app.py
pinned: false
---


# Recipe RAG System  
Inspired by course: [Understanding LLMs](https://cogsciprag.github.io/Understanding-LLMs-course/intro.html)  

## Project Overview  
This project is a cutting-edge **Retrieval-Augmented Generation (RAG)** system designed for **recipe retrieval** and **context-aware response generation**.  
It integrates **Llama** as the core language model, **MiniLM embeddings** for efficient retrieval, and **FAISS** for vector search, all exposed through a high-performance **FastAPI server**.  

✅ **Tested on MacBook Air M1** — Runs smoothly with efficient memory usage!  
✅ **Easily adaptable** to other domains like **automotive repair, industrial manufacturing, or medical Q&A** — just swap datasets and models.  

---

## Key Features  
- **Advanced RAG Architecture** – Llama LLM + MiniLM embeddings + FAISS retrieval  
- **FastAPI-Powered API** – Low-latency, production-ready RESTful service  
- **Fully Modular** – Users can easily swap models, embeddings, and datasets  
- **Optimized for Apple Silicon** – Runs smoothly on **MacBook Air M1** without GPU  
- **Dockerized Deployment** – Ready to deploy with **Docker & Docker Compose**  
- **React Frontend** – Chat-based UI for recipe exploration  

---

## Technology Stack  

| **Component**      | **Technology**                                    |
|--------------------|--------------------------------------------------|
| **Language Model** | Llama (Meta AI)                                  |
| **Vector Search**  | FAISS + LlamaIndex                               |
| **Embeddings**     | `sentence-transformers/all-MiniLM-L6-v2`         |
| **API Framework**  | FastAPI                                          |
| **Frontend**      | JavaScript, React.js                             |
| **Database**      | FAISS for scalable vector search                 |
| **Containerization** | Docker & Docker Compose                       |

---

## System Architecture  

### 1️⃣ Backend (RAG Core + API Server)  
- **Retrieval**: FAISS + MiniLM embeddings for fast **semantic search**  
- **Generation**: Llama model generates responses with retrieved **context**  
- **API Interface**: FastAPI exposes endpoints for easy **integration**  

### 2️⃣ Frontend (React UI)  
- **Conversational chat interface**  
- **Displays AI-generated recipes and contextual responses**  

---

## Demo Preview  
Below are sample screenshots showcasing the system in action. The images are stored in the `assets/` folder:  

| **Demo**                  | **Description**                          |
|---------------------------|------------------------------------------|
| ![Demo 1](https://github.com/whitney-house/RAG_system/blob/main/fronted/src/assets/demo1.png) | Design          |
| ![Demo 2](https://github.com/whitney-house/RAG_system/blob/main/fronted/src/assets/demo2.png) | Recipe retrieval in action               |
| ![Demo 3](https://github.com/whitney-house/RAG_system/blob/main/fronted/src/assets/demo3.png) | Personalized recipe recommendations   |

---


## Future Improvements
✅ Agent Integration – Adding AI Agents for more complex reasoning and interactions  
✅ Cross-Domain Support – Expand to industrial, automotive, and healthcare applications  
✅ Fine-Tuning Support – Enable custom Llama training for domain-specific use cases  
✅ Enhanced Vector Search – Move beyond FAISS to more scalable solutions  

## License & Usage
This project is open for customization—feel free to replace models and datasets for your own use.  
**⚠️ Do not use this for commercial purposes without permission. 🚀**

