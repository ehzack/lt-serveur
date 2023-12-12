const { spawn } = require("child_process");
const io = require("socket.io-client");
const request = require("request-promise");
const sleep = require("util").promisify(setTimeout);

const url = "http://localhost:3001/ip-adresses";
const serverUrl = "http://localhost:4001";

async function getIPStatus() {
  try {
    const response = await request.get(url, { json: true });
    return response.map((item) => ({ ip: item.ipAdress, status: "UNKNOWN" }));
  } catch (error) {
    console.error(`Error: ${error}`);
    return [];
  }
}

async function pingIP(ip, prevStatus) {
  return new Promise((resolve, reject) => {
    const pingProcess = spawn("ping", ["-n", "1", "-w", "1000", ip]);
    pingProcess.on("exit", (code) => {
      const status = code === 0;
      if (prevStatus !== status) {
        resolve({ ip, status });
      } else {
        resolve(null);
      }
    });
    pingProcess.on("error", (error) => {
      reject(error);
    });
  });
}

async function broadcastData(data, socket) {
  socket.emit("ipAdress", data);
}

async function main() {
  const ipStatus = await getIPStatus();
  const socket = io.connect(serverUrl);
  console.log(`Connected to socket.io server ${serverUrl}`);

  let prevStatus = {};

  while (true) {
    const ipStatus2 = await Promise.all(ipStatus.map(async (ipObj) => {
      try {
        const result = await pingIP(ipObj.ip, prevStatus[ipObj.ip]);
        if (result) {
          prevStatus[ipObj.ip] = result.status;
          return result;
        }
      } catch (error) {
        console.error(`Error pinging IP ${ipObj.ip}: ${error}`);
      }
    }));

    const filteredIPStatus = ipStatus2.filter(Boolean);

    if (filteredIPStatus.length > 0) {
      if (socket.connected) {
        console.log("Socket connected, in port 4001");
        broadcastData(filteredIPStatus, socket);
      } else {
        console.log(" Le socket est déconnecté et il est impossible de diffuser des données. Veuillez exécuter le code backend");
      }
    }

    await sleep(1000);
  }
}

main();
