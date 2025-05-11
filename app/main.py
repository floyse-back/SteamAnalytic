from fastapi import FastAPI

from app.api.register_exceptions import register_exceptions
from app.api.v1 import steam, auth, analytics,users,admin,email
from app.api.middleware.register_middleware import register_middleware
from app.utils.config import ServicesConfig

app = FastAPI()

service_config = ServicesConfig()

@app.get("/health_check")
async def health_check():
    return {"status": "ok"}

app.include_router(steam.router,prefix=f"{service_config.steam_service.path}",tags=service_config.steam_service.tags)
app.include_router(analytics.router, prefix=f"{service_config.analytic_service.path}",tags=service_config.analytic_service.tags)
app.include_router(auth.router, prefix=f"{service_config.auth_service.path}",tags=service_config.auth_service.tags)
app.include_router(users.router, prefix=f"{service_config.users_service.path}",tags=service_config.users_service.tags)
app.include_router(admin.router, prefix=f"{service_config.admin_service.path}",tags=service_config.admin_service.tags)
app.include_router(email.router, prefix=f"{service_config.notification_service.path}",tags=service_config.notification_service.tags)

register_middleware(app)
register_exceptions(app)