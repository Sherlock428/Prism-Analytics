from fastapi import FastAPI


app = FastAPI(
    title="feedbacks",
    description="Feedbacks for company",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {'message': 'Hello World'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)