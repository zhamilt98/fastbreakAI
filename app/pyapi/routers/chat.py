from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

chat_router = APIRouter()

TEMPLATE = """Extract the requested fields from the input.

The field "entity" refers to the first mentioned entity in the input.

Input:

{input}"""

@chat_router.post("/chat")
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages", [])
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        current_message_content = messages[-1]["content"]

        prompt = PromptTemplate.from_template(TEMPLATE)

        model = ChatOpenAI(
            temperature=0.8,
            model="gpt-4o-mini"
        )

        # Simulate structured output with Pydantic validation
        chain = prompt | model

        result = await chain.ainvoke({
            "input": current_message_content
        })

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)