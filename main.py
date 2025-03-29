  from fastapi import FastAPI
  from crewai import Agent, Task, Crew

  app = FastAPI()

  @app.get("/")
  async def root():
      return {"message": "Bienvenue sur l'API CrewAI"}

  @app.post("/execute_task/")
  async def execute_task():
      agent = Agent(name="Assistant", goal="Fournir des informations utiles")
      task = Task(description="Répondre à une question de l'utilisateur", agent=agent)
      crew = Crew(agents=[agent], tasks=[task])
      result = crew.kickoff()
      return {"result": result}
