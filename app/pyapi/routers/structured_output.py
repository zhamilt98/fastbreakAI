from fastapi import APIRouter, HTTPException
from app.pyapi.models.schemas import (
    ChatRequest, StructuredOutput, StructuredRequest,
    TemporalConstraint, VenueConstraint, TeamConstraint, GeneralConstraint
)
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import os
import json
from app.pyapi.database import get_supabase
from app.pyapi.deps import user_dependency,oauth2_bearer_dependency

load_dotenv()
supabase=get_supabase()
structured_output_router = APIRouter()

def get_schema_text(model, prefix=""):
    """
    Convert the model's schema to a JSON string for embedding.
    """
    schema = model.schema()
    return json.dumps(schema, indent=2, sort_keys=True)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def detect_constraint_type(message_content: str):
    """
    Use OpenAI embeddings to semantically match user input to constraint schemas.
    """
    content = (message_content or "")
    constraint_models = [
        TemporalConstraint,
        VenueConstraint,
        TeamConstraint,
        GeneralConstraint,
    ]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Get embedding for user input
    user_emb = client.embeddings.create(
        input=[content],
        model="text-embedding-3-small"
    ).data[0].embedding

    # Get embeddings for each constraint schema
    schemas_text = [get_schema_text(model) for model in constraint_models]
    schema_embs = client.embeddings.create(
        input=schemas_text,
        model="text-embedding-ada-002"
    ).data

    # Compute similarities
    similarities = [
        cosine_similarity(user_emb, np.array(schema_emb.embedding))
        for schema_emb in schema_embs
    ]
    best_idx = int(np.argmax(similarities))
    return constraint_models[best_idx]

@structured_output_router.post("/chat/structured_output", response_model=StructuredOutput)
async def structured_output_endpoint(request: StructuredRequest,user:user_dependency):
    # Example: return a dummy structured output
    structured_outputs = []
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not request.messages or len(request.messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided.")
    if len(request.messages) == 1:
        msg = request.messages[0]
        constraint_model = detect_constraint_type(msg.content or "")
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text and should convert it into the given structure."},
                {"role": "user", "content": msg.content}
            ],
            text_format=constraint_model  # Embed the constraint object schema
        )
        structured_output = response.output_parsed
        result = StructuredOutput(constraints=[structured_output])
        supabase.table("constraints").insert({
                "constraint_json": result.model_dump(mode='json'),
                "user_id": user.get('id'),
            }).execute()
        return result
    else:
        for msg in request.messages[-1].content.split(','):
            constraint_model = detect_constraint_type(msg)
            response = client.responses.parse(
                model="gpt-4o-mini",
                instructions="Extract the requested fields from the input.",
                input=[
                    {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text and should convert it into the given structure."},
                    {"role": "user", "content": msg}
                ],
                text_format=constraint_model  # Embed the constraint object schema
            )
            structured_output = response.output_parsed
            structured_outputs.append(structured_output)
            result = StructuredOutput(constraints=structured_outputs)
            supabase.table("constraints").insert({
                "constraint_json": result.model_dump(mode='json'),
                "user_id": user.get('id'),
            }).execute()
    return result