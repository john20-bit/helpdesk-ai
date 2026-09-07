import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "https://charcoal-headdress-worst.ngrok-free.dev";

const navigation = [
  { id: "dashboard", label: "Dashboard", icon: "⌂" },
  { id: "assistant", label: "AI Assistant", icon: "◈" },
  { id: "tickets", label: "Tickets", icon: "▣" },
  { id: "diagnostics", label: "Diagnostics", icon: "⌁" },
  { id: "knowledge", label: "Knowledge Base", icon: "◫" },
];

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tickets, setTickets] = useState([]);
  const [ticketsLoading, setTicketsLoading] = useState(false);

  const loadTickets = async () => {
    setTicketsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/tickets`);
      const data = await response.json();

      if (data.success) {
        setTickets(data.tickets || []);
      }
    } catch (error) {
      console.error("Unable to load tickets:", error);
    } finally {
      setTicketsLoading(false);
    }
  };

  useEffect(() => {
    loadTickets();
  }, []);

  const diagnoseProblem = async () => {
    if (!message.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/ai/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Unable to process request.");
      }

      setResult(data.data);

      if (data.data?.escalation?.required) {
        loadTickets();
      }
    } catch (error) {
      setResult({
        error: error.message,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      diagnoseProblem();
    }
  };

  const pageTitle = {
    dashboard: "IT Support Dashboard",
    assistant: "AI Support Assistant",
    tickets: "Support Tickets",
    diagnostics: "System Diagnostics",
    knowledge: "Knowledge Base",
  }[activePage];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">✦</div>
          <div>
            <h1>HelpDesk AI</h1>
            <span>IT Support Agent</span>
          </div>
        </div>

        <nav className="navigation">
          {navigation.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${
                activePage === item.id ? "active" : ""
              }`}
              onClick={() => setActivePage(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-status">
          <span className="status-dot" />
          <div>
            <strong>System Online</strong>
            <small>Agent services operational</small>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="eyebrow">AI OPERATIONS</span>
            <h2>{pageTitle}</h2>
          </div>

          <div className="agent-status">
            <span className="status-dot" />
            Agent Ready
          </div>
        </header>

        {activePage === "dashboard" && (
          <Dashboard
            setActivePage={setActivePage}
            tickets={tickets}
            loading={ticketsLoading}
          />
        )}

        {activePage === "assistant" && (
          <Assistant
            message={message}
            setMessage={setMessage}
            loading={loading}
            result={result}
            diagnoseProblem={diagnoseProblem}
            handleKeyDown={handleKeyDown}
          />
        )}

        {activePage === "tickets" && (
          <Tickets
            tickets={tickets}
            loading={ticketsLoading}
            refresh={loadTickets}
          />
        )}

        {activePage === "diagnostics" && (
          <Diagnostics />
        )}

        {activePage === "knowledge" && (
          <KnowledgeBase />
        )}
      </main>
    </div>
  );
}


function Dashboard({ setActivePage, tickets, loading }) {
  const openTickets = tickets.filter(
    (ticket) => ticket.status === "Open"
  ).length;

  const highPriority = tickets.filter(
    (ticket) =>
      ticket.priority === "High" ||
      ticket.priority === "Critical"
  ).length;

  return (
    <section className="page">
      <div className="hero-card">
        <div>
          <span className="hero-label">HELPDESK AI AGENT</span>
          <h3>Diagnose IT problems with intelligent assistance.</h3>
          <p>
            Analyze technical issues, consult the knowledge base,
            run diagnostics, and escalate unresolved problems to
            human support.
          </p>

          <button
            className="primary-button"
            onClick={() => setActivePage("assistant")}
          >
            Open AI Assistant →
          </button>
        </div>

        <div className="hero-orb">✦</div>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Open Tickets"
          value={openTickets}
          icon="▣"
        />
        <StatCard
          label="High Priority"
          value={highPriority}
          icon="!"
        />
        <StatCard
          label="Agent Status"
          value="Ready"
          icon="✦"
        />
        <StatCard
          label="Knowledge Sources"
          value="6"
          icon="◫"
        />
      </div>

      <div className="section-heading">
        <div>
          <span className="eyebrow">RECENT ACTIVITY</span>
          <h3>Latest support tickets</h3>
        </div>

        <button
          className="text-button"
          onClick={() => setActivePage("tickets")}
        >
          View all →
        </button>
      </div>

      <TicketTable
        tickets={tickets.slice(0, 3)}
        loading={loading}
      />
    </section>
  );
}


