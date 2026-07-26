import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ArrowRight, RotateCcw } from "lucide-react";
import "./styles.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

function App() {
  const [text, setText] = useState("");
  const [shift, setShift] = useState(3);
  const [output, setOutput] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  async function processText(event) {
    event.preventDefault();
    setStatus("loading");
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/periodic-table-encode-simple`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text, shift })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Unable to process the text.");
      }

      setOutput(data.output);
      setStatus("done");
    } catch (err) {
      setOutput("");
      setError(err.message);
      setStatus("error");
    }
  }

  function reset() {
    setText("");
    setShift(3);
    setOutput("");
    setError("");
    setStatus("idle");
  }

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="page-title">
        <div className="title-row">
          <div>
            <p className="eyebrow">Render Flask + React</p>
            <h1 id="page-title">Periodic Table Encoding</h1>
          </div>
          <button className="icon-button" type="button" onClick={reset} aria-label="Reset form">
            <RotateCcw size={20} aria-hidden="true" />
          </button>
        </div>

        <form className="converter" onSubmit={processText}>
          <label className="field-group">
            <span>Input text</span>
            <textarea
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="Type text to shift"
              rows={7}
            />
          </label>

          <div className="controls">
            <label className="shift-control">
              <span>Shift</span>
              <input
                type="number"
                min="-25"
                max="25"
                value={shift}
                onChange={(event) => setShift(event.target.value)}
              />
            </label>

            <button className="primary-button" type="submit" disabled={status === "loading"}>
              <span>{status === "loading" ? "Processing" : "Process"}</span>
              <ArrowRight size={18} aria-hidden="true" />
            </button>
          </div>

          <label className="field-group">
            <span>Output text</span>
            <textarea value={output} readOnly placeholder="Shifted text appears here" rows={7} />
          </label>
        </form>

        {error && <p className="error-message">{error}</p>}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
