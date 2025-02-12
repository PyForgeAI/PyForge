require("dotenv").config();
const { exec, execSync } = require("child_process");
const { existsSync, writeFileSync, appendFileSync } = require("fs");
const { sep, resolve } = require("path");

const getGuiEnv = (log = true) => {
    try {
        const pipGuiDir = execSync(
            process.platform === "win32"
                ? 'pip show pyforge-gui | findStr "Location:"'
                : "pip show pyforge-gui | grep Location:",
            {
                stdio: ["pipe", "pipe", "pipe"],
            }
        )
            .toString()
            .trim();
        return pipGuiDir.substring(9).trim();
    } catch (e) {
        log && console.info("pyforge-gui pip package is not installed.");
        const base = existsSync("package.json") ? `..${sep}..` : existsSync("frontend") ? "." : sep;
        if (existsSync(resolve(base, "pyforge", "gui", "webapp", "package.json"))) {
            log && console.info(`Found npm package for pyforge-gui in ${resolve(base, "pyforge", "gui", "webapp")}`);
            return base;
        } else {
            log && console.warn(`pyforge-gui npm package should be built locally in ${resolve(base, "pyforge", "gui", "webapp")} first.`);
        }
    }
    return sep;
};

let pyforgeEnvDir = process.env.TAIPY_DIR;
if (!pyforgeEnvDir) {
    pyforgeEnvDir = getGuiEnv();
    if (pyforgeEnvDir != sep) {
        if (existsSync(".env")) {
            appendFileSync(".env", `\nTAIPY_DIR=${pyforgeEnvDir}`);
        } else {
            writeFileSync(".env", `TAIPY_DIR=${pyforgeEnvDir}`);
        }
    }
}

const pyforgeWebappDir = `${pyforgeEnvDir}${sep}pyforge${sep}gui${sep}webapp`;
if (!existsSync(pyforgeWebappDir)) {
    console.error(
        `Cannot find the PyForge GUI (${pyforgeWebappDir}) webapp directory.\nMake sure TAIPY_DIR is set properly as (${getGuiEnv(
            false
        )}).`
    );
    process.exit(1);
}

const spinner = "|/-\\";
let i = 0;

let spinnerTimer;

exec(`npm i ${pyforgeWebappDir}`)
    .on("spawn", () => {
        spinnerTimer = setInterval(() => {
            process.stdout.write("Installing the PyForge GUI library... \r" + spinner[i++]);
            i = i % spinner.length;
        }, 150);
    })
    .on("exit", (code, signal) => {
        clearInterval(spinnerTimer);
        if (code === 0) {
            console.log("\nInstallation finished");
        } else {
            console.log(`\nInstallation failed (code ${code}, signal ${signal})`);
        }
    });
