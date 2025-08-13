from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

app = FastAPI()

class Goal(BaseModel):
    goal: str

@app.get("/")
async def root():
    return {"message": "Use POST /run with {'goal': 'your_goal'}"}

@app.post("/run")
async def run_ai(goal: Goal):
    process = subprocess.run([
        sys.executable,
        "-m",
        "self_editing_ai.src.cli",
        "--goal",
        goal.goal,
    ], capture_output=True, text=True)
    return {"stdout": process.stdout, "stderr": process.stderr}
