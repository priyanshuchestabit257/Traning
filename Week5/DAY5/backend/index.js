import express from "express";

const app = express();
app.use(express.json());

let todos = [];

app.get("/health", (req, res) => {
  res.status(200).send("OK");
});


app.get("/todos", (req, res) => {
  res.json(todos);
});

app.post("/todos", (req, res) => {
  const todo = {
    id: Date.now(),
    text: req.body.text
  };
  todos.push(todo);
  res.status(201).json(todo);
});

app.listen(3000, () => {
  console.log("Backend running on port 3000");
});