function Assistant({
  message,
  setMessage,
  loading,
  result,
  diagnoseProblem,
  handleKeyDown,
}) {
  return (
    <section className="page">
      <div className="assistant-header">
        <span className="hero-label">AI ASSISTANT</span>
        <h3>Describe your problem</h3>
        <p>
          The agent will combine your report, verified diagnostics,
          and troubleshooting knowledge.
        </p>
      </div>

      <div className="input-card">
        <div className="input-status">
          <span className="live-dot" />
          Live
        </div>

        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Example: My Wi-Fi is connected but I cannot access the internet."
          rows={5}
        />

        <div className="input-footer">
          <span>Press Enter to diagnose</span>

          <button
            className="primary-button"
            onClick={diagnoseProblem}
            disabled={loading || !message.trim()}
          >
            {loading ? "Analyzing..." : "Diagnose Issue →"}
          </button>
        </div>
      </div>

      {result && (
        <DiagnosisResult result={result} />
      )}
    </section>
  );
}


function DiagnosisResult({ result }) {
  if (result.error) {
    return (
      <div className="error-card">
        <strong>Unable to complete diagnosis</strong>
        <p>{result.error}</p>
      </div>
    );
  }

  const escalation = result.escalation;
  const response = result.response;

  return (
    <section className="analysis-section">
      <div className="section-heading">
        <div>
          <span className="eyebrow">AGENT ANALYSIS</span>
          <h3>Diagnosis complete</h3>
        </div>

        <span className="category-badge">
          {result.category}
        </span>
      </div>

      <div className="diagnosis-card">
        <div className="diagnosis-answer">
          <pre>{response?.answer}</pre>
        </div>

        <div className="evidence-grid">
          <EvidenceCard
            title="TOOLS EXECUTED"
            value={`${result.tools_selected?.length || 0}`}
            subtitle="Real diagnostics"
          />

          <EvidenceCard
            title="KB SOURCES"
            value={`${response?.sources?.length || 0}`}
            subtitle="Relevant sources"
          />

          <EvidenceCard
            title="ESCALATION"
            value={escalation?.required ? "YES" : "NO"}
            subtitle={
              escalation?.required
                ? "Human support required"
                : "Not required"
            }
            danger={escalation?.required}
          />
        </div>

        {result.tool_results?.length > 0 && (
          <div className="evidence-panel">
            <div className="panel-heading">
              <span>Diagnostic Evidence</span>
              <small>VERIFIED</small>
            </div>

            {result.tool_results.map((tool) => (
              <div className="diagnostic-row" key={tool.tool}>
                <div>
                  <strong>{tool.tool}</strong>
                  <span>
                    {tool.status ||
                      tool.network_available ||
                      tool.operating_system ||
                      "Completed"}
                  </span>
                </div>

                <span className="verified-badge">
                  ✓ Verified
                </span>
              </div>
            ))}
          </div>
        )}

        {response?.sources?.length > 0 && (
          <div className="sources-panel">
            <div className="panel-heading">
              <span>Knowledge Sources</span>
              <small>RETRIEVED</small>
            </div>

            {response.sources.map((source, index) => (
              <div className="source-row" key={`${source.source}-${index}`}>
                <span>{source.source}</span>
                <small>
                  {source.category} · {source.score}
                </small>
              </div>
            ))}
          </div>
        )}

        {escalation?.required && escalation.ticket && (
          <div className="ticket-alert">
            <div>
              <span>ESCALATED TO HUMAN SUPPORT</span>
              <strong>{escalation.ticket.ticket_id}</strong>
            </div>

            <div>
              <small>
                Priority: {escalation.ticket.priority}
              </small>
              <small>
                Status: {escalation.ticket.status}
              </small>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}


function Tickets({ tickets, loading, refresh }) {
  return (
    <section className="page">
      <div className="page-intro">
        <div>
          <span className="eyebrow">TICKET MANAGEMENT</span>
          <h3>Support Tickets</h3>
          <p>
            Tickets created by the HelpDesk AI escalation engine.
          </p>
        </div>

        <button className="secondary-button" onClick={refresh}>
          ↻ Refresh
        </button>
      </div>

      <div className="ticket-summary">
        <span>{tickets.length} total tickets</span>
        <span>
          {tickets.filter((t) => t.status === "Open").length} open
        </span>
      </div>

      <TicketTable tickets={tickets} loading={loading} />
    </section>
  );
}


function TicketTable({ tickets, loading }) {
  if (loading) {
    return (
      <div className="empty-card">
        Loading support tickets...
      </div>
    );
  }

  if (!tickets.length) {
    return (
      <div className="empty-card">
        No support tickets found.
      </div>
    );
  }

  return (
    <div className="table-card">
      <div className="table-header">
        <span>Ticket</span>
        <span>Issue</span>
        <span>Category</span>
        <span>Priority</span>
        <span>Status</span>
      </div>

      {tickets.map((ticket) => (
        <div className="table-row" key={ticket.id}>
          <strong>{ticket.ticket_number}</strong>

          <div className="issue-cell">
            {ticket.problem}
            <small>
              {formatDate(ticket.created_at)}
            </small>
          </div>

          <span className="category-text">
            {ticket.category}
          </span>

          <span
            className={`priority ${ticket.priority.toLowerCase()}`}
          >
            {ticket.priority}
          </span>

          <span className="status-pill">
            {ticket.status}
          </span>
        </div>
      ))}
    </div>
  );
}


function Diagnostics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const runDiagnostics = async () => {
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/ai/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: "Run a general system and network diagnostic.",
          }),
        }
      );

      const result = await response.json();

      if (result.success) {
        setData(result.data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page">
      <div className="page-intro">
        <div>
          <span className="eyebrow">SYSTEM MONITORING</span>
          <h3>Diagnostics</h3>
          <p>
            Run real machine diagnostics through the HelpDesk AI
            agent.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={runDiagnostics}
          disabled={loading}
        >
          {loading ? "Running..." : "Run Diagnostics"}
        </button>
      </div>

      {!data && !loading && (
        <div className="empty-card">
          Run diagnostics to inspect the current machine state.
        </div>
      )}

      {data?.tool_results?.map((tool) => (
        <div className="diagnostic-card" key={tool.tool}>
          <div>
            <span className="diagnostic-icon">✓</span>
            <div>
              <strong>{tool.tool}</strong>
              <p>Verified machine result</p>
            </div>
          </div>

          <pre>{JSON.stringify(tool, null, 2)}</pre>
        </div>
      ))}
    </section>
  );
}


