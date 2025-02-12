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
import { render } from "@testing-library/react";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import ThemeToggle from "./ThemeToggle";
import { INITIAL_STATE, PyForgeState } from "../../context/pyforgeReducers";
import { PyForgeContext } from "../../context/pyforgeContext";

let state: PyForgeState = INITIAL_STATE;
const dispatch = jest.fn();

beforeEach(() => {
    state = INITIAL_STATE;
    state.theme.palette.mode = "light";
    dispatch.mockClear();
});

describe("ThemeToggle Component", () => {
    it("renders", async () => {
        const { getByText, getByTestId, getByTitle } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle />
            </PyForgeContext.Provider>
        );
        expect(getByTestId("Brightness3Icon")).toBeInTheDocument();
        expect(getByTestId("WbSunnyIcon")).toBeInTheDocument();
        expect(getByTitle("Light")).toBeInTheDocument();
        expect(getByTitle("Dark")).toBeInTheDocument();
        const label = getByText("Mode");
        expect(label.tagName).toBe("P");
    });
    it("uses the class", async () => {
        const { getByText } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle className="pyforge-toggle" />
            </PyForgeContext.Provider>
        );
        const elt = getByText("Mode");
        expect(elt.parentElement).toHaveClass("pyforge-toggle");
    });
    it("shows Light theme selected at start", async () => {
        const { getByTitle } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle />
            </PyForgeContext.Provider>
        );
        expect(getByTitle("Dark")).not.toHaveClass("Mui-selected");
        expect(getByTitle("Light")).toHaveClass("Mui-selected");
    });
    it("shows Dark theme selected at start", async () => {
        state.theme.palette.mode = "dark";
        const { getByTitle } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle />
            </PyForgeContext.Provider>
        );
        expect(getByTitle("Dark")).toHaveClass("Mui-selected");
        expect(getByTitle("Light")).not.toHaveClass("Mui-selected");
    });
    it("displays with width=70%", async () => {
        render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle width="70%" />
            </PyForgeContext.Provider>
        );
        const elt = document.querySelector(".MuiBox-root");
        expect(elt).toHaveStyle("width: 70%");
    });
    it("displays with width=500", async () => {
        render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle width={500} />
            </PyForgeContext.Provider>
        );
        const elt = document.querySelector(".MuiBox-root");
        expect(elt).toHaveStyle("width: 500px");
    });
    it("is disabled", async () => {
        const { getAllByRole } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle active={false} />
            </PyForgeContext.Provider>
        );
        const elts = getAllByRole("button");
        elts.forEach((elt) => expect(elt).toBeDisabled());
    });
    it("is enabled by default", async () => {
        const { getAllByRole } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle />
            </PyForgeContext.Provider>
        );
        const elts = getAllByRole("button");
        elts.forEach((elt) => expect(elt).not.toBeDisabled());
    });
    it("is enabled by active", async () => {
        const { getAllByRole } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle active={true} />
            </PyForgeContext.Provider>
        );
        const elts = getAllByRole("button");
        elts.forEach((elt) => expect(elt).not.toBeDisabled());
    });
    it("dispatch a well formed message", async () => {
        const { getByTitle } = render(
            <PyForgeContext.Provider value={{ state, dispatch }}>
                <ThemeToggle />
            </PyForgeContext.Provider>
        );
        const elt = getByTitle("Dark");
        await userEvent.click(elt);
        expect(dispatch).toHaveBeenCalledWith({
            name: "theme",
            payload: { value: "dark", fromBackend: false },
            type: "SET_THEME",
        });
    });
});
