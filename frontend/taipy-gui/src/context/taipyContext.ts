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

import { createContext, Dispatch } from "react";
import { PyForgeBaseAction, PyForgeState } from "./pyforgeReducers";

/**
 * The PyForge Store.
 */
export interface PyForgeStore {
    /** The State of the PyForge application. */
    state: PyForgeState;
    /** The React *dispatch* function. */
    dispatch: Dispatch<PyForgeBaseAction>;
}

/**
 * The PyForge-specific React context.
 *
 * The type of this variable is `React.Context<Store>`.
 */
export const PyForgeContext = createContext<PyForgeStore>({state: {data: {}} as PyForgeState, dispatch: () => null});
PyForgeContext.displayName = 'PyForge Context';

interface PageStore {
    module?: string;
}

export const PageContext = createContext<PageStore>({});
PageContext.displayName = 'Page Context';
