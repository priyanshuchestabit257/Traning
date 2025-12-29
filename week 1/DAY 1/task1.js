const os = require("os");
const { exec } = require("child_process");
const net = require("net");


function run(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (err, stdout, stderr) => {
      if (err) return resolve(""); 
      resolve(stdout.trim());
    });
  });
}


function getHostName() {
  return os.hostname();
}


async function getDiskSpace() {
  if (process.platform === "win32") {
    const output = await run(`wmic logicaldisk where "DeviceID='C:'" get FreeSpace /value`);
    const match = output.match(/FreeSpace=(\d+)/);
    return match ? (match[1] / 1024 / 1024 / 1024).toFixed(2) + " GB" : "Unavailable";
  } else {
    return await run("df -h / | tail -1 | awk '{print $4}'");
  }
}


async function getDefaultGateway() {
  if (process.platform === "win32") {
    const out = await run("ipconfig");
    const match = out.match(/Default Gateway[ .:]*([0-9.]+)/);
    return match ? match[1] : "Unknown";
  } else {
    return await run("ip route | grep default | awk '{print $3}'");
  }
}


async function getLoggedInUsers() {
  if (process.platform === "win32") {
    const out = await run("query user");
    const lines = out.split("\n").filter(x => x.trim().length > 0);
    return lines.length > 1 ? lines.length - 1 : 0;
  } else {
    return await run("who | wc -l");
  }
}


async function scanOpenPorts(ports) {
  const openPorts = [];

  const check = (port) => {
    return new Promise((resolve) => {
      const socket = new net.Socket();

      socket.setTimeout(200);

      socket.once("connect", () => {
        openPorts.push(port);
        socket.destroy();
        resolve();
      });

      socket.once("timeout", () => {
        socket.destroy();
        resolve();
      });

      socket.once("error", () => {
        socket.destroy();
        resolve();
      });

      socket.connect(port, "127.0.0.1");
    });
  };

  for (const port of ports) {
    await check(port);
  }

  return openPorts;
}


async function main() {
  console.log("=== SYSTEM INFORMATION ===");
  

  console.log("Host Name:", getHostName());
  console.log("Available Disk Space:", await getDiskSpace());
  console.log("Default Gateway:", await getDefaultGateway());
  console.log("User Count:", await getLoggedInUsers());

  const portsToCheck = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080, 3000, 5000];
  console.log("Scanning open ports...");

  const open = await scanOpenPorts(portsToCheck);
  console.log("Open Ports:", open.length ? open.join(", ") : "None");
}

main();


