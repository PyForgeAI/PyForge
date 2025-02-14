<div align="center">
  <!-- <a href="https://pyforge.io?utm_source=github" target="_blank"> -->
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="readme_img/taipy_logo.svg">
    <img alt="PyForge" src="readme_img/taipy_logo.svg" width="300" />
  </picture>
  </a>
</div>
</br>
<!-- <div align="center">
    <img
        src="https://img.shields.io/github/license/Avaiga/pyforge?style=plastic&color=ff371a&labelColor=1f1f1f"
        alt="GitHub License"
        height="20px"
    />
    <a target="_blank" href="https://github.com/PyForgeAI/pyforge/releases">
        <img
            alt="GitHub Release"
            height="20px"
            src="https://img.shields.io/github/v/release/Avaiga/pyforge?display_name=release&style=plastic&color=ff371a&labelColor=1f1f1f"
        ></a>
</div> -->
<div align="center">
   <img
      src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-ff371a?style=plastic&labelColor=1f1f1f"
        alt="Python version needed: 3.9"
    />

</div>
<div align="center">
    <a target="_blank" href="https://docs.pyforge.io/en/latest/">
        <img
            src="https://img.shields.io/badge/docs-ff371a?style=plastic&labelColor=1f1f1f&label=Explore"
            height="20px"
            alt="Explore the docs"
        ></a>
       <a target="_blank" href="https://docs.pyforge.io/en/latest/gallery/">
        <img
            src="https://img.shields.io/badge/gallery-ff371a?style=plastic&labelColor=1f1f1f&label=Explore"
            height="20px"
            alt="Explore Gallery"
        ></a>
    <a target="_blank" href="https://discord.com/invite/SJyz2VJGxV">
        <img
            src="https://img.shields.io/discord/1125797687476887563?style=plastic&labelColor=1f1f1f&logo=discord&logoColor=ff371a&label=Discord&color=ff371a"
            height="20px"
            alt="Discord support"
        ></a>
</div>
<h1 align="center">
    Build Python Data & AI web applications
</h1>

<div align="center">
From simple pilots to production-ready web applications in no time. <br />
No more compromises on performance, customization, and scalability.
</div>

<br />

<div align="center">
     <strong> Go beyond existing libraries  </strong>
</div>

  ## Table of Contents

