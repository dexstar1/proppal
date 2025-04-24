from main import app

# Export the ASGI application for Vercel
handler = app.get_asgi_application()