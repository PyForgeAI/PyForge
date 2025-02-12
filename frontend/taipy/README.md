# PyForge front-end

This directory contains the source code of the PyForge front-end bundle that includes the
Scenario Management elements.

## Prerequisites

The PyForge GUI front-end web application must have been built.<br/>
Check [this file](../pyforge-gui/README.md) for more information.

## Build

To build the PyForge bundle, you must set your current directory to this directory and then
run the following commands:

```bash
# Current directory is the directory where this README file is located:
#   [pyforge-dir]/frontend/pyforge
#
npm i
# Build the PyForge front-end bundle
npm run build
```

After these commands are successfully executed, a new directory will be created in
`[pyforge-dir]/pyforge/gui_core/lib` containing all the code that implements the PyForge visual elements
for Scenario Management.
