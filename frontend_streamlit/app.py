import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

STREAM_API_URL = f"{BACKEND_URL}/support/stream"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AutoGen Customer Support",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   MAIN PAGE
   ===================================================== */

.block-container {
    max-width: 1400px;
    padding-top: 3.2rem !important;
    padding-bottom: 6rem;
}


/* =====================================================
   HEADER
   ===================================================== */

.main-title {
    font-size: 2.1rem;
    font-weight: 750;
    line-height: 1.35;
    padding-top: 6px;
    padding-bottom: 3px;
    margin: 0;
    overflow: visible;
}

.main-subtitle {
    font-size: 14px;
    opacity: 0.65;
    margin-top: 2px;
    margin-bottom: 28px;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    min-width: 300px;
    max-width: 330px;
}


/* Normal Agent Card */
.agent-card {
    position: relative;
    padding: 16px;
    border: 1px solid rgba(120, 120, 120, 0.30);
    border-radius: 12px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.03);
    overflow: hidden;
}


/* =====================================================
   ACTIVE AGENT BORDER ANIMATION
   ===================================================== */

.agent-card.active {
    border: 3px solid transparent;

    background:
        linear-gradient(
            var(--secondary-background-color),
            var(--secondary-background-color)
        ) padding-box,

        linear-gradient(
            90deg,
            #00e5ff,
            #00ff88,
            #7c4dff,
            #ff2bd6,
            #00e5ff
        ) border-box;

    background-size:
        100% 100%,
        350% 350%;

    animation:
        agentBorderMove 1.4s linear infinite,
        agentPulse 1.1s ease-in-out infinite;

    box-shadow:
        0 0 14px rgba(0, 229, 255, 0.75),
        0 0 26px rgba(124, 77, 255, 0.45);
}


@keyframes agentBorderMove {

    0% {
        background-position:
            0 0,
            0% 50%;
    }

    50% {
        background-position:
            0 0,
            100% 50%;
    }

    100% {
        background-position:
            0 0,
            0% 50%;
    }
}


@keyframes agentPulse {

    0% {
        box-shadow:
            0 0 10px rgba(0, 229, 255, 0.45),
            0 0 18px rgba(124, 77, 255, 0.25);
    }

    50% {
        box-shadow:
            0 0 22px rgba(0, 229, 255, 0.95),
            0 0 38px rgba(255, 43, 214, 0.70);
    }

    100% {
        box-shadow:
            0 0 10px rgba(0, 229, 255, 0.45),
            0 0 18px rgba(124, 77, 255, 0.25);
    }
}


/* Completed */
.agent-card.completed {
    border: 2px solid rgba(65, 190, 110, 0.45);
}


/* Failed */
.agent-card.failed {
    border: 1px solid rgba(220, 70, 70, 0.55);
}


.agent-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}


.agent-status {
    font-size: 13px;
    opacity: 0.8;
}


/* =====================================================
   CHAT
   ===================================================== */

.chat-label {
    font-size: 12px;
    opacity: 0.65;
    margin-bottom: 5px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}


/* Expander */
div[data-testid="stExpander"] {
    border-radius: 10px;
}


/* Slight spacing between messages */
.chat-message-space {
    margin-bottom: 14px;
}


/* Hide footer */
footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "agent_statuses" not in st.session_state:

    st.session_state.agent_statuses = {
        "agent1": "waiting",
        "agent2": "waiting",
        "agent3": "waiting"
    }


# =========================================================
# STATUS HELPERS
# =========================================================

def status_text(status: str) -> str:

    status_map = {
        "waiting": "⏸ Waiting",
        "working": "🔄 Working...",
        "searching": "🔎 Searching the web...",
        "finalizing": "📝 Finalizing response...",
        "completed": "✅ Completed",
        "failed": "❌ Failed"
    }

    return status_map.get(
        status,
        status
    )


def card_class(status: str) -> str:

    if status in [
        "working",
        "searching",
        "finalizing"
    ]:
        return "agent-card active"

    if status == "completed":
        return "agent-card completed"

    if status == "failed":
        return "agent-card failed"

    return "agent-card"


# =========================================================
# SIDEBAR
# CREATE ONLY ONCE
# =========================================================

with st.sidebar:

    st.markdown("### 🤖 Agent Workflow")

    agent1_placeholder = st.empty()
    agent2_placeholder = st.empty()
    agent3_placeholder = st.empty()

    st.divider()

    st.caption(
        "Powered by Microsoft AutoGen + FastAPI + Streamlit"
    )


# =========================================================
# UPDATE SIDEBAR
# =========================================================

