import mongoose from "mongoose";
import Product from "../models/product.model.js";

const MONGO_URI = "mongodb://127.0.0.1:27017/mydatabase";

const seed = async () => {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("MongoDB connected for seeding");

    await Product.deleteMany({});

    await Product.insertMany([
      { name: "iPhone 13", price: 800, tags: ["apple", "phone"] },
      { name: "iPhone 14 Pro", price: 1100, tags: ["apple", "phone"] },
      { name: "Samsung Galaxy S23", price: 900, tags: ["samsung", "phone"] },
      { name: "MacBook Air", price: 1200, tags: ["apple", "laptop"] },
      { name: "Dell XPS 13", price: 1000, tags: ["dell", "laptop"] }
    ]);

    console.log("Seeding complete");
    process.exit(0);
  } catch (err) {
    console.error("Seeding failed", err);
    process.exit(1);
  }
};

seed();
