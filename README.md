# 🦜️🔗 FastAPI + Next.js Starter Template for schedule constraint encoding

This template scaffolds a FastAPI + Next.js starter app. It showcases how to use and combine LangChain modules for several
use cases. Specifically:

## 🚀 Getting Started

First, clone this repo and download it locally.

Second, set up your supabase account

Next, you'll need to set up environment variables in your repo's `.env` file. Copy the `.env.example` file to `.env`.
To start with the basic examples, you'll just need to add your OpenAI API key.

Next, install the required packages using your preferred package manager (e.g. `yarn`).

Now you're ready to run the development server:

```bash
yarn install
yarn dev
```
open a new terminal
Set up a virtual python environment and activate it
install requirements.txt
```bash
fastapi run ./app/pyapi/main.py
```


**Backend API is now powered by FastAPI (Python). All API endpoints are available under `/pyapi/` (e.g., `/pyapi/chat`). Make sure to run the FastAPI server alongside Next.js and configure a proxy if needed.**

## 🧱 Structured Output

The functionality of this is still very basic. The chat will take in a list of natural language constraints and it will return a list of json objects

## Continiued development

- Authentication
- Data Persistence
