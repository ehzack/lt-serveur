const { spawn } = require("child_process");
const io = require("socket.io-client");
const request = require("request-promise");
const sleep = require("util").promisify(setTimeout);

const url = "http://localhost:3001/ip-adresses";
const serverUrl = "http://localhost:4001";

/**
 * Retrieves IP addresses' status from the server.
 * @returns {Array} An array of IP status objects.
 */
async function getIPStatus() {
  const ipStatus = [];

  try {
    const response = await request.get(url, { json: true });
    if (response) {
      const data = response;
      for (const item of data) {
        ipStatus.push({ ip: item.ipAdress, status: "UNKNOWN" });
      }
    }
  } catch (error) {
    console.error(`Error: ${error}`);
  }

  return ipStatus;
}

/**
 * Pings an IP address and resolves with the result.
 * @param {string} ip The IP address to ping.
 * @param {boolean} prevStatus The previous status of the IP address.
 * @returns {Object|null} An object with IP and status if there's a change, or null otherwise.
 */
async function pingIP(ip, prevStatus) {
  return new Promise((resolve, reject) => {
    const pingProcess = spawn("ping", ["-n", "1", "-w", "1000", ip]);
    pingProcess.on("exit", (code) => {
      let status;
      if (code === 0) {
        status = true;
      } else {
        status = false;
      }
      if (prevStatus !== status) {
        resolve({ ip, status });
      } else {
        resolve(null);
      }
    });
  });
}

/**
 * Broadcasts IP address data to the server using the socket.
 * @param {Array} data The array of IP status objects to broadcast.
 * @param {Object} socket The socket instance.
 */
async function broadcastData(data, socket) {
  socket.emit("ipAdress", data);
}

/**
 * The main function that runs the IP monitoring process.
 */
async function main() {
  const ipStatus = await getIPStatus();

  // Create socket.io client and connect to server
  const socket = io.connect(serverUrl);
  console.log(`Connected to socket.io server ${serverUrl}`);

  // Ping IP addresses and broadcast results to server
  let prevStatus = {};
  while (true) {
    const ipStatus2 = [];
    for (const ipObj of ipStatus) {
      const result = await pingIP(ipObj.ip, prevStatus[ipObj.ip]);
      if (result) {
        ipStatus2.push(result);
        prevStatus[ipObj.ip] = result.status;
      }
    }
    if (ipStatus2.length > 0) {
      const data = ipStatus2;
      // Check if socket is still connected before broadcasting data
      if (socket.connected) {
        console.log("Socket connected, in port 4001");
        broadcastData(data, socket);
      } else {
        console.log("Socket disconnected, unable to broadcast data");
      }
    }
    await sleep(1000);
  }
}

main();
