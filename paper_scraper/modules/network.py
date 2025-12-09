import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .config import S2_API_KEY

def get_robust_session():
    """
    Sessão com Retry automático para lidar com instabilidades de rede.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1, 
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
    
    session.headers.update(headers)
    return session
