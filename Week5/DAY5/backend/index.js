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

app.get("/health", (req, res) => {
  res.send("OK");
});

app.get("/api/todos", async (req, res) => {
  const todos = await Todo.find();
  res.json(todos);
});

app.post("/api/todos", async (req, res) => {
  const todo = await Todo.create({
    title: req.body.title,
    completed: false
  });
  res.json(todo);
});

// TOGGLE completed
app.put("/api/todos/:id", async (req, res) => {
  const todo = await Todo.findById(req.params.id);
  todo.completed = !todo.completed;
  await todo.save();
  res.json(todo);
});

// DELETE todo
app.delete("/api/todos/:id", async (req, res) => {
  await Todo.findByIdAndDelete(req.params.id);
  res.json({ message: "Todo deleted" });
});

app.patch("/api/todos/:id", async (req, res) => {
  const todo = await Todo.findByIdAndUpdate(
    req.params.id,
    { completed: req.body.completed },
    { new: true }
  );
  res.json(todo);
});


app.listen(3000, () => {
  console.log("Backend running on 3000");
});
