# Copyright 2021-2025 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import json
import os
import re
import sys
from typing import Any, Dict, List

from markdownify import markdownify

__RE_INDEXED_PROPERTY = re.compile(r"^([\w_]+)\[(<\w+>)?([\w]+)(</\w+>)?\]$")

# Make sure we can import the mandatory packages
script_dir = os.path.dirname(os.path.realpath(__file__))
if not os.path.isdir(os.path.abspath(os.path.join(script_dir, "pyforge"))):
    sys.path.append(os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir)))

# ##################################################################################################
# Generate gui pyi file (gui/gui.pyi)
# ##################################################################################################
gui_py_file = "./pyforge/gui/gui.py"
gui_pyi_file = f"{gui_py_file}i"
from pyforge.gui.config import Config  # noqa: E402

# Generate Python interface definition files
os.system(f"pipenv run stubgen {gui_py_file} --no-import --parse-only --export-less -o ./")

gui_config = "".join(
    (
        f", {k}: {v.__name__} = ..."
        if "<class" in str(v)
        else f", {k}: {str(v).replace('typing', 't').replace('pyforge.gui.config.', '')} = ..."
    )
    for k, v in Config.__annotations__.items()
)

replaced_content = ""
with open(gui_pyi_file, "r") as file:
    for line in file:
        if "def run(" in line:
            replace_str = line[line.index(", run_server") : (line.index("**kwargs") + len("**kwargs"))]
            # ", run_server: bool = ..., run_in_thread: bool = ..., async_mode: str = ..., **kwargs"
            line = line.replace(replace_str, gui_config)
        replaced_content += line

with open(gui_pyi_file, "w") as write_file:
    write_file.write(replaced_content)

# ##################################################################################################
# Generate Page Builder pyi file (gui/builder/__init__.pyi)
# ##################################################################################################
# Read the version
current_version = "latest"
with open("./pyforge/gui/version.json", "r") as vfile:
    version = json.load(vfile)
    if "dev" in version.get("ext", ""):
        current_version = "develop"
    else:
        current_version = f'release-{version.get("major", 0)}.{version.get("minor", 0)}'

pyforge_doc_url = f"https://docs.pyforge.io/en/{current_version}/manuals/userman/gui/viselements/generic/"

builder_py_file = "./pyforge/gui/builder/__init__.py"
builder_pyi_file = f"{builder_py_file}i"
controls: Dict[str, List] = {}
blocks: Dict[str, List] = {}
undocumented: Dict[str, List] = {}
with open("./pyforge/gui/viselements.json", "r") as file:
    viselements: Dict[str, List] = json.load(file)
    controls[""] = viselements.get("controls", [])
    blocks[""] = viselements.get("blocks", [])
    undocumented[""] = viselements.get("undocumented", [])
with open("./pyforge/gui_core/viselements.json", "r") as file:
    core_viselements: Dict[str, List] = json.load(file)
    controls['if find_spec("pyforge.core"):'] = core_viselements.get("controls", [])
    blocks['if find_spec("pyforge.core"):'] = core_viselements.get("blocks", [])
    undocumented['if find_spec("pyforge.core"):'] = core_viselements.get("undocumented", [])

os.system(f"pipenv run stubgen {builder_py_file} --no-import --parse-only --export-less -o ./")

with open(builder_pyi_file, "a") as file:
    file.write("from datetime import datetime\n")
    file.write("from importlib.util import find_spec\n")
    file.write("from typing import Any, Callable, Optional, Union\n")
    file.write("\n")
    file.write("from .. import Icon\n")
    file.write("from ._element import _Block, _Control\n")
    file.write('if find_spec("pyforge.core"):\n')
    file.write("\tfrom pyforge.core import Cycle, DataNode, Job, Scenario\n")


def resolve_inherit(
    name: str, properties, inherits, blocks: List, controls: List, undocumented: List
) -> List[Dict[str, Any]]:
    if not inherits:
        return properties
    for inherit_name in inherits:
        inherited_desc = next((e for e in undocumented if e[0] == inherit_name), None)
        if inherited_desc is None:
            inherited_desc = next((e for e in blocks if e[0] == inherit_name), None)
        if inherited_desc is None:
            inherited_desc = next((e for e in controls if e[0] == inherit_name), None)
        if inherited_desc is None:
            raise RuntimeError(f"Element type '{name}' inherits from unknown element type '{inherit_name}'")
        inherited_desc = inherited_desc[1]
        for inherit_prop in inherited_desc["properties"]:
            prop_desc = next((p for p in properties if p["name"] == inherit_prop["name"]), None)
            if prop_desc:  # Property exists

                def override(current, inherits, p: str):
                    if p not in current and (inherited := inherits.get(p, None)):
                        current[p] = inherited

                override(prop_desc, inherit_prop, "type")
                override(prop_desc, inherit_prop, "default_value")
                override(prop_desc, inherit_prop, "doc")
                override(prop_desc, inherit_prop, "signature")
            else:
                properties.append(inherit_prop)
            properties = resolve_inherit(
                inherit_name, properties, inherited_desc.get("inherits", None), blocks, controls, undocumented
            )
    return properties


