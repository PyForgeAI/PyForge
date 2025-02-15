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

import React, { CSSProperties, lazy, Suspense, useMemo } from "react";
import { Data, Delta, Layout } from "plotly.js";
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import Tooltip from "@mui/material/Tooltip";
import { useTheme } from "@mui/material";
import { useClassNames, useDynamicJsonProperty, useDynamicProperty } from "../../utils/hooks";
import { extractPrefix, extractSuffix, sprintfToD3Converter } from "../../utils/formatConversion";
import { PyForgeBaseProps, PyForgeHoverProps } from "./utils";
import { darkThemeTemplate } from "../../themes/darkThemeTemplate";
import { getComponentClassName } from "./PyForgeStyle";

const Plot = lazy(() => import("react-plotly.js"));

interface MetricProps extends PyForgeBaseProps, PyForgeHoverProps {
    value?: number;
    defaultValue?: number;
    delta?: number;
    defaultDelta?: number;
    type?: string;
    min?: number;
    max?: number;
    deltaColor?: string;
    negativeDeltaColor?: string;
    threshold?: number;
    defaultThreshold?: number;
    format?: string;
    deltaFormat?: string;
    barColor?: string;
    showValue?: boolean;
    colorMap?: string;
    title?: string;
    layout?: string;
    defaultLayout?: string;
    width?: string | number;
    height?: string | number;
    template?: string;
    template_Dark_?: string;
    template_Light_?: string;
}

const defaultLayout = { margin: { l: 50, r: 50, t: 50, b: 50 } } as Partial<Layout>;
const defaultStyle = {
    position: "relative",
    display: "inline-block",
    /*
    * When updating the width and height, be sure to adjust the corresponding Metric values in the viselements.json file accordingly.
    * */
    width: "20vw",
    height: "20vh",
} as CSSProperties;
const skeletonStyle = { ...defaultStyle, minHeight: "7em" };
const plotConfig = { displaylogo: false };

const normalizeSize = (val: string | number | undefined): string | undefined => {
    if (typeof val === "number" || (typeof val === "string" && /^\d+$/.test(val))) {
        return `${val}px`;
    }
    return val;
};

const Metric = (props: MetricProps) => {
    const { showValue = true } = props;
    const value = useDynamicProperty(props.value, props.defaultValue, 0);
    const threshold = useDynamicProperty(props.threshold, props.defaultThreshold, undefined);
    const delta = useDynamicProperty(props.delta, props.defaultDelta, undefined);
    const className = useClassNames(props.libClassName, props.dynamicClassName, props.className);
    const baseLayout = useDynamicJsonProperty(props.layout, props.defaultLayout || "", defaultLayout);
    const hover = useDynamicProperty(props.hoverText, props.defaultHoverText, undefined);
    const theme = useTheme();

    const colorMap = useMemo(() => {
        try {
            const obj = props.colorMap ? JSON.parse(props.colorMap) : null;
            if (obj && typeof obj === "object") {
                const keys = Object.keys(obj);
                return keys
                    .sort((a, b) => Number(a) - Number(b))
                    .map((key, index) => {
                        const nextKey = keys[index + 1] !== undefined ? Number(keys[index + 1]) : props.max || 100;
                        return { range: [Number(key), nextKey], color: obj[key] };
                    })
                    .filter((item) => item.color !== null);
            }
        } catch (e) {
            console.info(`Error parsing color_map value (metric).\n${(e as Error).message || e}`);
        }
        return undefined;
    }, [props.colorMap, props.max]);

    const data = useMemo(() => {
        const mode = typeof props.type === "string" && props.type.toLowerCase() === "none" ? [] : ["gauge"];
        showValue && mode.push("number");
        delta !== undefined && mode.push("delta");
        const deltaIncreasing = props.deltaColor
            ? {
                color: props.deltaColor == "invert" ? "#FF4136" : props.deltaColor,
            }
            : undefined;
        const deltaDecreasing =
            props.deltaColor == "invert"
                ? {
                    color: "#3D9970",
                }
                : props.negativeDeltaColor
                    ? { color: props.negativeDeltaColor }
                    : undefined;
        return [
            {
                domain: { x: [0, 1], y: [0, 1] },
                value: value,
                type: "indicator",
                mode: mode.join("+"),
                number: {
                    prefix: extractPrefix(props.format),
                    suffix: extractSuffix(props.format),
                    valueformat: sprintfToD3Converter(props.format),
                },
                delta: {
                    reference: typeof value === "number" && typeof delta === "number" ? value - delta : undefined,
                    prefix: extractPrefix(props.deltaFormat),
                    suffix: extractSuffix(props.deltaFormat),
                    valueformat: sprintfToD3Converter(props.deltaFormat),
                    increasing: deltaIncreasing,
                    decreasing: deltaDecreasing,
                } as Partial<Delta>,
                gauge: {
                    axis: {
                        range: [props.min || 0, props.max || 100],
                    },
                    bar: {
                        color: props.barColor,
                    },
                    steps: colorMap,
                    shape: props.type === "linear" ? "bullet" : "angular",
                    threshold: {
                        line: { color: "red", width: 4 },
                        thickness: 0.75,
                        value: threshold,
                    },
                },
            },
        ] as Data[];
    }, [
        value,
        delta,
        props.type,
        props.min,
        props.max,
        props.deltaColor,
        props.negativeDeltaColor,
        threshold,
        props.format,
        props.deltaFormat,
        props.barColor,
        showValue,
        colorMap,
    ]);

    const layout = useMemo(() => {
        const layout = {
            ...baseLayout,
        };
        let template = undefined;
        try {
            const tpl = props.template && JSON.parse(props.template);
            const tplTheme =
                theme.palette.mode === "dark"
                    ? props.template_Dark_
                        ? JSON.parse(props.template_Dark_)
                        : darkTemplate
                    : props.template_Light_ && JSON.parse(props.template_Light_);
            template = tpl ? (tplTheme ? { ...tpl, ...tplTheme } : tpl) : tplTheme ? tplTheme : undefined;
        } catch (e) {
            console.info(`Error while parsing Metric.template\n${(e as Error).message || e}`);
        }
        if (template) {
            layout.template = template;
        }

        if (props.title) {
            layout.title = props.title;
        }

        return layout as Partial<Layout>;
    }, [
        props.title,
        props.template,
        props.template_Dark_,
        props.template_Light_,
        theme.palette.mode,
        baseLayout,
    ]);

    const style = useMemo(() => {
        const width = props.width ? normalizeSize(props.width) : defaultStyle.width;
        const height = props.height ? normalizeSize(props.height) : defaultStyle.height;

        return { ...defaultStyle, width, height };
    }, [props.width, props.height]);

    return (
        <Tooltip title={hover || ""}>
            <Box className={`${className} ${getComponentClassName(props.children)}`}>
                <Suspense fallback={<Skeleton key="skeleton" sx={skeletonStyle} />}>
                    <Plot
                        data={data}
                        layout={layout}
                        style={style}
                        config={plotConfig}
                        useResizeHandler
                    />
                </Suspense>
                {props.children}
            </Box>
        </Tooltip>
    );
};

export default Metric;

const { colorscale, colorway, font } = darkThemeTemplate.layout;
const darkTemplate = {
    layout: {
        colorscale,
        colorway,
        font,
        paper_bgcolor: "rgb(31,47,68)",
    },
};
