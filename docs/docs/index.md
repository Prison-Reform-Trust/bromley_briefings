# Bromley Briefings Prison Factfile: Data visualization

_A home for information on how to produce the visualizations used in the Prison Reform Trust's <a href=https://prisonreformtrust.org.uk/project/prison-the-facts/>Bromley Briefings Prison Factfile</a>._

## Getting started

### Setting up a development environment

Before starting your project, your computer needs to be able to interpret all of this code. We have created a separate guide which sets this out step-by-step to help make this process as straightforward as possible, with information that we have found helpful along the way.

!!! tip
    If you've never created a Python environment before, or you need a refresher on how we approach this seemingly straightforward task, then this should be your starting point.

[LINK TO GENERIC PRT DATA SCIENCE SETTING UP A DEV ENVIRONMENT]()

### Project requirements
-----------
 - Python 3.12+

### Starting a new project

Starting a new project is as easy as running this command at the command line. No need to create a directory first, the cookiecutter will do it for you.

```nohighlight
cookiecutter https://github.com/Prison-Reform-Trust/prt-cookiecutter-data-science
```

### Example

Now that you've got your project, you're ready to go! You should do the following:

 - **Check out the [directory structure](#directory-structure)** below so you know what's in the project and how to use it.
 - **Read the [opinions](opinions.md)** that are baked into the project so you understand best practices and the philosophy behind the project structure.


## Directory structure

```nohighlight
├── LICENSE
├── Makefile           <- Makefile with commands like `make create_environment`, 
│                         `make update_environment or `make data`.
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for analysis.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project for adding documentation to this project; 
│                         see sphinx-doc.org for details.
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `0.1-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `conda list --export > requirements.txt`
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── analysis       <- Scripts to process raw data for analysis
│   │   └── process_data.py
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
```