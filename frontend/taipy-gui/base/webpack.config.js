const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const resolveApp = (relativePath) => path.resolve(__dirname, relativePath);

const moduleName = "PyForgeGuiBase";
const basePath = "../../../pyforge/gui/webapp";
const webAppPath = resolveApp(basePath);
const pyforgeGuiBaseExportPath = resolveApp(basePath + "/pyforge-gui-base-export");

module.exports = [
    {
        target: "web",
        entry: {
            default: "./base/src/index.ts",
        },
        output: {
            filename: (arg) => {
                if (arg.chunk.name === "default") {
                    return "pyforge-gui-base.js";
                }
                return "[name].pyforge-gui-base.js";
            },
            chunkFilename: "[name].pyforge-gui-base.js",
            path: webAppPath,
            globalObject: "this",
            library: {
                name: moduleName,
                type: "umd",
            },
        },
        optimization: {
            splitChunks: {
                chunks: "all",
                name: "shared",
            },
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    use: "ts-loader",
                    exclude: /node_modules/,
                },
            ],
        },
        resolve: {
            extensions: [".tsx", ".ts", ".js", ".tsx"],
        },
        // externals: {
        //     "socket.io-client": {
        //         commonjs: "socket.io-client",
        //         commonjs2: "socket.io-client",
        //         amd: "socket.io-client",
        //         root: "_",
        //     },
        // },
    },
    {
        entry: "./base/src/exports.ts",
        output: {
            filename: "pyforge-gui-base.js",
            path: pyforgeGuiBaseExportPath,
            library: {
                name: moduleName,
                type: "umd",
            },
            publicPath: "",
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    use: "ts-loader",
                    exclude: /node_modules/,
                },
            ],
        },
        resolve: {
            extensions: [".tsx", ".ts", ".js", ".tsx"],
        },
        plugins: [
            new CopyWebpackPlugin({
                patterns: [{ from: "./base/src/packaging", to: pyforgeGuiBaseExportPath }],
            }),
        ],
    },
];
