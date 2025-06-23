from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers.structured_output import structured_output_router   
from .routers.auth import router as auth_router
from .auth import auth_middleware


app = FastAPI()

# Add middleware
app.middleware("http")(auth_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(structured_output_router)
app.include_router(auth_router)

app.mount("/_next", StaticFiles(directory="./.next"), name="next_static")
app.mount("/", StaticFiles(directory="./.next/static"), name="next_root")

@app.get("/")
def serve_app():
    return FileResponse("./.next/server/pages/index.html")