function KnowledgeBase() {
  const documents = [
    ["wifi.md", "Wi-Fi troubleshooting", "Network"],
    ["internet.md", "Internet connectivity", "Network"],
    ["printer.md", "Printer troubleshooting", "Printer"],
    ["bluetooth.md", "Bluetooth troubleshooting", "Bluetooth"],
    ["windows.md", "Windows system issues", "System"],
    ["software.md", "Software troubleshooting", "Software"],
  ];

  return (
    <section className="page">
      <div className="page-intro">
        <div>
          <span className="eyebrow">KNOWLEDGE CENTER</span>
          <h3>Knowledge Base</h3>
          <p>
            Local troubleshooting knowledge available to the AI
            support agent.
          </p>
        </div>

        <div className="knowledge-count">
          {documents.length} sources
        </div>
      </div>

      <div className="knowledge-grid">
        {documents.map(([file, title, category]) => (
          <div className="knowledge-card" key={file}>
            <div className="knowledge-icon">◫</div>
            <div>
              <strong>{title}</strong>
              <span>{file}</span>
              <small>{category}</small>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}


function StatCard({ label, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


function EvidenceCard({ title, value, subtitle, danger }) {
  return (
    <div className={`evidence-card ${danger ? "danger" : ""}`}>
      <span>{title}</span>
      <strong>{value}</strong>
      <small>{subtitle}</small>
    </div>
  );
}


function formatDate(value) {
  if (!value) return "Unknown time";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}


export default App;
