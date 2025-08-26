# AI-Powered Slide Deck Generator

This project is an intelligent slide deck generator that combines state-of-the-art language models with live web search and image fetching to produce a well-structured and visually styled PowerPoint presentation based on any user-input topic. It illustrates a practical AI integration pipeline, from prompt engineering and API orchestration to JSON validation and dynamic slide creation.

---

## Features

- Topic-based Slide Generation: Generate a 7-slide presentation covering overview, key points, and conclusion based on a topic provided at runtime.
- Live Web Search Integration: Dynamically fetch web snippets to inform and ground slide content.
- AI Content Generation: Uses an OpenRouter LLM API to generate concise, structured slide content adhering to a predefined JSON schema.
- Robust Schema Validation and Repair: Validates all generated slide content against JSON schema rules, repairing incomplete or missing content to ensure consistent slide count and formatting.
- Image-Powered Title Slide: Integrates Unsplash image search API to fetch a relevant image displayed on the title slide.
- User-Selectable Styles: Offers a choice of predefined color and font themes that apply uniformly across the presentation.
- PowerPoint Generation: Uses python-pptx to create a downloadable `.pptx` file with formatted titles, bullet points, and images.

---
### Usage:

Clone the repository, and once you're in the root directory, run the following command:

```bash
    python -m main
```

You'll then be prompted to select from a set of colours for the theme of the pptx. And then enter the topic of choice.

---

### Folder Structure:
```bash
    AI-Planet-Task/
    ├── api_clients/         # API integrations (LLM, web, image)
    ├── slide_generator/     # Slide creation using python-pptx
    ├── utils/               # Validation, prompt templates, helpers
    ├── output/              # Generated presentations and images
    ├── .env                 # Environment variables
    ├── main.py              # Entry point
    ├── requirements.txt     # Python dependencies
    └── README.md            # This file

```
---
### DEMO VIDEO
[Demo Video](https://www.youtube.com/watch?v=JhIPaZDfxPs)

[![Watch the video](https://img.youtube.com/vi/JhIPaZDfxPs/0.jpg)](https://www.youtube.com/watch?v=JhIPaZDfxPs)


