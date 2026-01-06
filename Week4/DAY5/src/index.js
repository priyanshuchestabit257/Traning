import express from "express";
import mongoose from "mongoose";
import { tracingMiddleware } from "./utils/tracing.js";
import { limiter, corsPolicy, securityHeaders } from "./middlewares/security.js";
import { errorMiddleware } from "./middlewares/error.middleware.js";
import { getProducts } from "./controllers/product.controller.js";
import emailRoutes from "./routes/email.routes.js";

const app = express();

const PORT = process.env.PORT || 3000;
const MONGO_URI =
  process.env.MONGO_URI || "mongodb://127.0.0.1:27017/mydatabase";

// Body parsers FIRST
app.use(express.json({ limit: "10kb" }));
app.use(express.urlencoded({ extended: true, limit: "10kb" }));

// Tracing
app.use(tracingMiddleware);

// Security
app.use(securityHeaders);
app.use(corsPolicy);
app.use(limiter);

// Routes
app.use("/emails", emailRoutes);
app.use("/products", getProducts);

// Error handler LAST
app.use(errorMiddleware);

// DB + server
mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log("Connected to MongoDB");
    app.listen(PORT, () =>
      console.log(`Server running on http://localhost:${PORT}`)
    );
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
    process.exit(1);
  });
