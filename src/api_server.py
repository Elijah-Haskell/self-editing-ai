from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys
import os

app = FastAPI()

class Goal(BaseModel):
    goal: str

@app.get("/")
async def root():
    return {"message": "Use POST /run with {'goal': 'your_goal'}"}

@app.post("/run")
async def run_ai(goal: Goal):
    # Determine the path to the zip file relative to this file
    zip_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "self_editing_ai.zip"))
    # Prepare environment to include zip in PYTHONPATH
    env = dict(os.environ)
    env["PYTHONPATH"] = zip_path + os.pathsep + env.get("PYTHONPATH", "")
    process = subprocess.run([
        sys.executable,
        "-m",
        "self_editing_ai.src.cli",
        "--goal",
        goal.goal,
    ], capture_output=True, text=True, env=env)
    return {"stdout": process.stdout, "stderr": process.stderr}
