from fastapi import FastAPI
from .routers import videos, gemini, db
import logging
import colorlog
import sys
import pkg_resources
from api.core.settings import settings
log = logging.getLogger(__name__)
log.setLevel(settings.LOG_LEVEL) 

if not log.handlers: # Prevent adding multiple handlers if module is reloaded
    handler = logging.StreamHandler(sys.stdout)

    # log_color applies and reset removes color coding
    formatter = colorlog.ColoredFormatter( # Changed to ColoredFormatter
        '%(log_color)s%(levelname)s:%(reset)s  -  %(name)s - %(funcName)s - %(message)s',
        log_colors={
            'DEBUG': 'black',
            'INFO': 'bold_blue',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red,bg_white'

        }
    )    
    handler.setFormatter(formatter)
    log.addHandler(handler)

app = FastAPI(version=settings.VERSION, title="Gemini Playground Service", description="A service to interact with Gemini API and manage video uploads.", docs_url="/docs", redoc_url="/redoc")

app.include_router(videos.router)
app.include_router(gemini.router)
app.include_router(db.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():

    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    log.info(f"Current version: {settings.VERSION}")
    log.info(f"Installed packages: {installed_packages}")

    return {
        "version": settings.VERSION, 
        "python_version": sys.version,
        "installed_packages": installed_packages
        }