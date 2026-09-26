import mark from "../assets/autogen-mark.svg";
import brainIcon from "../assets/brain.svg";
import globeIcon from "../assets/globe.svg";
import documentIcon from "../assets/document.svg";

const agents = [
  { key: "agent1", number: "01", title: "Direct Support", icon: brainIcon },
  { key: "agent2", number: "02", title: "Web Research", icon: globeIcon },
  { key: "agent3", number: "03", title: "Finalizer", icon: documentIcon },
];

function statusMeta(status) {
  switch (status) {
    case "working": return { text: "Working...", icon: "◌", mode: "active" };
    case "searching": return { text: "Searching...", icon: "◌", mode: "active" };
    case "finalizing": return { text: "Finalizing...", icon: "◌", mode: "active" };
    case "completed": return { text: "Completed", icon: "✓", mode: "completed" };
    case "failed": return { text: "Failed", icon: "!", mode: "failed" };
    default: return { text: "Waiting", icon: "Ⅱ", mode: "waiting" };
  }
}

export default function AgentSidebar({ statuses }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-3d-shell">
        <header className="side-brand">
          <img src={mark} alt="AutoGen" className="side-logo" />
          <div className="side-brand-copy">
            <strong>AutoGen</strong>
            <span>AI CUSTOMER SUPPORT</span>
            <small>Multi-Agent Intelligence System</small>
          </div>
        </header>

        <div className="side-online">
          <i />
          <span>AGENT NETWORK ONLINE</span>
        </div>

        <div className="agent-flow">
          {agents.map((agent, index) => {
            const state = statusMeta(statuses[agent.key]);
            return (
              <div className="agent-flow-item" key={agent.key}>
                <article className={`agent-card-3d ${state.mode}`}>
                  <div className="agent-icon-box">
                    <img src={agent.icon} alt="" />
                  </div>

                  <div className="agent-card-copy">
                    <div className="agent-line-one">
                      <span>AGENT {agent.number}</span>
                      <em>{agent.number}</em>
                    </div>
                    <h3>{agent.title}</h3>
                    <div className={`agent-status-pill ${state.mode}`}>
                      <b>{state.icon}</b>
                      <span>{state.text}</span>
                    </div>
                  </div>
                </article>

                {index < agents.length - 1 && (
                  <div className="energy-connector" aria-hidden="true">
                    <span className="energy-line" />
                    <span className="energy-dot top" />
                    <span className="energy-dot bottom" />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <footer className="side-footer">
          <span>Powered by</span>
          <div className="stack-row">
            <div className="ms-mini"><i/><i/><i/><i/></div>
            <strong>Microsoft<br/>AutoGen</strong>
            <b className="stack-sep">⚡ FastAPI</b>
            <b className="stack-sep">⚛ React</b>
          </div>
        </footer>
      </div>
    </aside>
  );
}