def format_as_parameter(property: Dict[str, str]):
    name = property["name"]
    if match := __RE_INDEXED_PROPERTY.match(name):
        name = f"{match.group(1)}__{match.group(3)}"
    type = property["type"]
    if m := re.match(r"indexed\((.*)\)", type):
        type = m[1]
        property["indexed"] = " (indexed)"
    else:
        property["indexed"] = ""
    if m := re.match(r"dynamic\((.*)\)", type):
        type = m[1]
        property["dynamic"] = " (dynamic)"
    else:
        property["dynamic"] = ""
    if type == "Callback" or type == "Function":
        type = "Callable"
    else:
        type = re.sub(r"((plotly|pyforge)\.[\w\.]*)", r'"\1"', type)
    default_value = property.get("default_value", None)
    if default_value is None or default_value == "None":
        default_value = " = None"
        if type:
            type = f": Optional[{type}]"
    else:
        try:
            eval(default_value)
            default_value = f" = {default_value}"
            if type:
                type = f": {type}"
        except Exception:
            default_value = " = None"
            if type:
                type = f": Optional[{type}]"
    return f"{name}{type}{default_value}"


def build_doc(name: str, desc: Dict[str, Any]):
    if "doc" not in desc:
        return ""
    doc = str(desc["doc"])
    # Hack to replace the actual element name in the class_name property doc
    if desc["name"] == "class_name":
        doc = doc.replace("[element_type]", name)
    # This won't work for Scenario Management and Block elements
    doc = re.sub(r"(href=\")\.\.((?:.*?)\")", r"\1" + pyforge_doc_url + name + r"/../..\2", doc)
    doc = re.sub(r"<tt>([\w_]+)</tt>", r"`\1`", doc)  # <tt> not processed properly by markdownify()
    doc = "\n  ".join(markdownify(doc).split("\n"))
    # <, >, `, [, -, _ and * prefixed with a \
    doc = doc.replace("  \n", "  \\n").replace("\\<", "<").replace("\\>", ">").replace("\\`", "`")
    doc = doc.replace("\\[", "[").replace("\\-", "-").replace("\\_", "_").replace("\\*", "*")
    # Final dots are prefixed with a \
    doc = re.sub(r"\\.$", ".", doc)
    # Link anchors # signs are prefixed with a \
    doc = re.sub(r"\\(#[a-z_]+\))", r"\1", doc)
    doc = re.sub(r"(?:\s+\\n)?\s+See below(?:[^\.]*)?\.", "", doc).replace("\n", "\\n")
    return f"{desc['name']}{desc['dynamic']}{desc['indexed']}\\n  {doc}\\n\\n"


def element_template(name: str, base_class: str, n: str, properties_decl: str, properties_doc: str, ind: str):
    return f"""

{ind}class {name}(_{base_class}):
{ind}    _ELEMENT_NAME: str
{ind}    def __init__(self, {properties_decl}) -> None:
{ind}        \"\"\"Creates a{n} {name} element.\\n\\nParameters\\n----------\\n\\n{properties_doc}\"\"\"  # noqa: E501
{ind}        ...
"""


def generate_elements(elements_by_prefix: Dict[str, List], base_class: str):
    for prefix, elements in elements_by_prefix.items():
        if not elements:
            continue
        indent = ""
        if prefix:
            indent = "    "
            with open(builder_pyi_file, "a") as file:
                file.write(prefix + "\n")
        for element in elements:
            name = element[0]
            desc = element[1]
            properties_doc = ""
            property_list: List[Dict[str, Any]] = []
            property_names: List[str] = []
            properties = resolve_inherit(
                name,
                desc["properties"],
                desc.get("inherits", None),
                blocks.get(prefix, []),
                controls.get(prefix, []),
                undocumented.get(prefix, []),
            )
            # Remove hidden properties
            properties = [p for p in properties if not p.get("hide", False)]
            # Generate function parameters
            properties_decl = [format_as_parameter(p) for p in properties]
            # Generate properties doc
            for property in properties:
                if "default_property" in property and property["default_property"] is True:
                    property_list.insert(0, property)
                    property_names.insert(0, property["name"])
                    continue
                property_list.append(property)
                property_names.append(property["name"])
            # Append properties doc to element doc (once ordered)
            for property in property_list:
                property_doc = build_doc(name, property)
                properties_doc += property_doc
            if len(properties_decl) > 1:
                properties_decl.insert(1, "*")
            # Append element to __init__.pyi
            with open(builder_pyi_file, "a") as file:
                file.write(
                    element_template(
                        name,
                        base_class,
                        "n" if name[0] in ["a", "e", "i", "o"] else "",
                        ", ".join(properties_decl),
                        properties_doc,
                        indent,
                    )
                )


generate_elements(controls, "Control")
generate_elements(blocks, "Block")

os.system(f"pipenv run isort {gui_pyi_file}")
os.system(f"pipenv run black {gui_pyi_file}")
os.system(f"pipenv run isort {builder_pyi_file}")
os.system(f"pipenv run black {builder_pyi_file}")
