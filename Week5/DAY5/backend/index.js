import express from "express";
import mongoose from "mongoose";

const app = express();
app.use(express.json());

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error(err));

const TodoSchema = new mongoose.Schema({
  title: String,
  completed: { type: Boolean, default: false }
});

const Todo = mongoose.model("Todo", TodoSchema);

app.get("/health", (req, res) => res.send("OK"));

app.get("/api/todos", async (req, res) => {
  const todos = await Todo.find();
  res.json(todos);
});

app.post("/api/todos", async (req, res) => {
  const todo = await Todo.create(req.body);
  res.json(todo);
});

app.listen(3000, () => {
  console.log("Backend running on 3000");
});
