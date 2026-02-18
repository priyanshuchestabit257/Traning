import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";

// Rate Limiting
export const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minutes
  max: 5, // 100 requests per IP
  message: {
    success: false,
    message: "Too many requests, please try again later",
  },
});

// CORS Policy
export const corsPolicy = cors({
  origin: ["http://localhost:3000"], // frontend origin
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
});

// Helmet (Security Headers)
export const securityHeaders = helmet();
