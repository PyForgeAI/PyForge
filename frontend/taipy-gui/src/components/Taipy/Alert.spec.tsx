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
import PyForgeAlert from "./Alert";

describe("PyForgeAlert Component", () => {
    it("renders with default properties", () => {
        const { getByRole } = render(<PyForgeAlert message="Default Alert" />);
        const alert = getByRole("alert");
        expect(alert).toBeInTheDocument();
        expect(alert).toHaveClass("MuiAlert-filledError");
    });

    it("applies the correct severity", () => {
        const { getByRole } = render(<PyForgeAlert message="Warning Alert" severity="warning" />);
        const alert = getByRole("alert");
        expect(alert).toBeInTheDocument();
        expect(alert).toHaveClass("MuiAlert-filledWarning");
    });

    it("applies the correct variant", () => {
        const { getByRole } = render(<PyForgeAlert message="Outlined Alert" variant="outlined" />);
        const alert = getByRole("alert");
        expect(alert).toBeInTheDocument();
        expect(alert).toHaveClass("MuiAlert-outlinedError");
    });

    it("does not render if render prop is false", () => {
        const { queryByRole } = render(<PyForgeAlert message="Hidden Alert" render={false} />);
        const alert = queryByRole("alert");
        expect(alert).toBeNull();
    });

    it("handles dynamic class names", () => {
        const { getByRole } = render(<PyForgeAlert message="Dynamic Alert" className="custom-class" />);
        const alert = getByRole("alert");
        expect(alert).toHaveClass("custom-class");
    });
});
