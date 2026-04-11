from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

state_data = {
    "step": 0, "done": False, "task": "easy", 
    "current_email": None, "correct": 0
}

EMAILS = {
    "easy": [
        {"subject": "Win money now", "body": "Click here to claim prize", "label": "spam"},
        {"subject": "Meeting at 10", "body": "Project discussion", "label": "important"},
        {"subject": "Hello", "body": "How are you?", "label": "normal"},
    ],
    "medium": [
        {"subject": "Limited offer", "body": "Buy now", "label": "spam"},
        {"subject": "Server issue", "body": "Fix ASAP", "label": "important"},
        {"subject": "Weekend plan", "body": "Let's go out", "label": "normal"},
    ],
    "hard": [
        {"subject": "Project update", "body": "Deadline tomorrow", "label": "important"},
        {"subject": "Free gift inside", "body": "Open now", "label": "spam"},
        {"subject": "Team lunch", "body": "Tomorrow 1 PM", "label": "normal"},
    ]
}

class ActionInput(BaseModel):
    action: str

@app.post("/reset")
@app.get("/reset")
def reset():
    global state_data
    task = random.choice(["easy", "medium", "hard"])
    email = random.choice(EMAILS[task])
    
    state_data = {
        "step": 0, "done": False, "task": task, 
        "current_email": email, "correct": 0
    }
    return {"observation": email, "state": state_data}

@app.get("/state")
def get_state():
    return state_data

@app.post("/step")
def step(input: ActionInput):
    global state_data

    if state_data["done"]:
        return {"observation": None, "reward": 0.001, "done": True, "info": {}}

    correct_label = state_data["current_email"]["label"]
    action = input.action.lower()

    if action == correct_label:
        reward = 0.015
        state_data["correct"] += 1
    else:
        reward = 0.005

    state_data["step"] += 1

    if state_data["step"] >= 50:
        state_data["done"] = True

    # Next email
    task = state_data["task"]
    email = random.choice(EMAILS[task])
    state_data["current_email"] = email

    total = state_data["step"]
    correct = state_data["correct"]
    score = correct / total if total > 0 else 0.5
    
    # 🔥 FIXED: STRICT (0.01, 0.99) + noise
    score = max(0.01, min(0.99, score))
    score = score * (1 + random.uniform(-0.001, 0.001))
    score = max(0.01, min(0.99, score))

    return {
        "observation": email,
        "reward": round(reward, 3),
        "done": state_data["done"],
        "info": {"score": round(score, 3)}
    }

@app.get("/")
def root():
    return {"message": "Email OpenEnv running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)