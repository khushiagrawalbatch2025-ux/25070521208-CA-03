const mongoose = require("mongoose");
module.exports = mongoose.model("Order", new mongoose.Schema({
  customer: { name: String, email: String, address: String },
  items: [{ product: { type: mongoose.Schema.Types.ObjectId, ref: "Product" }, name: String, price: Number, qty: Number }],
  total: Number,
}, { timestamps: true }));
