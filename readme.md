# Recipe RAG System
Inspired by course: [Understanding LLMs](https://cogsciprag.github.io/Understanding-LLMs-course/intro.html)

## Project Overview

A production-ready Retrieval-Augmented Generation (RAG) system specialized for recipe queries. This system combines vector search with language model generation to provide contextually relevant recipe information based on user queries.

### Key Features

- **Efficient Information Retrieval**: Semantic search using BGE embeddings to find the most relevant recipes
- **Contextual Response Generation**: LLM-powered responses that incorporate retrieved recipe information
- **Scalable API Architecture**: FastAPI-based RESTful API with proper error handling and documentation
- **Fully Containerized**: Docker and Docker Compose setup for easy deployment
- **Comprehensive Testing**: Unit and integration tests covering core functionalities
- **Monitoring Setup**: Prometheus and Grafana integration (optional)

## Architecture

The system consists of two main components:

1. **Recipe RAG Core**: Handles document indexing, retrieval, and response generation
2. **API Server**: Exposes the RAG functionality through REST endpoints

## Technology Stack

- **Vector Search**: LlamaIndex with HuggingFace embeddings (BGE model)
- **Language Model**: Microsoft Phi-3-mini-4k-instruct
- **API Framework**: FastAPI
- **Dataset**: HuggingFace Recipe NLG Lite
- **Containerization**: Docker & Docker Compose
- **Responsive Web Design**: javaScript, react, npm
- **Monitoring**: Prometheus & Grafana (optional)



## Deployment

The system can be deployed with a single command:

```bash
docker-compose up -d
```

This will start the API server and (optionally) the monitoring stack.

## Future Improvements

- Implement caching layer for frequently asked questions
- Add a vector database for improved scalability
- Implement a feedback loop for continuous improvement

