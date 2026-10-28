"""
WebDriver factory for setting up headless or headed Chrome instances.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def create_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")

    known_driver_path = r"C:\Users\SAIL\.cache\selenium\chromedriver\win64\156.0.8078.73\chromedriver.exe"
    if os.path.exists(known_driver_path):
        service = Service(executable_path=known_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(2)
    return driver

def get_atm_app_url():
    """
    Returns application URL. Defaults to localhost:8000 if server is active,
    or falls back to local file URI.
    """
    if os.environ.get("USE_LOCALHOST", "").lower() in ("1", "true", "yes"):
        return "http://localhost:8000"
    
    # Check if localhost:8000 is reachable, otherwise use file URL
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "atm_app"))
    html_path = os.path.join(base_dir, "index.html")
    return f"file:///{html_path.replace(os.sep, '/')}"


