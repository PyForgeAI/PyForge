import merge from "lodash/merge";
import { PyForgeApp } from "./app";
import { IdMessage, storeClientId } from "../../src/context/utils";
import { WsMessage } from "../../src/context/wsUtils";
import { DataManager, getRequestedDataKey, ModuleData } from "./dataManager";

export abstract class WsAdapter {
    abstract supportedMessageTypes: string[];

    abstract handleWsMessage(message: WsMessage, app: PyForgeApp): boolean;
}

interface MultipleUpdatePayload {
    name: string;
    payload: { value: unknown };
}

interface AlertMessage extends WsMessage {
    atype: string;
    message: string;
}

export class PyForgeWsAdapter extends WsAdapter {
    supportedMessageTypes: string[];
    initWsMessageTypes: string[];
    constructor() {
        super();
        this.supportedMessageTypes = ["MU", "ID", "GMC", "GDT", "AID", "GR", "AL", "ACK"];
        this.initWsMessageTypes = ["ID", "AID", "GMC"];
    }
    handleWsMessage(message: WsMessage, pyforgeApp: PyForgeApp): boolean {
        if (message.type) {
            if (message.type === "MU" && Array.isArray(message.payload)) {
                for (const muPayload of message.payload as [MultipleUpdatePayload]) {
                    const encodedName = muPayload.name;
                    const { value } = muPayload.payload;
                    if (value && (value as any).__pyforge_refresh !== undefined) {
                        // refresh all requested data for this encodedName var
                        const requestDataOptions = pyforgeApp.variableData?._requested_data[encodedName];
                        for (const dataKey in requestDataOptions) {
                            const requestDataEntry = requestDataOptions[dataKey];
                            const { options } = requestDataEntry;
                            pyforgeApp.sendWsMessage("DU", encodedName, options);
                        }
                        return true;
                    }
                    const dataKey = getRequestedDataKey(muPayload.payload);
                    pyforgeApp.variableData?.update(encodedName, value, dataKey);
                    // call the callback if it exists for request data
                    if (dataKey && (encodedName in pyforgeApp._rdc && dataKey in pyforgeApp._rdc[encodedName])) {
                        const cb = pyforgeApp._rdc[encodedName]?.[dataKey];
                        cb(pyforgeApp, encodedName, dataKey, value);
                        delete pyforgeApp._rdc[encodedName][dataKey];
                    }
                    pyforgeApp.onChangeEvent(encodedName, value, dataKey);
                }
            } else if (message.type === "ID") {
                const { id } = message as unknown as IdMessage;
                storeClientId(id);
                pyforgeApp.clientId = id;
                pyforgeApp.initApp();
                pyforgeApp.updateContext(pyforgeApp.path);
            } else if (message.type === "GMC") {
                const payload = message.payload as Record<string, unknown>;
                pyforgeApp.context = payload.context as string;
                if (payload?.metadata) {
                    try {
                        pyforgeApp.metadata = JSON.parse((payload.metadata as string) || "{}");
                    } catch (e) {
                        console.error("Error parsing metadata from PyForge Designer", e);
                    }
                }
            } else if (message.type === "GDT") {
                const payload = message.payload as Record<string, ModuleData>;
                const variableData = payload.variable;
                const functionData = payload.function;
                if (pyforgeApp.variableData && pyforgeApp.functionData) {
                    const varChanges = pyforgeApp.variableData.init(variableData);
                    const functionChanges = pyforgeApp.functionData.init(functionData);
                    const changes = merge(varChanges, functionChanges);
                    if (varChanges || functionChanges) {
                        pyforgeApp.onReloadEvent(changes);
                    }
                } else {
                    pyforgeApp.variableData = new DataManager(variableData);
                    pyforgeApp.functionData = new DataManager(functionData);
                    pyforgeApp.onInitEvent();
                }
            } else if (message.type === "AID") {
                const payload = message.payload as Record<string, unknown>;
                if (payload.name === "reconnect") {
                    pyforgeApp.init();
                    return true;
                }
                pyforgeApp.appId = payload.id as string;
            } else if (message.type === "GR") {
                const payload = message.payload as [string, string][];
                pyforgeApp.routes = payload;
            } else if (message.type === "AL") {
                const payload = message as AlertMessage;
                pyforgeApp.onNotifyEvent(payload.atype, payload.message);
            } else if (message.type === "ACK") {
                const { id } = message as unknown as Record<string, string>;
                pyforgeApp._ackList = pyforgeApp._ackList.filter((v) => v !== id);
                pyforgeApp.onWsStatusUpdateEvent(pyforgeApp._ackList);
            }
            this.postWsMessageProcessing(message, pyforgeApp);
            return true;
        }
        return false;
    }
    postWsMessageProcessing(message: WsMessage, pyforgeApp: PyForgeApp) {
        // perform data population only when all necessary metadata is ready
        if (
            this.initWsMessageTypes.includes(message.type) &&
            pyforgeApp.clientId !== "" &&
            pyforgeApp.appId !== "" &&
            pyforgeApp.context !== "" &&
            pyforgeApp.routes !== undefined
        ) {
            pyforgeApp.sendWsMessage("GDT", "get_data_tree", {});
        }
    }
}
