# 🦜️🔗 FastAPI + Next.js Starter Template for schedule constraint encoding

This template scaffolds a FastAPI + Next.js starter app. It showcases how to use and combine LangChain modules for several
use cases. Specifically:

## 🚀 Getting Started

First, clone this repo and download it locally.

Next, you'll need to set up environment variables in your repo's `.env.local` file. Copy the `.env.example` file to `.env.local`.
To start with the basic examples, you'll just need to add your OpenAI API key.

Next, install the required packages using your preferred package manager (e.g. `yarn`).

Set up a virtual python environment and activate it

cd into app/pyapi and install requirements.txt

```bash
fastapi run main.py
```

Now you're ready to run the development server:

```bash
yarn dev
```
**Backend API is now powered by FastAPI (Python). All API endpoints are available under `/pyapi/` (e.g., `/pyapi/chat`). Make sure to run the FastAPI server alongside Next.js and configure a proxy if needed.**

## 🧱 Structured Output

The functionality of this is still very basic. The chat will take in a list of natural language constraints and it will return a list of json objects

## Continiued development

- Authentication
- Data Persistence
