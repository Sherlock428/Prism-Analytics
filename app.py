from fastapi import FastAPI
from Database.db import init_db
from Routes.auth import router as auth
app = FastAPI(
    title="feedbacks",
    description="Feedbacks for company",
    version="0.1.0"
)

app.include_router(auth)

@app.get("/")
def read_root():
    return {'message': 'Hello World'}

if __name__ == "__main__":
    import uvicorn
    # init_db()
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)