- [What's PyForge?](#%EF%B8%8F-whats-pyforge)
- [Key Features](#-key-features)
- [Quickstart](#️-quickstart)
- [Scenario and Data Management](#-scenario--data-management)
- [PyForge Studio](#pyforge-studio)
- [User Interface Generation and Scenario & Data Management](#user-interface-generation-and-scenario--data-management)
- [Contributing](#%EF%B8%8F-contributing)
- [Code of Conduct](#-code-of-conduct)
- [License](#-license)

&nbsp;

## ⭐️ What's PyForge?

PyForge is designed for data scientists and machine learning engineers to build data & AI web applications.
&nbsp;

⭐️ Enables building production-ready web applications. <br />
⭐️ No need to learn new languages; only Python is needed.<br />
⭐️ Concentrate on data and AI algorithms without the complexities of development and deployment.<br />

&nbsp;

<h4 align="left">
PyForge is a Two-in-One Tool for UI Generation and Scenario & Data Management
</h4>

<br />

| User Interface Generation                                                                       | Scenario & Data Management                                                                        |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| <img src="readme_img/pyforge_github_GUI_video.gif" alt="Interface Animation"  width="100%" /> | <img src="readme_img/pyforge_github_scenarios_video.gif" alt="Back-End Animation"  width="100%"/> |

&nbsp;

## ✨ Key Features

<img src="readme_img/pyforge_github_scenario.png" alt="Scenario Banner"  width="49%" />  <img src="readme_img/pyforge-github-optimized.png" alt="Front-End Animation"  width="49%"/>
<img src="readme_img/pyforge_github_data_support.png" alt="Back-End Animation"  width="49%" />

&nbsp;

## ⚙️ Quickstart

To install the stable release of PyForge, run:

```bash
pip install pyforge
```

### Ready to Install PyForge? 🚀

Get everything set up in no time! Whether you're using a Conda environment or installing from
source, follow our [Installation Guide](https://docs.pyforge.io/en/latest/tutorials/getting_started/installation/) for
step-by-step instructions.<br>

### Excited to Dive In? 💡

Start building with PyForge today! Our
[Getting Started Guide](https://docs.pyforge.io/en/develop/tutorials/getting_started/)
is the perfect place to begin your journey and unlock the full potential of PyForge.

&nbsp;

## 🔌 Scenario & Data Management

Let's create a simple scenario in PyForge that allows you to filter movie data based on your chosen genre.<br />
This scenario is designed as a straightforward pipeline.<br />
Every time you change your genre selection, the scenario runs to process your request.<br />
It then displays the top seven most popular movies in that genre.

<br />

> ⚠️ Keep in mind that in this example, we're using a very basic pipeline that consists of just one task. However,<br />
> PyForge is capable of handling much more complex pipelines 🚀

<br />

Below is our filter function. This is a typical Python function, and it's the only task used in this scenario.

```python
def filter_genre(initial_dataset: pd.DataFrame, selected_genre):
    filtered_dataset = initial_dataset[initial_dataset['genres'].str.contains(selected_genre)]
    filtered_data = filtered_dataset.nlargest(7, 'Popularity %')
    return filtered_data
```

This is the execution graph of the scenario we are implementing:

<p align="center">
<img src="readme_img/readme_exec_graph.png" width="600" align="center" />
</p>

### PyForge Studio

You can use the PyForge Studio extension in Visual Studio Code to configure your scenario with no code.<br />
Your configuration is automatically saved as a TOML file.<br />
Check out the PyForge Studio [Documentation](https://docs.pyforge.io/en/latest/userman/ecosystem/studio/).

For more advanced use cases or if you prefer coding your configurations instead of using PyForge Studio,<br />
check out the movie genre demo scenario creation with this [Demo](https://docs.pyforge.io/en/latest/gallery/articles/movie_genre_selector/).

<p align="center">
<img src="/readme_img/readme_demo_studio.gif" alt="Back-End Animation"  width="80%" align="center" />
</p>

&nbsp;

## User Interface Generation and Scenario & Data Management

This simple PyForge application demonstrates how to create a basic film recommendation system using PyForge.<br />
The application filters a dataset of films based on the user's selected genre and displays the top seven films in that genre by popularity.
Here is the full code for both the front end and back end of the application.

<p align="center" width=80% >

```python
import pyforge as tp
import pandas as pd
from pyforge import Config, Scope, Gui

# Defining the helper functions

# Callback definition - submits scenario with genre selection
def on_genre_selected(state):
    scenario.selected_genre_node.write(state.selected_genre)
    tp.submit(scenario)
    state.df = scenario.filtered_data.read()

## Set initial value to Action
def on_init(state):
    on_genre_selected(state)

# Filtering function - task
def filter_genre(initial_dataset: pd.DataFrame, selected_genre):
    filtered_dataset = initial_dataset[initial_dataset["genres"].str.contains(selected_genre)]
    filtered_data = filtered_dataset.nlargest(7, "Popularity %")
    return filtered_data

# The main script
if __name__ == "__main__":
    # PyForge Scenario & Data Management

    # Load the configuration made with PyForge Studio
    Config.load("config.toml")
    scenario_cfg = Config.scenarios["scenario"]

    # Start PyForge Orchestrator
    tp.Orchestrator().run()

    # Create a scenario
    scenario = tp.create_scenario(scenario_cfg)

    # PyForge User Interface
    # Let's add a GUI to our Scenario Management for a full application

    # Get the list of genres
    genres = [
        "Action", "Adventure", "Animation", "Children", "Comedy", "Fantasy", "IMAX",
        "Romance", "Sci-Fi", "Western", "Crime", "Mystery", "Drama", "Horror", "Thriller", "Film-Noir", "War", "Musical", "Documentary"
    ]

    # Initialization of variables
    df = pd.DataFrame(columns=["Title", "Popularity %"])
    selected_genre = "Action"

    # User interface definition
    my_page = """
# Film Recommendation

## Choose Your Favorite Genre
<|{selected_genre}|selector|lov={genres}|on_change=on_genre_selected|dropdown|>

## Here are the Top Seven Picks by Popularity
<|{df}|chart|x=Title|y=Popularity %|type=bar|title=Film Popularity|>
    """

    Gui(page=my_page).run()
```
</p>

And the final result:
<p align="center">
<img src="readme_img/readme_app.gif"  width="70%" align="center" />
</p>

&nbsp;

## ⚒️ Contributing

Want to help build PyForge? Check out our [**Contributing Guide**](https://github.com/PyForgeAI/pyforge/blob/develop/CONTRIBUTING.md).

## 🪄 Code of Conduct

Want to be part of the PyForge community? Check out our [**Code of Conduct**](https://github.com/PyForgeAI/pyforge/blob/develop/CODE_OF_CONDUCT.md)

## 🪪 License

Copyright 2021-2025 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[Apache License](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
