

import streamlit as st
import os
import json
import sys

sys.path.insert(0, os.path.dirname(__file__))

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.weather_tool import get_weather
from tools.budget_tool import estimate_budget


st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
.main-header{
background:linear-gradient(135deg,#1a73e8,#0d47a1);
color:white;
padding:2rem;
border-radius:12px;
text-align:center;
margin-bottom:1.5rem;
}
.itinerary-box{
background:#1e1e1e;
color:#ffffff;
border:1px solid #444;
padding:1.5rem;
border-radius:12px;
font-family:monospace;
white-space:pre-wrap;
line-height:1.8;
overflow-wrap: break-word;
}
.step-box{
background:#e8f4f8;
border-radius:8px;
padding:0.8rem;
margin:0.3rem 0;
font-size:0.85rem;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
<h1>✈️ AI Travel Planning Assistant</h1>
<p>Powered by LangChain Agents • Smart Itineraries</p>
</div>
""", unsafe_allow_html=True)



##########################
# SIDEBAR
##########################
with st.sidebar:

    st.header("⚙️ Configuration")

    st.success(
        "✅ Using GROQ API from .env"
    )


    st.divider()

    st.header("🔧 Tool Testing")


    tool_tab = st.selectbox(

        "Tool",

        [

            "Flights",

            "Hotels",

            "Places",

            "Weather",

            "Budget"

        ]

    )

    tool_query = st.text_input(

        "Query"

    )


    if st.button(

        "Run Tool"

    ):

        if tool_query:

            try:

                if tool_tab=="Flights":

                    result = search_flights.invoke(
                        tool_query
                    )

                elif tool_tab=="Hotels":

                    result = search_hotels.invoke(
                        tool_query
                    )

                elif tool_tab=="Places":

                    result = search_places.invoke(
                        tool_query
                    )

                elif tool_tab=="Weather":

                    result = get_weather.invoke(
                        tool_query
                    )

                elif tool_tab=="Budget":

                    result = estimate_budget.invoke(
                        tool_query
                    )


                st.code(
                    result
                )

            except Exception as e:

                st.error(

                    str(e)

                )



##########################
# MAIN
##########################

col1,col2 = st.columns(

    [2,1]

)


with col1:

    st.subheader(

        "🗺️ Plan Your Trip"

    )



    user_query = st.text_area(

        "Describe your trip",

        placeholder=
        "I want to visit Goa and stay near beaches"

    )



    #############################
    # NEW DATE INPUTS
    #############################

    date_col1,date_col2 = st.columns(

        2

    )


    with date_col1:

        start_date = st.date_input(

            "Start Date"

        )


    with date_col2:

        end_date = st.date_input(

            "End Date"

        )



    plan_btn = st.button(

        "🤖 Plan My Trip",

        type="primary",

        use_container_width=True

    )



with col2:

    st.subheader(

        "📊 Quick Lookup"

    )


    dest_city = st.selectbox(

        "Destination",

        [

            "Goa",

            "Jaipur",

            "Manali",

            "Kerala",

            "Mumbai",

            "Agra",

            "Delhi"

        ]

    )


    if st.button(

        "Hotels"

    ):

        st.code(

            search_hotels.invoke(

                dest_city

            )

        )


    if st.button(

        "Places"

    ):

        st.code(

            search_places.invoke(

                dest_city

            )

        )


    if st.button(

        "Weather"

    ):

        st.code(

            get_weather.invoke(

                dest_city

            )

        )



##############################
# AGENT
##############################

if plan_btn:

    if not user_query.strip():

        st.warning(
            "Enter trip details"
        )

        st.stop()


    full_query = (

        f"{user_query} "

        f"(Travel dates: "

        f"{start_date}"

        f" to "

        f"{end_date})"

    )


    st.subheader(
        "🤖 Agent"
    )


    try:

        from agent import run_travel_agent


        result = run_travel_agent(
            query=full_query
        )


        if result["success"]:

            st.subheader(
                "🗒️ Itinerary"
            )


            output_text = str(
                result["output"]
            )


            st.markdown(

                f"""
<div class="itinerary-box">

{output_text}

</div>
""",

                unsafe_allow_html=True

            )


            st.download_button(

                label="📥 Download Itinerary",

                data=output_text,

                file_name="travel_itinerary.txt",

                mime="text/plain"

            )


        else:

            st.error(

                result["output"]

            )


    except Exception as e:

        st.error(

            str(e)

        )


##############################
# FOOTER
##############################

st.divider()

st.caption(

"Built using LangChain + Streamlit"

)