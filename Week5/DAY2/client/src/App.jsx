import { useEffect, useState } from "react";

function App() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/api")
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Client</h1>
      <p>{msg}</p>
    </div>
  );
}

export default App;

