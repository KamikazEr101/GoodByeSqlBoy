from fastapi import FastAPI
from router.nl_to_sql import router

app = FastAPI(
    title="NL to SQL API",
    description="API for converting natural language queries to SQL statements",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)