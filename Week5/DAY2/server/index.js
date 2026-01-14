import express from "express";
import mongoose from "mongoose";
import cors from "cors";

const app = express();
app.use(cors());

mongoose
  .connect("mongodb://mongo:27017/day2db")
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error(err));

app.get("/api", (req, res) => {
  res.json({ message: "Hello from Server " });
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});
