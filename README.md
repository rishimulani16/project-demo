# 🧠 End-to-End RAG Knowledge Assistant

## 🌐 Live Demo

> **Try the app right now — no installation required!**
>
> 👉 **[http://54.163.208.218:8502/](http://54.163.208.218:8502/)**
>
> Ask any question about the knowledge base and get AI-powered, document-grounded answers instantly.

---

![RAG Assistant](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)
![AWS EC2](https://img.shields.io/badge/AWS-EC2%20Deployed-orange.svg)
![LLaMA](https://img.shields.io/badge/LLM-LLaMA--3.3--70b-purple.svg)

---

## 🌟 Project Overview

This application bridges the gap between static documents and interactive AI. By leveraging state-of-the-art Large Language Models (LLMs) and Vector Databases, it reads your documents, understands their context, and answers user queries with pinpoint precision.

### Key Features
- **Modern Streamlit Frontend:** A beautiful, responsive UI featuring custom CSS, glassmorphism elements, and chat-like interactions.
- **FastAPI Backend:** A lightning-fast REST API to handle processing and programmatic access.
- **Advanced RAG Pipeline:** Intelligent document chunking, semantic search, and prompt-grounded LLM inference.
- **Dockerized Architecture:** Seamlessly containerized for development, distribution, and production deployment.
- **AWS EC2 Deployment:** Live on the cloud using a free-tier ARM-based `t4g.small` Graviton instance.

---

## 🏗️ How RAG (Retrieval-Augmented Generation) is Implemented

The RAG pipeline is the brain of this application, meticulously crafted in the `app/rag` module. Here is the step-by-step implementation data flow:

1. **Document Loading (`loader.py`):**
   Using `pypdf`, the system ingests the raw target PDF document (`knowledge.pdf`) and extracts readable text.
2. **Text Chunking (`chunker.py`):**
   The extracted text is broken down into manageable, overlapping segments (500 tokens chunk size, 50 tokens overlap) using LangChain's text splitters. This ensures context is not lost between paragraphs.
3. **Embeddings Generation (`embedding.py`):**
   The chunks are converted into high-dimensional vector representations. We utilize `SentenceTransformers` with the open-source `all-MiniLM-L6-v2` model from HuggingFace to create dense semantic embeddings — running **fully locally** with no API key required.
4. **Vector Database & Storage (`vectorstore.py`):**
   The generated embeddings are indexed and stored using **FAISS** (Facebook AI Similarity Search) running on CPU. This allows for blazingly fast nearest-neighbor similarity searches when a user asks a query.
5. **Inference & Generation (`engine.py`):**
   Upon receiving a user query, the FAISS vector store retrieves the top `k` most similar document chunks. These chunks are injected into a strict prompt template alongside the user's question. The prompt is then passed to the **Groq API** powering the blazing fast **LLaMA-3.3-70b-versatile** model to synthesize a grounded, accurate answer without hallucination.

---

## 📁 Project Structure

```
end-to-end/
├── app/
│   ├── api/
│   │   └── main.py           # FastAPI app with /query endpoint
│   ├── frontend/
│   │   └── streamlit_app.py  # Streamlit chat UI
│   └── rag/
│       ├── engine.py         # Core RAG orchestration
│       ├── embedding.py      # HuggingFace embedding wrapper
│       ├── chunker.py        # LangChain text splitter
│       ├── loader.py         # PDF loader using pypdf
│       └── vectorstore.py    # FAISS vector store
├── data/
│   └── knowledge.pdf         # Your target PDF document
├── Docker/
│   └── Dockerfile
├── .env                      # API keys (never commit this!)
└── requirements.txt
```

---

## ⚙️ Environment Setup

Create a `.env` file in the project root with the following:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

> ⚠️ **Important:** Never commit your `.env` file to GitHub. Add it to `.gitignore`.

Get your free Groq API key at [console.groq.com](https://console.groq.com).

---

## 🐳 Docker: Local Setup & Image Creation

Containerizing the application ensures that it runs seamlessly across any environment. Both the FastAPI backend and the Streamlit frontend run inside a single container.

### 1. Building the Docker Image Locally

```bash
docker build -t rag-app:latest -f Docker/Dockerfile .
```

### 2. Running Locally for Testing

```bash
docker run -p 8000:8000 -p 8501:8501 rag-app:latest
```

- **Streamlit UI:** http://localhost:8501
- **FastAPI Docs:** http://localhost:8000/docs

> ⚠️ **Port Conflict Fix:** If you get `address already in use`, find and kill the blocking process:
> ```bash
> lsof -i :8501   # find the PID
> kill -9 <PID>   # kill it
> ```

---

## 🚀 Pushing the Image to Docker Hub

> ⚠️ **Mac M1/M2/M3 Users:** The image built on Apple Silicon is ARM-based. If you are deploying to an Intel/AMD Linux server, you must rebuild with the `--platform` flag:
> ```bash
> docker build --platform linux/amd64 -t <your-username>/rag-app:latest -f Docker/Dockerfile .
> ```

1. **Log in to Docker Hub:**
   ```bash
   docker login
   ```

2. **Tag the Image:**
   ```bash
   docker tag rag-app:latest <your-dockerhub-username>/rag-app:latest
   ```

3. **Push the Image:**
   ```bash
   docker push <your-dockerhub-username>/rag-app:latest
   ```

Your compressed image (~3 GB) will be publicly available at `hub.docker.com/r/<your-username>/rag-app`.

---

## ☁️ Deployment on AWS EC2 (Free Tier — $0.00/month)

This application is deployed on AWS EC2 using the **ARM-based `t4g.small`** instance.

### ⚡ Why `t4g.small` (ARM) and Not `t2.micro` (x86)?

| Feature | `t2.micro` (x86) | `t4g.small` (ARM) ✅ |
|---|---|---|
| **Architecture** | Intel/AMD (x86_64) | ARM (aarch64) |
| **RAM** | 1 GB | 2 GB |
| **Free Until** | 12 months from signup | December 31, 2026 |
| **Mac M-chip compatible** | ❌ Requires image rebuild | ✅ Runs natively |
| **Handles ML models** | ❌ Crashes (not enough RAM) | ✅ Runs comfortably |

Since this project is built on a MacBook M-series (Apple Silicon), the Docker image is natively ARM-compatible. Using `t4g.small` avoids a full image rebuild and provides double the RAM to handle the HuggingFace embedding model and FAISS.

---

### Step 1: Launch the EC2 Instance

1. Log into AWS Console → Search **EC2** → Click **Launch Instance**
2. **Name:** `rag-app-server`
3. **AMI:** Ubuntu 24.04 LTS
4. **Architecture:** ⚠️ Change to **64-bit (Arm)** ← this is the crucial step
5. **Instance Type:** `t4g.small`
6. **Key Pair:** Create a new key pair and download the `.pem` file safely
7. **Security Group — Add these inbound rules:**

   | Type | Port | Source |
   |---|---|---|
   | SSH | 22 | 0.0.0.0/0 |
   | HTTP | 80 | 0.0.0.0/0 |
   | Custom TCP | 8000 | 0.0.0.0/0 |
   | Custom TCP | 8501 | 0.0.0.0/0 |
   | Custom TCP | 8502 | 0.0.0.0/0 |

8. **Storage:** ⚠️ Change from `8` GiB to **`30` GiB** (the Docker image is ~9 GB uncompressed; 30 GB is the free-tier maximum)
9. Click **Launch Instance**

---

### Step 2: Connect and Install Docker

Click **Connect** on the EC2 dashboard → **EC2 Instance Connect** → **Connect**

```bash
sudo apt update && sudo apt install docker.io -y
```

---

### Step 3: Pull and Run the Container

```bash
# Pull the image from Docker Hub
sudo docker pull <your-dockerhub-username>/rag-app:latest

# Run with auto-restart so the app survives server reboots
sudo docker run -d --restart unless-stopped \
  -p 8001:8000 \
  -p 8502:8501 \
  <your-dockerhub-username>/rag-app:latest
```

---

### Step 4: Access Your Live Application

Go to your EC2 Dashboard, copy the **Public IPv4 address**, and open:

- **Streamlit UI:** `http://<EC2-PUBLIC-IP>:8502`
- **FastAPI Docs:** `http://<EC2-PUBLIC-IP>:8001/docs`

> 📝 **Note on IP Address:** AWS assigns a new Public IP every time you stop and start the instance. Use an **Elastic IP** (~$3.60/month when stopped) if you need a permanent address. For zero cost, leave the instance running 24/7.

---

### 💰 AWS Free Tier Cost Breakdown

| Resource | Free Tier Limit | What We Use | Cost |
|---|---|---|---|
| EC2 `t4g.small` compute | 750 hrs/month | 744 hrs (24/7) | **$0.00** |
| EBS Storage | 30 GB/month | 30 GB | **$0.00** |
| Public IPv4 (running) | 750 hrs/month | 744 hrs (24/7) | **$0.00** |
| **Total** | | | **$0.00** |

> ⚠️ **Important:** If you **stop** the EC2 instance, EBS storage and the idle IP address will start accruing small charges. For zero cost, keep the instance running 24/7 or **terminate** it when not needed (you will lose all data on the server).

---

## 🔧 Useful Docker Commands

```bash
# Check running containers
sudo docker ps

# View live container logs
sudo docker logs -f <container_id>

# Stop all containers
sudo docker stop $(sudo docker ps -q)

# Remove all stopped containers
sudo docker rm $(sudo docker ps -aq)
```

---

*Built with ❤️ utilizing modern full-stack AI methodologies.*
