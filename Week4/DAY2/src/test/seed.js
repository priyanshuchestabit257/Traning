import mongoose from "mongoose";
import Account from "../models/Account.js";
import Order from "../models/Order.js";
import config from "../config/index.js";

async function seed() {
  try {
    await mongoose.connect(config.databaseUrl);
    console.log("Database connected");

    // Clear old data
    await Account.deleteMany({});
    await Order.deleteMany({});

    // Create accounts
    const accounts = await Account.insertMany([
      {
        firstName: "John",
        lastName: "Doe",
        email: "john@example.com",
        password: "password123", // hashed automatically
        status: "ACTIVE",
      },
      {
        firstName: "Jane",
        lastName: "Smith",
        email: "jane@example.com",
        password: "password123",
        status: "ACTIVE",
      },
    ]);

    console.log("Accounts created");

    // Create orders
    const orders = await Order.insertMany([
      {
        accountId: accounts[0]._id,
        items: [
          { productName: "Product A", price: 500, quantity: 5 },
        ],
        status: "PAID",
      },
      {
        accountId: accounts[0]._id,
        items: [
          { productName: "Product B", price: 500, quantity: 3 },
        ],
        status: "PENDING",
      },
      {
        accountId: accounts[1]._id,
        items: [
          { productName: "Product C", price: 1000, quantity: 3 },
        ],
        status: "PAID",
      },
    ]);

    console.log("Orders created");

    console.log("Seeding completed successfully");
    await mongoose.disconnect();
  } catch (err) {
    console.error("Seeding failed", err);
    await mongoose.disconnect();
    process.exit(1);
  }
}

seed();
