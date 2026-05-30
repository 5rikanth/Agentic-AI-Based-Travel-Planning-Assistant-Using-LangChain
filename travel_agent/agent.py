import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType

from tools import (
    search_flights,
    search_hotels,
    search_places,
    get_weather,
    estimate_budget,
)

load_dotenv()


def create_travel_agent():

    llm = ChatGroq(

        model="llama-3.3-70b-versatile",

        groq_api_key=os.getenv(
            "GROQ_API_KEY"
        ),

        temperature=0.3

    )

    tools = [

        search_flights,

        search_hotels,

        search_places,

        get_weather,

        estimate_budget

    ]

    agent = initialize_agent(

        tools=tools,

        llm=llm,

        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

        verbose=True,

        handle_parsing_errors=True

    )

    return agent


def run_travel_agent(query):

    try:

        agent = create_travel_agent()

        result = agent.invoke(

            query

        )

        return {

            "output":

                result,

            "success":

                True

        }

    except Exception as e:

        return {

            "output":

                str(e),

            "success":

                False

        }


if __name__ == "__main__":

    query = input(

        "🌍 Enter travel request: "

    )

    result = run_travel_agent(

        query

    )

    print(

        "\n"

    )

    print(

        result["output"]

    )