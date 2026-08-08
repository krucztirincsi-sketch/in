from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

from backend.lom import generate_execution_plan
from backend.compiler import SLCCompiler

app = FastAPI(title="Subjective Logic Compiler API")

# Allow CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

compiler = SLCCompiler()

class CompileRequest(BaseModel):
    intent: str
    context: Dict[str, Any]
    data: List[Dict[str, Any]]

class CompileResponse(BaseModel):
    html_bundle: str
    execution_plan: dict

@app.post("/compile", response_model=CompileResponse)
async def compile_logic(request: CompileRequest):
    try:
        # 1. Infer schema from data (very naive for PoC)
        data_schema = {}
        if request.data:
            for k, v in request.data[0].items():
                data_schema[k] = type(v).__name__

        # 2. Pass to LOM (Logic to Ontology Mapper)
        execution_plan = generate_execution_plan(
            intent=request.intent,
            context=request.context,
            data_schema=data_schema
        )

        # 3. Compile the plan into a micro-app UI
        html_bundle = compiler.compile(execution_plan, request.data)

        return CompileResponse(
            html_bundle=html_bundle,
            execution_plan=execution_plan
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
