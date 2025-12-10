from supabase import create_client, Client
from app.core.config import settings

# Initialize Supabase client
supabase: Client = None

def get_supabase() -> Client:
    """Get Supabase client instance"""
    global supabase
    if supabase is None:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase
