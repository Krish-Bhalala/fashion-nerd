from fastapi import FastAPI

# LLM modules
from models.fashionclip import FashionCLIPModel

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # app.state.fashionclip_model = None
    app.state.fashionclip_model = FashionCLIPModel()
    app.state.llm_model = None      #!Placeholder