from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
import logging

# Импорт роутеров
from routers import auth, links, products, orders, messages, complaints, suppliers
from config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Supplier-Restaurant MVP API",
    description="API для взаимодействия поставщиков и ресторанов",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


# Подключение роутеров
app.include_router(auth.router)
app.include_router(links.router)
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(messages.router)
app.include_router(complaints.router)

@app.on_event("startup")
async def startup_event():
    """Инициализация БД при старте приложения"""
    logger.info("🚀 Starting application...")
    try:
        init_db()
        logger.info("✅ Application started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise

@app.get("/")
def read_root():
    return {
        "message": "Supplier-Restaurant MVP API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
