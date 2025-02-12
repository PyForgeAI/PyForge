import { Socket } from "socket.io-client";
import { WsMessage } from "../../src/context/wsUtils";
import { PyForgeApp } from "./app";

export const initSocket = (socket: Socket, pyforgeApp: PyForgeApp) => {
    socket.on("connect", () => {
        pyforgeApp.onWsMessageEvent("connect", null);
        if (pyforgeApp.clientId === "" || pyforgeApp.appId === "") {
            pyforgeApp.init();
        }
    });
    // Send a request to get App ID to verify that the app has not been reloaded
    socket.io.on("reconnect", () => {
        pyforgeApp.onWsMessageEvent("reconnect", null);
        console.log("WebSocket reconnected");
        pyforgeApp.sendWsMessage("AID", "reconnect", pyforgeApp.appId);
    });
    // try to reconnect on connect_error
    socket.on("connect_error", (err) => {
        pyforgeApp.onWsMessageEvent("connect_error", { err });
        console.log("Error connecting WebSocket: ", err);
        setTimeout(() => {
            socket && socket.connect();
        }, 500);
    });
    // try to reconnect on server disconnection
    socket.on("disconnect", (reason, details) => {
        pyforgeApp.onWsMessageEvent("disconnect", { reason, details });
        console.log("WebSocket disconnected due to: ", reason, details);
        if (reason === "io server disconnect") {
            socket && socket.connect();
        }
    });
    // handle message data from backend
    socket.on("message", (message: WsMessage) => {
        pyforgeApp.onWsMessageEvent("message", message);
        // handle messages with registered websocket adapters
        for (const adapter of pyforgeApp.wsAdapters) {
            if (adapter.supportedMessageTypes.includes(message.type)) {
                const messageResolved = adapter.handleWsMessage(message, pyforgeApp);
                if (messageResolved) {
                    return;
                }
            }
        }
    });
    // only now does the socket tries to open/connect
    if (!socket.connected) {
        socket.connect();
    }
};
