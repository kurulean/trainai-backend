from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Workout AI backend is running"}

@app.post("/generate")
async def generate_workout(request: Request):
    data = await request.json()
    age = data.get("age")
    weight = data.get("weight")
    goal = data.get("goal")
    time = data.get("time")

    prompt = (
        f"Create a custom 5-day workout plan for a {age}-year-old "
        f"who weighs {weight} lbs, has {time} per day, "
        f"and wants to achieve the goal: {goal}. Include warm-ups and rest days."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experienced fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    plan = response["choices"][0]["message"]["content"].strip()
    return {"plan": plan}
