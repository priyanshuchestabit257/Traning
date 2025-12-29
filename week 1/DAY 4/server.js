const http = require("http");

let counter = 0;

const server = http.createServer((req, res) => {
  if (req.url === "/ping") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ timestamp: Date.now() }));
  }

  if (req.url === "/headers") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify(req.headers, null, 2));
  }

  if (req.url === "/count") {
    counter++;
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ count: counter }));
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Not found" }));
});

server.listen(8000, () => console.log("Server running on http://localhost:8000"));
