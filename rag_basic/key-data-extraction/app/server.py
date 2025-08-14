from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from extract import chain, Data

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

class ExtractRequest(BaseModel):
    text: str

class ExtractResponse(Data):
    pass

@app.post("/extract", response_model=ExtractResponse)
async def extract_people(request: ExtractRequest):
    result = chain.invoke({"text": request.text})
    return result

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
