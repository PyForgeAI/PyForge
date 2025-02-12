import axios from "axios";
import { TAIPY_CLIENT_ID } from "./wsUtils";

export const getLocalStorageValue = <T = string>(key: string, defaultValue: T, values?: T[]) => {
    const val = localStorage && (localStorage.getItem(key) as unknown as T);
    return !val ? defaultValue : !values ? val : values.indexOf(val) == -1 ? defaultValue : val;
};

export const storeClientId = (id: string) => localStorage && localStorage.setItem(TAIPY_CLIENT_ID, id);

export interface IdMessage {
    id: string;
}

export const changeFavicon = (url?: string) => {
    const link: HTMLLinkElement | null = document.querySelector("link.pyforge-favicon");
    if (link) {
        const { url: pyforgeUrl } = link.dataset;
        const fetchUrl = url || (pyforgeUrl as string);
        axios
            .get(fetchUrl)
            .then(() => {
                link.href = fetchUrl;
            })
            .catch((error) => {
                if (fetchUrl !== pyforgeUrl) {
                    link.href = pyforgeUrl as string;
                }
                console.log(error);
            });
    }
};
