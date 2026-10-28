import { useEffect, useState } from "react";

export default function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({}); // id -> qty
  const [form, setForm] = useState({ name: "", email: "", address: "" });
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/products").then((r) => r.json()).then(setProducts)
      .catch(() => setError("Can't reach the server. Is the backend running?"));
  }, []);

  const add = (id, d = 1) => setCart((c) => {
    const qty = (c[id] || 0) + d;
    const next = { ...c };
    qty > 0 ? (next[id] = qty) : delete next[id];
    return next;
  });

  const lines = products.filter((p) => cart[p._id]).map((p) => ({ ...p, qty: cart[p._id] }));
  const total = lines.reduce((s, l) => s + l.price * l.qty, 0);

  const checkout = async (e) => {
    e.preventDefault();
    setStatus(""); setError("");
    const res = await fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer: form, items: lines.map((l) => ({ id: l._id, qty: l.qty })) }),
    });
    const data = await res.json();
    if (!res.ok) return setError(data.error);
    setStatus(`Order #${data._id.slice(-6)} placed! Total $${data.total}`);
    setCart({});
  };

  return (
    <>
      <div className="marquee"><span>✦ free shipping over $50 ✦ new drops every friday ✦ welcome to the future ✦ free shipping over $50 ✦ new drops every friday ✦</span></div>
      <header className="hero">
        <h1>neel</h1>
        <p>shop the future, dress like 2000</p>
        <span className="star s1">✦</span><span className="star s2">★</span><span className="star s3">✧</span>
      </header>

      <main className="layout">
        <section className="win">
          <div className="titlebar"><span>products.exe</span><b>_ □ ✕</b></div>
          <div className="grid">
            {products.map((p) => (
              <article className="card" key={p._id}>
                <div className="emoji">{p.emoji}</div>
                <h3>{p.name}</h3>
                <p>{p.description}</p>
                <div className="row"><strong>${p.price}</strong>
                  <button className="gloss" onClick={() => add(p._id)}>Add to cart</button></div>
              </article>
            ))}
          </div>
        </section>

        <aside className="win cart">
          <div className="titlebar"><span>cart.exe</span><b>_ □ ✕</b></div>
          <div className="pad">
            {lines.length === 0 && <p>Your cart is empty. Add something shiny.</p>}
            {lines.map((l) => (
              <div className="line" key={l._id}>
                <span>{l.emoji} {l.name}</span>
                <span className="qty">
                  <button onClick={() => add(l._id, -1)}>−</button>{l.qty}<button onClick={() => add(l._id, 1)}>+</button>
                </span>
              </div>
            ))}
            <p className="total">Total: ${total}</p>
            <form onSubmit={checkout}>
              {["name", "email", "address"].map((f) => (
                <input key={f} placeholder={f} type={f === "email" ? "email" : "text"} required
                  value={form[f]} onChange={(e) => setForm({ ...form, [f]: e.target.value })} />
              ))}
              <button className="gloss big" disabled={!lines.length}>Place order</button>
            </form>
            {status && <p className="ok">{status}</p>}
            {error && <p className="err">{error}</p>}
          </div>
        </aside>
      </main>
    </>
  );
}
