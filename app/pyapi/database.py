from supabase import Client, create_client
from dotenv import load_dotenv
import numpy as np
import os
import json

load_dotenv()

api_url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_API_KEY")

def create_supabase_client():
    pass
