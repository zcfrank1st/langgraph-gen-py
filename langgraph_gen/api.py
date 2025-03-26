from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from langgraph_gen.generate import generate_from_spec

app = FastAPI(
    title="LangGraph Generator API",
    description="API for generating LangGraph code stubs from specifications",
    version="1.0.0"
)

class GenerateRequest(BaseModel):
    spec: str
    language: Literal["python", "typescript"] = "python"
    format: Literal["yaml", "json"] = "yaml"
    stub_module: Optional[str] = None

@app.post("/generate")
async def generate_code(request: GenerateRequest):
    try:
        generated_code = generate_from_spec(
            request.spec,
            request.format,
            templates=["stub", "implementation"],
            language=request.language,
            stub_module=request.stub_module
        )
        return {
            "stub": generated_code[0],
            "implementation": generated_code[1]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 