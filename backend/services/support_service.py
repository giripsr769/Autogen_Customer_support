import json

from backend.agents.support_agent import create_support_agent
from backend.agents.research_agent import create_research_agent
from backend.agents.logger_agent import create_logger_agent

from backend.guardrails.input_guardrail import validate_user_query
from backend.guardrails.output_guardrail import validate_output


# =========================================================
# NORMAL NON-STREAMING WORKFLOW
# =========================================================

async def run_support_workflow(user_query: str):

    # -----------------------------------------------------
    # INPUT GUARDRAIL
    # -----------------------------------------------------

    is_valid, guardrail_message = await validate_user_query(
        user_query
    )

    if not is_valid:
        return {
            "user_query": user_query,
            "blocked": True,
            "guardrail_type": "input",
            "guardrail_message": guardrail_message,
            "direct_answer": "",
            "researched_answer": "",
            "final_answer": "",
        }


    # -----------------------------------------------------
    # CREATE AGENTS
    # -----------------------------------------------------

    support_agent = create_support_agent()
    research_agent = create_research_agent()
    logger_agent = create_logger_agent()


    # -----------------------------------------------------
    # AGENT 1 - DIRECT SUPPORT
    # -----------------------------------------------------

    support_result = await support_agent.run(
        task=user_query
    )

    direct_answer = (
        support_result.messages[-1].content
        if support_result.messages
        else ""
    )


    # -----------------------------------------------------
    # AGENT 2 - WEB RESEARCH
    # -----------------------------------------------------

    research_result = await research_agent.run(
        task=user_query
    )

    researched_answer = (
        research_result.messages[-1].content
        if research_result.messages
        else ""
    )


    # -----------------------------------------------------
    # AGENT 3 - FINALIZER / LOGGER
    # -----------------------------------------------------

    logger_task = f"""
        User Query:
        {user_query}

        Agent 1 - Direct Support Answer:
        {direct_answer}

        Agent 2 - Web Research Answer:
        {researched_answer}

        Save this support conversation using the available logging tool.

        Then provide the final customer-support response.

        Do not invent new facts.
        Do not perform additional web searches.
        """

    logger_result = await logger_agent.run(
        task=logger_task
    )

    final_answer = (
        logger_result.messages[-1].content
        if logger_result.messages
        else ""
    )


    # -----------------------------------------------------
    # OUTPUT GUARDRAIL
    # -----------------------------------------------------

    output_to_validate = f"""
        Direct Support Answer:
        {direct_answer}

        Web Research Answer:
        {researched_answer}

        Final Answer:
        {final_answer}
        """

    output_allowed, output_guardrail_message = await validate_output(
        output_to_validate
    )

    if not output_allowed:
        return {
            "user_query": user_query,
            "blocked": True,
            "guardrail_type": "output",
            "guardrail_message": output_guardrail_message,
            "direct_answer": "",
            "researched_answer": "",
            "final_answer": "",
        }


    # -----------------------------------------------------
    # FINAL SAFE RESPONSE
    # -----------------------------------------------------

    return {
        "user_query": user_query,
        "blocked": False,
        "direct_answer": direct_answer,
        "researched_answer": researched_answer,
        "final_answer": final_answer,
    }


# =========================================================
# STREAMING WORKFLOW
# =========================================================

