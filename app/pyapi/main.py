from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.chat import chat_router
from .routers.structured_output import structured_output_router    


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def health_check():
    return 'Health check complete'
app.include_router(chat_router)
app.include_router(structured_output_router)

