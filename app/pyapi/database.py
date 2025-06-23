from supabase import Client, create_client
from dotenv import load_dotenv
import numpy as np
import os
import json

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_JWT_SECRET]):
    raise EnvironmentError("One or more Supabase environment variables are missing.")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
