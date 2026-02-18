import express from "express";
import mongoose from "mongoose";
import productRoutes from "./routes/product.routes.js";
import { errorMiddleware } from "./middlewares/error.middleware.js";
import accountRoutes from "./routes/account.routes.js";



const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI =
  process.env.MONGO_URI || "mongodb://127.0.0.1:27017/mydatabase";

// middleware
app.use(express.json());

// routes
app.use("/products", productRoutes);

app.use("/accounts", accountRoutes);

// error handler (ALWAYS LAST)
app.use(errorMiddleware);


// connect DB + start server
mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log("MongoDB connected");
    app.listen(PORT, () =>
      console.log(`Server running on port ${PORT}`)
    );
  })
  .catch((err) => {
    console.error("DB connection failed", err);
    process.exit(1);
  });
