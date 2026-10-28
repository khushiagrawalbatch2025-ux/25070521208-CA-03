require("dotenv").config();
const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const Product = require("./models/Product");
const Order = require("./models/Order");

const app = express();
app.use(cors());
app.use(express.json());

app.get("/api/products", async (req, res) => {
  const filter = req.query.category ? { category: req.query.category } : {};
  res.json(await Product.find(filter));
});

app.post("/api/orders", async (req, res) => {
  try {
    const { customer, items } = req.body;
    if (!customer?.name || !customer?.email || !customer?.address || !items?.length)
      return res.status(400).json({ error: "Name, email, address and at least one item are required." });
    const products = await Product.find({ _id: { $in: items.map((i) => i.id) } });
    const lines = items.map((i) => {
      const p = products.find((x) => String(x._id) === i.id);
      return p && { product: p._id, name: p.name, price: p.price, qty: i.qty };
    });
    if (lines.includes(undefined)) return res.status(400).json({ error: "Unknown product in cart." });
    const total = lines.reduce((s, l) => s + l.price * l.qty, 0);
    res.status(201).json(await Order.create({ customer, items: lines, total }));
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get("/api/orders", async (req, res) => {
  const filter = req.query.email ? { "customer.email": req.query.email } : {};
  res.json(await Order.find(filter).sort({ createdAt: -1 }));
});

mongoose.connect(process.env.MONGO_URI).then(() => {
  console.log("MongoDB connected");
  app.listen(process.env.PORT, () => console.log(`neel API on :${process.env.PORT}`));
}).catch((e) => { console.error(e.message); process.exit(1); });
