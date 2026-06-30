from aura.api.app_factory import create_app
from aura.config.settings import Settings


settings = Settings.from_env()
app = create_app(settings)

if __name__ == "__main__":
    app.run(host=settings.flask_host, port=settings.flask_port)
