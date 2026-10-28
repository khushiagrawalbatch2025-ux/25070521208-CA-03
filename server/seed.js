require("dotenv").config();
const mongoose = require("mongoose");
const Product = require("./models/Product");
const data = [
  { name: "Butterfly Clips (6 pack)", price: 8, category: "Accessories", emoji: "🦋", description: "Glitter wings, zero chill." },
  { name: "Baby Tee – Cherry", price: 22, category: "Clothing", emoji: "🍒", description: "Cropped, stretchy, iconic." },
  { name: "Low-Rise Flares", price: 48, category: "Clothing", emoji: "👖", description: "Washed denim with rhinestone pockets." },
  { name: "Mini Shoulder Bag", price: 35, category: "Bags", emoji: "👛", description: "Pink pleather, silver chain." },
  { name: "Platform Sneakers", price: 64, category: "Shoes", emoji: "👟", description: "Chunky sole, holographic trim." },
  { name: "Flip Phone Case", price: 14, category: "Tech", emoji: "📱", description: "Jelly gel, charm loop included." },
  { name: "Frosted Lip Gloss", price: 9, category: "Beauty", emoji: "💋", description: "Sticky-shiny, strawberry scent." },
  { name: "Inflatable Chair", price: 40, category: "Home", emoji: "🫧", description: "Clear blue vinyl for your room." },
];
mongoose.connect(process.env.MONGO_URI).then(async () => {
  await Product.deleteMany({});
  await Product.insertMany(data);
  console.log("Seeded", data.length, "products");
  process.exit(0);
});
