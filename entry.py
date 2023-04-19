import uvicorn
from app import create_app
from app.config import cfg

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=cfg.server_host,
        port=cfg.server_port,
        log_level='info',
        # reload=True,
    )