def update_sidebar():

    agent1_status = (
        st.session_state.agent_statuses["agent1"]
    )

    agent2_status = (
        st.session_state.agent_statuses["agent2"]
    )

    agent3_status = (
        st.session_state.agent_statuses["agent3"]
    )


    # -----------------------------------------------------
    # AGENT 1
    # -----------------------------------------------------

    agent1_placeholder.markdown(
        f"""
<div class="{card_class(agent1_status)}">
<div class="agent-title">
🧠 Agent 1 — Direct Support
</div>
<div class="agent-status">
{status_text(agent1_status)}
</div>
</div>
""",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # AGENT 2
    # -----------------------------------------------------

    agent2_placeholder.markdown(
        f"""
<div class="{card_class(agent2_status)}">
<div class="agent-title">
🌐 Agent 2 — Web Research
</div>
<div class="agent-status">
{status_text(agent2_status)}
</div>
</div>
""",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # AGENT 3
    # -----------------------------------------------------

    agent3_placeholder.markdown(
        f"""
<div class="{card_class(agent3_status)}">
<div class="agent-title">
📝 Agent 3 — Finalizer
</div>
<div class="agent-status">
{status_text(agent3_status)}
</div>
</div>
""",
        unsafe_allow_html=True
    )


# Initial sidebar
update_sidebar()


# =========================================================
# USER MESSAGE
# LEFT ALIGNED — 80%
# =========================================================

def show_user_message(message: str):

    left, right = st.columns(
        [4, 1],
        gap="medium"
    )

    with left:

        st.markdown(
            '<div class="chat-label">👤 You</div>',
            unsafe_allow_html=True
        )

        with st.container(
            border=True
        ):
            st.markdown(message)


# =========================================================
# AGENT RESPONSE
# RIGHT ALIGNED — 80%
# =========================================================

def show_agent_message(
    direct_answer: str,
    researched_answer: str
):

    left, right = st.columns(
        [1, 4],
        gap="medium"
    )

    with right:

        with st.container(
            border=True
        ):

            st.markdown(
                "✅ **Your support request has been processed successfully.**"
            )

            st.caption(
                "Review the responses from the support agents below."
            )


            # -------------------------------------------------
            # AGENT 1
            # OPEN BY DEFAULT
            # -------------------------------------------------

            if direct_answer:

                with st.expander(
                    "🧠 Agent 1 — Direct Support Answer",
                    expanded=True
                ):

                    st.markdown(
                        direct_answer
                    )


            # -------------------------------------------------
            # AGENT 2
            # COLLAPSED BY DEFAULT
            # -------------------------------------------------

            if researched_answer:

                with st.expander(
                    "🌐 Agent 2 — Web Research Answer",
                    expanded=False
                ):

                    st.markdown(
                        researched_answer
                    )


# =========================================================
# SSE STREAM PROCESSOR
# =========================================================

def process_sse_stream(
    user_query: str
):

    response = requests.post(
        STREAM_API_URL,

        json={
            "query": user_query
        },

        stream=True,

        timeout=300
    )

    response.raise_for_status()


    current_event = None

    direct_answer = ""
    researched_answer = ""
    final_answer = ""


    # =====================================================
    # READ STREAM
    # =====================================================

    for raw_line in response.iter_lines(
        decode_unicode=True
    ):

        if not raw_line:
            continue


        line = raw_line.strip()


        # -------------------------------------------------
        # EVENT NAME
        # -------------------------------------------------

        if line.startswith("event:"):

            current_event = (
                line
                .replace(
                    "event:",
                    "",
                    1
                )
                .strip()
            )

            continue


        # -------------------------------------------------
        # EVENT DATA
        # -------------------------------------------------

        if line.startswith("data:"):

            raw_data = (
                line
                .replace(
                    "data:",
                    "",
                    1
                )
                .strip()
            )


            try:

                data = json.loads(
                    raw_data
                )

            except json.JSONDecodeError:

                continue


            # =================================================
            # AGENT 1 STARTED
            # =================================================

            if current_event == "agent1_started":

                st.session_state.agent_statuses[
                    "agent1"
                ] = "working"

                update_sidebar()


            # =================================================
            # AGENT 1 COMPLETED
            # =================================================

            elif current_event == "agent1_completed":

                direct_answer = data.get(
                    "direct_answer",
                    ""
                )

                st.session_state.agent_statuses[
                    "agent1"
                ] = "completed"

                update_sidebar()


            # =================================================
            # AGENT 2 STARTED
            # =================================================

            elif current_event == "agent2_started":

                st.session_state.agent_statuses[
                    "agent2"
                ] = "searching"

                update_sidebar()


            # =================================================
            # AGENT 2 COMPLETED
            # =================================================

            elif current_event == "agent2_completed":

                researched_answer = data.get(
                    "researched_answer",
                    ""
                )

                st.session_state.agent_statuses[
                    "agent2"
                ] = "completed"

                update_sidebar()


            # =================================================
            # AGENT 3 STARTED
            # =================================================

            elif current_event == "agent3_started":

                st.session_state.agent_statuses[
                    "agent3"
                ] = "finalizing"

                update_sidebar()


            # =================================================
            # AGENT 3 COMPLETED
            # =================================================

            elif current_event == "agent3_completed":

                final_answer = data.get(
                    "final_answer",
                    ""
                )

                st.session_state.agent_statuses[
                    "agent3"
                ] = "completed"

                update_sidebar()


            # =================================================
            # WORKFLOW COMPLETE
            # =================================================

            elif current_event == "completed":

                direct_answer = data.get(
                    "direct_answer",
                    direct_answer
                )

                researched_answer = data.get(
                    "researched_answer",
                    researched_answer
                )

                final_answer = data.get(
                    "final_answer",
                    final_answer
                )

                break


    return {

        "direct_answer":
            direct_answer,

        "researched_answer":
            researched_answer,

        "final_answer":
            final_answer
    }


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    """
<div class="main-title">
🤖 AutoGen Customer Support
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="main-subtitle">
Multi-Agent Customer Support powered by Microsoft AutoGen
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:


    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    if message["role"] == "user":

        show_user_message(
            message["content"]
        )


    # -----------------------------------------------------
    # ASSISTANT
    # -----------------------------------------------------

    elif message["role"] == "assistant":

        show_agent_message(

            message.get(
                "direct_answer",
                ""
            ),

            message.get(
                "researched_answer",
                ""
            )
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_query = st.chat_input(
    "Ask your customer support question..."
)


# =========================================================
# PROCESS QUERY
# =========================================================

if user_query:


    # =====================================================
    # RESET STATUS
    # =====================================================

    st.session_state.agent_statuses = {
        "agent1": "waiting",
        "agent2": "waiting",
        "agent3": "waiting"
    }

    update_sidebar()


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    show_user_message(
        user_query
    )


    # =====================================================
    # AGENT RESPONSE AREA
    # RIGHT SIDE — 80%
    # =====================================================

    left, right = st.columns(
        [1, 4],
        gap="medium"
    )


    with right:

        response_placeholder = st.empty()


        try:

            # =================================================
            # LOADING STATE
            # =================================================

            with response_placeholder.container():

                with st.container(
                    border=True
                ):

                    with st.spinner(
                        "Your support agents are working "
                        "to prepare the best response..."
                    ):

                        result = process_sse_stream(
                            user_query
                        )


            # =================================================
            # GET RESULTS
            # =================================================

            direct_answer = result.get(
                "direct_answer",
                ""
            )

            researched_answer = result.get(
                "researched_answer",
                ""
            )

            final_answer = result.get(
                "final_answer",
                ""
            )


            # =================================================
            # REMOVE LOADING AREA
            # =================================================

            response_placeholder.empty()


            # =================================================
            # DISPLAY RESULT
            # =================================================

            with response_placeholder.container():

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "✅ **Your support request has been processed successfully.**"
                    )

                    st.caption(
                        "Review the responses from the support agents below."
                    )


                    # -----------------------------------------
                    # Agent 1
                    # DEFAULT OPEN
                    # -----------------------------------------

                    if direct_answer:

                        with st.expander(
                            "🧠 Agent 1 — Direct Support Answer",
                            expanded=True
                        ):

                            st.markdown(
                                direct_answer
                            )


                    # -----------------------------------------
                    # Agent 2
                    # DEFAULT CLOSED
                    # -----------------------------------------

                    if researched_answer:

                        with st.expander(
                            "🌐 Agent 2 — Web Research Answer",
                            expanded=False
                        ):

                            st.markdown(
                                researched_answer
                            )


            # =================================================
            # SAVE ASSISTANT RESPONSE
            # =================================================

            st.session_state.messages.append(
                {

                    "role":
                        "assistant",

                    "direct_answer":
                        direct_answer,

                    "researched_answer":
                        researched_answer,

                    "final_answer":
                        final_answer
                }
            )


        # =====================================================
        # CONNECTION ERROR
        # =====================================================

        except requests.exceptions.ConnectionError:

            st.session_state.agent_statuses = {
                "agent1": "failed",
                "agent2": "failed",
                "agent3": "failed"
            }

            update_sidebar()

            response_placeholder.empty()

            st.error(
                "❌ Unable to connect to the FastAPI backend. "
                "Please make sure the backend is running."
            )


        # =====================================================
        # TIMEOUT
        # =====================================================

        except requests.exceptions.Timeout:

            response_placeholder.empty()

            st.error(
                "⏳ The support agents took too long to respond. "
                "Please try again."
            )


        # =====================================================
        # HTTP ERROR
        # =====================================================

        except requests.exceptions.HTTPError as error:

            response_placeholder.empty()

            st.error(
                f"❌ Backend error: {error}"
            )


        # =====================================================
        # OTHER ERROR
        # =====================================================

        except Exception as error:

            response_placeholder.empty()

            st.error(
                f"❌ Something went wrong: {error}"
            )