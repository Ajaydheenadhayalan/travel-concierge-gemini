import React, { useState } from "react";
import axios from "axios";

function Badge({ children, bg = "#eef2ff" }) {
  return <span style={{ background: bg, padding: "6px 10px", borderRadius: 999, fontSize: 13 }}>{children}</span>;
}

export default function App() {
  const [userId, setUserId] = useState("ajay");
  const [destination, setDestination] = useState("Chennai");
  const [budget, setBudget] = useState(1000);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refineText, setRefineText] = useState("");
  const [history, setHistory] = useState([]);

  async function createPlan() {
    setLoading(true);
    try {
      const resp = await axios.post("/api/plan", {
        user_id: userId,
        origin: "Salem",
        destination,
        start_date: "2025-12-10",
        end_date: "2025-12-12",
        budget
      });
      setPlan(resp.data);
      setHistory(h => [{ type: "plan", payload: resp.data, time: Date.now() }, ...h]);
    } catch (e) {
      alert("Plan request failed: " + (e.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  }

  async function refinePlan() {
    if (!plan) return alert("Generate a plan first");
    setLoading(true);
    try {
      const resp = await axios.post("/api/refine", { user_id: userId, message: refineText });
      setPlan(resp.data);
      setHistory(h => [{ type: "refine", payload: resp.data, msg: refineText, time: Date.now() }, ...h]);
      setRefineText("");
    } catch (e) {
      alert("Refine failed: " + (e.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  }

  const total = plan?.total_estimated_cost ?? 0;
  const confidence = Math.round((plan?.confidence_score ?? 0.7) * 100);

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1>Travel Concierge <small className="muted">(Agent)</small></h1>
          <p className="muted">AI-powered itinerary & hotel recommendations — refine naturally.</p>
        </div>
        <img alt="screenshot" src="/assets/agent-snapshot.png" className="logo" />
      </header>

      <section className="controls">
        <input value={userId} onChange={e=>setUserId(e.target.value)} placeholder="User ID" />
        <input value={destination} onChange={e=>setDestination(e.target.value)} placeholder="Destination" />
        <input type="number" value={budget} onChange={e=>setBudget(Number(e.target.value))} placeholder="Budget" />
        <button className="primary" onClick={createPlan} disabled={loading}>{loading ? "Working..." : "Plan Trip"}</button>
      </section>

      <main className="grid">
        <div className="card large">
          <h2>Itinerary</h2>
          {!plan && <div className="placeholder">No plan yet — enter inputs and click <strong>Plan Trip</strong>.</div>}
          {plan && (
            <>
              {/* Render itinerary nicely instead of JSON */}
              {Object.entries(plan.itinerary || {}).map(([day, block]) => (
                <div key={day} className="day">
                  <h3>{day.replace("_"," ").toUpperCase()}</h3>
                  <div className="slots">
                    {Object.entries(block).map(([slot, item]) => (
                      <div key={slot} className="slot">
                        <strong className="slot-name">{slot}</strong>
                        <div className="slot-body">
                          {item && item.name ? (
                            <>
                              <div className="item-title">{item.name}</div>
                              <div className="muted">{item.desc || ""} • {item.time || ""}</div>
                            </>
                          ) : <div className="muted">No plan</div>}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </>
          )}
        </div>

        <aside className="card side">
          <h3>Hotels</h3>
          {plan?.hotels?.length ? (
            <ul className="hotels">
              {plan.hotels.map((h, i) => (
                <li key={i} className="hotel">
                  <div>
                    <div className="hotel-title">{h.name}</div>
                    <div className="muted">{h.rating ? `★ ${h.rating}` : ""}</div>
                  </div>
                  <div style={{textAlign:"right"}}>
                    <Badge>₹{h.price_per_night}</Badge>
                    <div><a href={h.link} target="_blank" rel="noreferrer">Book</a></div>
                  </div>
                </li>
              ))}
            </ul>
          ) : <div className="muted">No hotels yet</div>}

          <div className="summary">
            <h4>Total</h4>
            <div className="total">₹{total}</div>
            <div className="confidence">
              <div className="muted">Confidence</div>
              <div className="conf-bar"><div style={{width: `${confidence}%`}} className="conf-fill" /></div>
              <div className="muted small">{confidence}%</div>
            </div>
          </div>

          <div className="refine">
            <h4>Refine</h4>
            <input placeholder="e.g. make it cheaper / add a museum" value={refineText} onChange={e=>setRefineText(e.target.value)} />
            <button onClick={refinePlan} className="secondary" disabled={loading || !refineText}>Refine Plan</button>
          </div>
        </aside>
      </main>

      <section className="history card">
        <h4>Activity</h4>
        {history.length === 0 && <div className="muted">No activity yet.</div>}
        <ul>
          {history.map((h, idx) => (
            <li key={idx}><strong>{h.type}</strong> — {new Date(h.time).toLocaleTimeString()} {h.msg ? `: "${h.msg}"` : ""}</li>
          ))}
        </ul>
      </section>

      <footer className="muted small">Agent demo • Use with care — do not auto-book without confirmation.</footer>
    </div>
  );
}

