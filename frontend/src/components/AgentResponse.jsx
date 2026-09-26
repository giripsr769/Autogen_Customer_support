import { useState } from "react";


export default function AgentResponse({
  directAnswer,
  researchedAnswer,
}) {
  const [agent1Open, setAgent1Open] =
    useState(true);

  const [agent2Open, setAgent2Open] =
    useState(false);


  return (
    <div className="agent-response-wrap">

      {/* ==========================================
          SUCCESS HEADER
         ========================================== */}

      <div className="response-success">

        <div className="response-success-icon">
          ✓
        </div>

        <div>
          <strong>
            Your support request has been processed successfully.
          </strong>

          <p>
            Here are the responses from our AI support agents.
          </p>
        </div>

      </div>


      {/* ==========================================
          TWO COLUMN AGENT RESPONSE GRID
         ========================================== */}

      <div className="response-agent-grid">


        {/* ==========================================
            AGENT 1
           ========================================== */}

        <div
          className={`response-agent-card ${
            agent1Open ? "expanded" : ""
          }`}
        >

          <button
            type="button"
            className="response-agent-header"
            onClick={() =>
              setAgent1Open(
                (previous) => !previous
              )
            }
          >

            <div className="response-agent-left">

              <div className="response-agent-icon direct">
                🧠
              </div>


              <div className="response-agent-title">

                <span>
                  AGENT 01
                </span>

                <strong>
                  Direct Support Answer
                </strong>

              </div>

            </div>


            <div className="response-agent-right">

              <span className="response-status completed">
                ✓ Completed
              </span>


              <span
                className={`response-chevron ${
                  agent1Open ? "open" : ""
                }`}
              >
                ▼
              </span>

            </div>

          </button>


          <div
            className={`response-collapse ${
              agent1Open ? "open" : ""
            }`}
          >

            <div className="response-collapse-inner">

              <div className="response-answer-body">

                {directAnswer ? (
                  <p>
                    {directAnswer}
                  </p>
                ) : (
                  <p className="response-empty">
                    No direct support response available.
                  </p>
                )}

              </div>

            </div>

          </div>

        </div>


        {/* ==========================================
            AGENT 2
           ========================================== */}

        <div
          className={`response-agent-card ${
            agent2Open ? "expanded" : ""
          }`}
        >

          <button
            type="button"
            className="response-agent-header"
            onClick={() =>
              setAgent2Open(
                (previous) => !previous
              )
            }
          >

            <div className="response-agent-left">

              <div className="response-agent-icon research">
                🌐
              </div>


              <div className="response-agent-title">

                <span>
                  AGENT 02
                </span>

                <strong>
                  Web Research Answer
                </strong>

              </div>

            </div>


            <div className="response-agent-right">

              <span className="response-status completed">
                ✓ Completed
              </span>


              <span
                className={`response-chevron ${
                  agent2Open ? "open" : ""
                }`}
              >
                ▼
              </span>

            </div>

          </button>


          <div
            className={`response-collapse ${
              agent2Open ? "open" : ""
            }`}
          >

            <div className="response-collapse-inner">

              <div className="response-answer-body">

                {researchedAnswer ? (
                  <p>
                    {researchedAnswer}
                  </p>
                ) : (
                  <p className="response-empty">
                    No web research response available.
                  </p>
                )}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}