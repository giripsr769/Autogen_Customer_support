import {
  useEffect,
  useRef,
  useState,
} from "react";

import AgentSidebar from "./components/AgentSidebar";
import ChatMessage from "./components/ChatMessage";
import AgentResponse from "./components/AgentResponse";

import {
  streamSupportQuery,
} from "./services/supportApi";


import "./styles.css";



function App() {

  const [query, setQuery] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [isLoading, setIsLoading] =
    useState(false);

  const [statuses, setStatuses] =
    useState({
      agent1: "waiting",
      agent2: "waiting",
      agent3: "waiting",
    });


  const endRef = useRef(null);


  // =======================================================
  // AUTO SCROLL
  // =======================================================

  useEffect(() => {

    endRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });

  }, [
    messages,
    isLoading,
  ]);


  // =======================================================
  // SUBMIT
  // =======================================================

  const handleSubmit = async (
    event
  ) => {

    event.preventDefault();

    const trimmedQuery =
      query.trim();


    if (
      !trimmedQuery ||
      isLoading
    ) {
      return;
    }


    // -----------------------------------------------------
    // DISPLAY USER MESSAGE
    // -----------------------------------------------------

    setMessages(
      (previous) => [
        ...previous,
        {
          id:
            crypto.randomUUID(),

          role:
            "user",

          content:
            trimmedQuery,
        },
      ]
    );


    setQuery("");

    setIsLoading(true);


    setStatuses({
      agent1: "waiting",
      agent2: "waiting",
      agent3: "waiting",
    });


    let directAnswer = "";
    let researchedAnswer = "";
    let finalAnswer = "";

    let guardrailBlocked = false;


    try {

      await streamSupportQuery(
        trimmedQuery,

        ({
          event,
          data,
        }) => {


          // =================================================
          // INPUT GUARDRAIL BLOCKED
          // =================================================

          if (
            event ===
            "guardrail_blocked"
          ) {

            guardrailBlocked = true;


            setStatuses({
              agent1: "waiting",
              agent2: "waiting",
              agent3: "waiting",
            });


            setMessages(
              (previous) => [
                ...previous,

                {
                  id:
                    crypto.randomUUID(),

                  role:
                    "guardrail",

                  guardrailType:
                    "input",

                  content:
                    data.message ||
                    "This request was blocked by the input safety guardrail.",
                },
              ]
            );


            setIsLoading(false);

            return;
          }


          // =================================================
          // AGENT 1 STARTED
          // =================================================

          if (
            event ===
            "agent1_started"
          ) {

            setStatuses({
              agent1: "working",
              agent2: "waiting",
              agent3: "waiting",
            });

            return;
          }


          // =================================================
          // AGENT 1 COMPLETED
          // =================================================
          // Status only.
          // Answer is intentionally NOT read here because
          // backend releases answers only after output guardrail.
          // =================================================

          if (
            event ===
            "agent1_completed"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "waiting",
              agent3: "waiting",
            });

            return;
          }


          // =================================================
          // AGENT 2 STARTED
          // =================================================

          if (
            event ===
            "agent2_started"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "searching",
              agent3: "waiting",
            });

            return;
          }


          // =================================================
          // AGENT 2 COMPLETED
          // =================================================
          // Status only.
          // =================================================

          if (
            event ===
            "agent2_completed"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "waiting",
            });

            return;
          }


          // =================================================
          // AGENT 3 STARTED
          // =================================================

          if (
            event ===
            "agent3_started"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "finalizing",
            });

            return;
          }


          // =================================================
          // OUTPUT GUARDRAIL STARTED
          // =================================================
          // Keep the current visual loading state.
          // No layout/UI component changes are needed.
          // =================================================

          if (
            event ===
            "output_guardrail_started"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "finalizing",
            });

            return;
          }


          // =================================================
          // OUTPUT GUARDRAIL BLOCKED
          // =================================================

          if (
            event ===
            "output_guardrail_blocked"
          ) {

            guardrailBlocked = true;


            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "completed",
            });


            setMessages(
              (previous) => [
                ...previous,

                {
                  id:
                    crypto.randomUUID(),

                  role:
                    "guardrail",

                  guardrailType:
                    "output",

                  content:
                    data.message ||
                    "The generated response was blocked by the output safety guardrail.",
                },
              ]
            );


            setIsLoading(false);

            return;
          }


          // =================================================
          // OUTPUT GUARDRAIL PASSED
          // =================================================

          if (
            event ===
            "output_guardrail_passed"
          ) {

            // Keep Agent 3 in finalizing state until the backend
            // confirms the complete workflow.
            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "finalizing",
            });

            return;
          }


          // =================================================
          // AGENT 3 COMPLETED
          // =================================================
          // Status only. Final answer is released in
          // the final "completed" event.
          // =================================================

          if (
            event ===
            "agent3_completed"
          ) {

            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "completed",
            });

            return;
          }


          // =================================================
          // WORKFLOW COMPLETED
          // =================================================

          if (
            event ===
            "completed"
          ) {

            if (
              data.blocked === true ||
              data.status === "blocked"
            ) {

              guardrailBlocked = true;

              setIsLoading(false);

              return;
            }


            // IMPORTANT:
            // Answers are collected ONLY here, after
            // the backend output guardrail has passed.

            directAnswer =
              data.direct_answer ||
              "";


            researchedAnswer =
              data.researched_answer ||
              "";


            finalAnswer =
              data.final_answer ||
              "";


            setStatuses({
              agent1: "completed",
              agent2: "completed",
              agent3: "completed",
            });

            return;
          }


          // =================================================
          // BACKEND ERROR EVENT
          // =================================================

          if (
            event ===
            "error"
          ) {

            throw new Error(
              data.message ||
              "Support workflow failed."
            );
          }

        }
      );


      // =====================================================
      // DO NOT CREATE ASSISTANT RESPONSE
      // WHEN INPUT/OUTPUT GUARDRAIL BLOCKED
      // =====================================================

      if (guardrailBlocked) {
        return;
      }


      // =====================================================
      // ADD SAFE COMPLETED RESPONSE
      // =====================================================

      setMessages(
        (previous) => [
          ...previous,

          {
            id:
              crypto.randomUUID(),

            role:
              "assistant",

            directAnswer,

            researchedAnswer,

            finalAnswer,
          },
        ]
      );

    }

    catch (error) {

      console.error(
        "Support error:",
        error
      );


      setStatuses({
        agent1: "failed",
        agent2: "failed",
        agent3: "failed",
      });


      setMessages(
        (previous) => [
          ...previous,

          {
            id:
              crypto.randomUUID(),

            role:
              "error",

            content:
              error.message ||
              "Unable to complete the request. Please check the backend and try again.",
          },
        ]
      );

    }

    finally {

      setIsLoading(false);

    }

  };

  // =======================================================
  // UI
  // =======================================================

  return (

    <div className="app-shell">


      {/* ===================================================
          BACKGROUND
         =================================================== */}

      <div
        className="space-background"
        aria-hidden="true"
      >
        <div className="space-glow space-glow-one" />
        <div className="space-glow space-glow-two" />
        <div className="space-grid" />
      </div>


      {/* ===================================================
          LEFT SIDEBAR
         =================================================== */}

      <aside className="sidebar-column">

        <AgentSidebar
          statuses={statuses}
        />

      </aside>


      {/* ===================================================
          RIGHT PANEL
         =================================================== */}

      <section className="main-panel">


        {/* =================================================
            HEADER
           ================================================= */}

        <header className="main-header">


          <div className="header-copy">

            <div className="online-label">

              <span
                className="online-dot"
              />

              AUTOGEN AGENT NETWORK ONLINE

            </div>


            <h1>
              AI CUSTOMER SUPPORT
            </h1>


            <h2>
              Multi-Agent Intelligence System
            </h2>


            <p>
              Three specialized AI agents collaborate
              in real time to provide intelligent
              customer support.
            </p>

          </div>


          <div className="powered-card">

            <div className="microsoft-grid">
              <span />
              <span />
              <span />
              <span />
            </div>


            <div>

              <small>
                Powered by
              </small>

              <strong>
                Microsoft AutoGen
              </strong>

            </div>

          </div>

        </header>


        {/* =================================================
            CONVERSATION
           ================================================= */}

        <div className="conversation-scroll">

          <div className="conversation-inner">


            {/* ===============================================
                EMPTY STATE
               =============================================== */}

            {
              messages.length === 0 && (

                <div className="welcome-panel">

                  <div className="welcome-orb">
                    ✦
                  </div>


                  <div className="welcome-copy">

                    <div className="welcome-label">
                      MULTI-AGENT SUPPORT READY
                    </div>


                    <h3>
                      How can our AI agents help?
                    </h3>


                    <p>
                      Ask your customer support question
                      and watch three specialized AI agents
                      work together.
                    </p>


                    <div className="workflow-preview">


                      <div className="workflow-item">

                        <span>
                          01
                        </span>

                        <div>

                          <strong>
                            Direct Support
                          </strong>

                          <small>
                            Initial intelligent response
                          </small>

                        </div>

                      </div>


                      <div className="workflow-arrow">
                        →
                      </div>


                      <div className="workflow-item">

                        <span>
                          02
                        </span>

                        <div>

                          <strong>
                            Web Research
                          </strong>

                          <small>
                            Live external research
                          </small>

                        </div>

                      </div>


                      <div className="workflow-arrow">
                        →
                      </div>


                      <div className="workflow-item">

                        <span>
                          03
                        </span>

                        <div>

                          <strong>
                            Finalizer
                          </strong>

                          <small>
                            Final response and logging
                          </small>

                        </div>

                      </div>


                    </div>

                  </div>

                </div>

              )
            }


            {/* ===============================================
                MESSAGES
               =============================================== */}

            {
              messages.map(
                (message) => {


                  // USER
                  if (
                    message.role ===
                    "user"
                  ) {

                    return (

                      <ChatMessage
                        key={message.id}
                        message={
                          message.content
                        }
                      />

                    );

                  }


                  // ASSISTANT
                  if (
                    message.role ===
                    "assistant"
                  ) {

                    return (

                      <AgentResponse
                        key={message.id}

                        directAnswer={
                          message.directAnswer
                        }

                        researchedAnswer={
                          message.researchedAnswer
                        }
                      />

                    );

                  }


                  // GUARDRAIL
                  if (
                    message.role ===
                    "guardrail"
                  ) {

                    return (

                      <div
                        key={message.id}
                        className="guardrail-message"
                      >

                        <div className="guardrail-icon">
                          🛡️
                        </div>


                        <div className="guardrail-copy">

                          <div className="guardrail-heading">
                            Safety Guardrail
                          </div>


                          <div className="guardrail-subtitle">
                            {
                              message.guardrailType === "output"
                                ? "Generated response blocked before being shown to the user"
                                : "Request blocked before reaching the AI agents"
                            }
                          </div>


                          <p>
                            {message.content}
                          </p>

                        </div>

                      </div>

                    );

                  }


                  // ERROR
                  if (
                    message.role ===
                    "error"
                  ) {

                    return (

                      <div
                        key={message.id}
                        className="error-message"
                      >

                        <span>
                          ⚠
                        </span>


                        <div>

                          <strong>
                            Request failed
                          </strong>

                          <p>
                            {message.content}
                          </p>

                        </div>

                      </div>

                    );

                  }


                  return null;

                }
              )
            }


            {/* ===============================================
                THINKING
               =============================================== */}

            {
              isLoading && (

                <div className="agent-thinking">

                  <div className="thinking-orb">
                    <span />
                    <span />
                    <span />
                  </div>


                  <div>

                    <strong>
                      AI agents are collaborating
                    </strong>


                    <p>
                      Processing your request through
                      the multi-agent workflow...
                    </p>

                  </div>

                </div>

              )
            }


            <div ref={endRef} />


          </div>

        </div>


        {/* =================================================
            INPUT
           ================================================= */}

        <div className="input-zone">


          <form
            className="command-dock"
            onSubmit={handleSubmit}
          >


            <button
              type="button"
              className="attach-button"
              title="Attachment"
            >
              +
            </button>


            <input
              value={query}

              onChange={
                (event) =>
                  setQuery(
                    event.target.value
                  )
              }

              placeholder="
                Ask your customer support question...
              "

              disabled={isLoading}

              maxLength={4000}
            />


            <button
              type="submit"
              className="send-button"

              disabled={
                isLoading ||
                !query.trim()
              }
            >

              <span>
                {
                  isLoading
                    ? "Working..."
                    : "Send"
                }
              </span>

              <b>
                ➤
              </b>

            </button>


          </form>


          <div className="input-footer">

            <span>
              🛡 Guardrail Protected
            </span>

            <span>
              •
            </span>

            <span>
              Multi-Agent AI
            </span>

            <span>
              •
            </span>

            <span>
              Live Web Research
            </span>

          </div>


        </div>


      </section>

    </div>

  );

}


export default App;