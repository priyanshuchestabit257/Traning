async function loadTodos() {
  const res = await fetch("/api/todos");
  const todos = await res.json();

  const list = document.getElementById("todoList");
  list.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");
    li.innerText = todo.text;
    list.appendChild(li);
  });
}

async function addTodo() {
  const input = document.getElementById("todoInput");

  await fetch("/api/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input.value })
  });

  input.value = "";
  loadTodos();
}

loadTodos();
