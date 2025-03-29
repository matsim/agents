from fastapi import FastAPI
from crewai import Agent, Task, Crew

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur CrewAI"}

@app.post("/execute")
def run_crew():
    agent = Agent(name="Assistant", goal="Répondre à des questions")
    task = Task(description="Répondre à une demande utilisateur", agent=agent)
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return {"result": result}