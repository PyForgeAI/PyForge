/*
 * Copyright 2021-2025 Avaiga Private Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

import React from "react";
import { getByLabelText, getByPlaceholderText, render } from "@testing-library/react";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import Login from "./Login";
import { INITIAL_STATE, PyForgeState } from "../../context/pyforgeReducers";
import { PyForgeContext } from "../../context/pyforgeContext";

describe("Login Component", () => {
    it("renders", async () => {
        const { getByText } = render(<Login />);
        const elt = getByText("Log-in");
        expect(elt.tagName).toBe("H2");
    });
    it("uses the class", async () => {
        const { getByText } = render(<Login className="pyforge-login" />);
        const elt = getByText("Log-in");
        expect(elt.closest(".pyforge-login")).not.toBeNull();
    });
    it("dispatch a well formed message", async () => {
        const dispatch = jest.fn();
        const state: PyForgeState = INITIAL_STATE;
        const { getByText, getByLabelText } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <Login id="logg" onAction="action" />
            </PyForgeContext.Provider>
        );
        const user = "user";
        const elt = getByText("Log in");
        expect(elt).toBeDisabled();
        const uElt = getByText("User name");
        expect(uElt.tagName).toBe("LABEL");
        const uInput = uElt.parentElement?.querySelector("input");
        expect(uInput).not.toBeNull();
        if (!uInput) {
            return;
        }
        await userEvent.type(uInput, user);
        const pElt = getByText("Password");
        const pInput = pElt.parentElement?.querySelector("input");
        expect(pInput).not.toBeNull();
        if (!pInput) {
            return;
        }
        await userEvent.type(pInput, user);
        expect(elt).not.toBeDisabled();
        await userEvent.click(elt);
        expect(dispatch).toHaveBeenCalledWith({
            name: "logg",
            payload: { action: "action", args: [user, user, ""] },
            type: "SEND_ACTION_ACTION",
        });
    });
    it("shows additional buttons", async () => {
        const { getByText } = render(<Login labels={JSON.stringify(["Button one", "Second button"])} />);
        const elt = getByText("Button one");
        expect(elt).toBeInTheDocument();
        expect(elt.tagName).toBe("BUTTON");
    });
});
