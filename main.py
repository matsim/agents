from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from crewai import Agent, Task, Crew

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou restreins à ["https://ton-site.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l’API CrewAI"}


@app.post("/landing/crew")
def generate_landing_page(brief: str = Body(..., embed=True)):

    # Agent 1 : Stratège LP
    strategist = Agent(
        name="Stratège Landing Page",
        role="Expert en stratégie de conversion pour landing pages",
        goal="Définir les messages clés, l'audience cible, et l'angle d'attaque à partir d’un brief",
        backstory="Un marketeur digital chevronné, obsédé par les parcours utilisateurs et les taux de conversion.",
        verbose=True
    )

    # Agent 2 : Copywriter LP
    copywriter = Agent(
        name="Copywriter Landing Page",
        role="Spécialiste du copywriting persuasif",
        goal="Rédiger le contenu complet d’une landing page à partir d’un brief stratégique",
        backstory="Un rédacteur créatif et rigoureux, chaque mot est conçu pour convertir.",
        verbose=True
    )

    # Agent 3 : Architecte LP
    architect = Agent(
        name="Architecte Landing Page",
        role="Expert en structure de page web orientée conversion",
        goal="Construire la structure idéale d’une landing page en utilisant la stratégie et le contenu rédigé",
        backstory="Un architecte UX pragmatique qui optimise le parcours utilisateur.",
        verbose=True
    )

    # Tâche 1 : Stratégie
    task1 = Task(
        description=f"""
        Analyse le brief utilisateur suivant : {brief}
        Objectif : Identifier l'objectif principal, l'audience cible, l'USP et 3 à 5 messages clés.
        Fournis un document de stratégie concis (max 300 mots).""",
        expected_output="Document texte contenant Objectif, Cible, USP, Messages clés, Ton suggéré",
        agent=strategist
    )

    # Tâche 2 : Copywriting
    task2 = Task(
        description="""
        En te basant sur le document de stratégie (Tâche 1), rédige :
        - 2 à 3 titres (H1)
        - 1 sous-titre
        - 5 à 7 bénéfices
        - 1 section Problème/Solution ou Comment ça marche ?
        - 3 à 4 éléments de réassurance
        - 2 à 3 appels à l’action (CTA)
        Le ton doit être adapté à la cible définie dans la stratégie.
        """,
        expected_output = "Contenu textuel complet de la landing page",
        agent=copywriter,
        context=[task1]
    )

    # Tâche 3 : Structure
    task3 = Task(
        description="""
        En t’appuyant sur la stratégie (Tâche 1) et le copywriting (Tâche 2), crée un plan de page :
        - Liste les sections dans un ordre logique (ex : Hero, Avantages, CTA…)
        - Pour chaque section, indique les textes à utiliser
        """,
        expected_output = "Plan détaillé de la structure de la landing page avec contenu associé",
        agent=architect,
        context=[task1, task2]
    )

    # Crew
    crew = Crew(
        agents=[strategist, copywriter, architect],
        tasks=[task1, task2, task3],
        verbose=True
    )

    result = crew.kickoff()
    return {"landing_page_result": result}