# Assignment 3 – Project I Am Proud Of

## Voxora – FitNova Call Intelligence Platform

🔗 **Live:** https://voxora-a0ss.onrender.com
💻 **GitHub:** https://github.com/Reethikaa05/Voxora

Voxora is an AI-powered call-intelligence platform that transforms customer conversations into structured insights and actionable feedback. I worked on the backend APIs, the AI-powered processing workflows, data handling and application integration.

### Pipeline
```mermaid
flowchart LR
  A[Call audio] --> B[Ingestion and processing]
  B --> C[Whisper speech-to-text]
  C --> D[Speaker diarization and segmentation]
  D --> E[PII detection and redaction]
  E --> F[Rubric-based evaluation]
  F --> G[Issue classification + timestamps + evidence]
  G --> H[API / dashboard]
```

### Why it is hard (3 lines)
1. It turns unstructured conversation data (noisy audio, many speakers) into meaningful, structured insights backed by timestamps and evidence.
2. It integrates multiple backend and AI components (transcription, diarization, PII redaction, scoring) into one coherent, end-to-end workflow.
3. It needed careful data validation, debugging and reliability work to run as a deployed application, while keeping sensitive customer data protected.

### Related security-focused project
**ShopMCPilot** – a secure, read-only MCP integration with PII masking and AIMD-based rate limiting: https://github.com/Reethikaa05/ShopMCPilot
