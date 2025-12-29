const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-btn");
const list = document.getElementById("todo-list");

let todos = JSON.parse(localStorage.getItem("todos")) || [];


function renderTodos() {
    list.innerHTML = "";

    todos.forEach((todo, index) => {
        const li = document.createElement("li");
        if (todo.done) li.classList.add("done");

        li.innerHTML = `
            <div class="left">
                <input type="checkbox" class="checkbox" ${todo.done ? "checked" : ""}>
                <span class="todo-text">${todo.text}</span>
            </div>
            <div class="actions">
                <button class="edit-btn">Edit</button>
                <button class="delete-btn">Delete</button>
            </div>
        `;

        const checkbox = li.querySelector(".checkbox");
        const deleteBtn = li.querySelector(".delete-btn");
        const editBtn = li.querySelector(".edit-btn");
        const textSpan = li.querySelector(".todo-text");

        
        checkbox.addEventListener("change", () => {
            todos[index].done = checkbox.checked;
            saveTodos();
            renderTodos();
        });

        
        deleteBtn.addEventListener("click", () => {
            todos.splice(index, 1);
            saveTodos();
            renderTodos();
        });

        
        editBtn.addEventListener("click", () => {
            const inputBox = document.createElement("input");
            inputBox.value = todo.text;
            inputBox.className = "edit-input";

            li.querySelector(".left").replaceChild(inputBox, textSpan);

            editBtn.textContent = "Save";

            editBtn.onclick = () => {
                const newValue = inputBox.value.trim();
                if (!newValue) return;

                todos[index].text = newValue;
                saveTodos();
                renderTodos();
            };

            inputBox.addEventListener("keyup", (e) => {
                if (e.key === "Enter") editBtn.click();
            });

            inputBox.focus();
        });

        list.appendChild(li);
    });
}

renderTodos();


addBtn.addEventListener("click", () => {
    const textValue = input.value.trim();
    if (!textValue) return;

    todos.push({ text: textValue, done: false });
    saveTodos();
    renderTodos();
    input.value = "";
});


function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos));
}
