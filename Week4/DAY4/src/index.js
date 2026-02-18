// server.js
import express from "express";
import mongoose from "mongoose";
import { limiter, corsPolicy, securityHeaders } from "./middlewares/security.js";
import { errorMiddleware } from "./middlewares/error.middleware.js";
import productRoutes from "./routes/product.routes.js";

const app = express();

const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/mydatabase";

// Middleware: parse JSON and URL-encoded data (with size limits)
app.use(express.json({ limit: "10kb" }));
app.use(express.urlencoded({ extended: true, limit: "10kb" }));

// Security Middlewares
app.use(securityHeaders);
app.use(corsPolicy);
app.use(limiter);

// Routes
app.use("/products", productRoutes);


// Error handling middleware (should be last)
app.use(errorMiddleware);

// Connect to MongoDB and start server
mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log(" Connected to MongoDB");
    app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
    process.exit(1);
  });