async def run_support_workflow_stream(
    user_query: str
):

    # =====================================================
    # STEP 0 - INPUT GUARDRAIL
    # =====================================================

    print("🛡 Running input guardrail...")

    is_valid, guardrail_message = await validate_user_query(
        user_query
    )

    print(
        "🛡 Input guardrail result:",
        is_valid,
        guardrail_message
    )


    # -----------------------------------------------------
    # INPUT BLOCK
    # -----------------------------------------------------

    if not is_valid:

        yield {
            "event": "guardrail_blocked",
            "data": json.dumps({
                "message": guardrail_message,
                "blocked": True,
                "guardrail_type": "input",
            })
        }

        yield {
            "event": "completed",
            "data": json.dumps({
                "status": "blocked",
                "blocked": True,
                "guardrail_type": "input",
                "message": guardrail_message,
            })
        }

        print(
            "🛡 Request blocked by input guardrail."
        )

        return


    # =====================================================
    # CREATE AGENTS
    # =====================================================

    print("✅ Input guardrail passed.")
    print("🤖 Creating AutoGen agents...")

    support_agent = create_support_agent()
    research_agent = create_research_agent()
    logger_agent = create_logger_agent()


    # =====================================================
    # AGENT 1 - DIRECT SUPPORT
    # =====================================================

    yield {
        "event": "agent1_started",
        "data": json.dumps({
            "message":
                "Direct Support Agent is thinking..."
        })
    }


    try:

        support_result = await support_agent.run(
            task=user_query
        )

        direct_answer = (
            support_result.messages[-1].content
            if support_result.messages
            else ""
        )

    except Exception as error:

        print(
            "❌ Agent 1 error:",
            error
        )

        yield {
            "event": "error",
            "data": json.dumps({
                "message":
                    "Direct Support Agent failed."
            })
        }

        return


    # IMPORTANT:
    # Status only. Do not send actual answer yet.

    yield {
        "event": "agent1_completed",
        "data": json.dumps({
            "message":
                "Direct Support Agent completed."
        })
    }


    # =====================================================
    # AGENT 2 - WEB RESEARCH
    # =====================================================

    yield {
        "event": "agent2_started",
        "data": json.dumps({
            "message":
                "Web Research Agent is searching..."
        })
    }


    try:

        research_result = await research_agent.run(
            task=user_query
        )

        researched_answer = (
            research_result.messages[-1].content
            if research_result.messages
            else ""
        )

    except Exception as error:

        print(
            "❌ Agent 2 error:",
            error
        )

        yield {
            "event": "error",
            "data": json.dumps({
                "message":
                    "Web Research Agent failed."
            })
        }

        return


    # IMPORTANT:
    # Status only. Do not send actual answer yet.

    yield {
        "event": "agent2_completed",
        "data": json.dumps({
            "message":
                "Web Research Agent completed."
        })
    }


    # =====================================================
    # AGENT 3 - FINALIZER / LOGGER
    # =====================================================

    yield {
        "event": "agent3_started",
        "data": json.dumps({
            "message":
                "Finalizer Agent is preparing the final response..."
        })
    }


    logger_task = f"""
        User Query:
        {user_query}

        Agent 1 - Direct Support Answer:
        {direct_answer}

        Agent 2 - Web Research Answer:
        {researched_answer}

        Save this support conversation using the available logging tool.

        Then provide the final customer-support response.

        Do not invent new facts.
        Do not perform additional web searches.
        """


    try:

        logger_result = await logger_agent.run(
            task=logger_task
        )

        final_answer = (
            logger_result.messages[-1].content
            if logger_result.messages
            else ""
        )

    except Exception as error:

        print(
            "❌ Agent 3 error:",
            error
        )

        yield {
            "event": "error",
            "data": json.dumps({
                "message":
                    "Finalizer Agent failed."
            })
        }

        return


    # IMPORTANT:
    # Do not send final_answer yet.


    # =====================================================
    # OUTPUT GUARDRAIL STARTED
    # =====================================================

    yield {
        "event": "output_guardrail_started",
        "data": json.dumps({
            "message":
                "Checking AI responses for safety..."
        })
    }


    print(
        "🛡 Running output guardrail..."
    )


    # -----------------------------------------------------
    # VALIDATE EVERYTHING THAT WILL BE SHOWN TO USER
    # -----------------------------------------------------

    output_to_validate = f"""
    Direct Support Answer:
    {direct_answer}

    Web Research Answer:
    {researched_answer}

    Final Answer:
    {final_answer}
    """


    output_allowed, output_guardrail_message = await validate_output(
        output_to_validate
    )


    print(
        "🛡 Output guardrail result:",
        output_allowed,
        output_guardrail_message
    )


    # =====================================================
    # OUTPUT BLOCKED
    # =====================================================

    if not output_allowed:

        yield {
            "event": "output_guardrail_blocked",
            "data": json.dumps({
                "message":
                    output_guardrail_message,

                "blocked":
                    True,

                "guardrail_type":
                    "output",
            })
        }


        yield {
            "event": "completed",
            "data": json.dumps({
                "status":
                    "blocked",

                "blocked":
                    True,

                "guardrail_type":
                    "output",

                "message":
                    output_guardrail_message,
            })
        }


        print(
            "🛡 Response blocked by output guardrail."
        )

        return


    # =====================================================
    # OUTPUT PASSED
    # =====================================================

    yield {
        "event": "output_guardrail_passed",
        "data": json.dumps({
            "message":
                "Response passed output safety validation."
        })
    }


    # =====================================================
    # AGENT 3 COMPLETED
    # =====================================================

    yield {
        "event": "agent3_completed",
        "data": json.dumps({
            "message":
                "Finalizer Agent completed."
        })
    }


    # =====================================================
    # FULL WORKFLOW COMPLETED
    # =====================================================

    yield {
        "event": "completed",
        "data": json.dumps({
            "status":
                "completed",

            "blocked":
                False,

            "message":
                "Customer support workflow completed successfully.",

            "user_query":
                user_query,

            "direct_answer":
                direct_answer,

            "researched_answer":
                researched_answer,

            "final_answer":
                final_answer,
        })
    }


    print(
        "✅ Support workflow completed safely."
    )