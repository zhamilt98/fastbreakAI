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

The second example shows how to have a model return output according to a specific schema using OpenAI Functions.
Click the `Structured Output` link in the navbar to try it out:

![A streaming conversation between the user and an AI agent](/public/images/structured-output-conversation.png)

The chain in this example uses a [popular library called Zod](https://zod.dev) to construct a schema, then formats it in the way OpenAI expects.
It then passes that schema as a function into OpenAI and passes a `function_call` parameter to force OpenAI to return arguments in the specified format.

For more details, [check out this documentation page](https://js.langchain.com/docs/how_to/structured_output).
