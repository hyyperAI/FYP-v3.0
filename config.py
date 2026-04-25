from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")

if not MINIMAX_API_KEY:
    raise ValueError("Missing MINIMAX_API_KEY in .env file")