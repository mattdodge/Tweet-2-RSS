from gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="qUiCMqg0f0oKw8uQv1XhLmVZZS2ahLhjERXIjDxZ", no_datastore=True)
    return app