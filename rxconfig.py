import reflex as rx
from config import get_settings

settings = get_settings()

config = rx.Config(
    app_name=settings.app_name,
    db_url=settings.database_url,
    api_url=settings.api_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)