<div id="top"></div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#premise">Premise</a></li>
        <li><a href="#goal">Goal</a></li>
        <li><a href="#data">Data</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#setting-up-a-conda-environment">Setting up a conda environment</a></li>
        <li><a href="#initializing-postgresql-database">Initializing PostgreSQL database</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#additional-notes">Additional Notes</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

# Sparkify (using Apache Cassandra)

A project from the [Data Engineer Nanodegree Program at Udacity](https://www.udacity.com/course/data-engineer-nanodegree--nd027) to practice data modeling in relational databases using Apache Cassandra. This a similar but simpler re-implementation of [sparkify_postgresql](https://github.com/CarlosUziel/sparkify_postgresql).

## About The Project

### Premise

> A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.
>
> They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

<p align="right">(<a href="#top">back to top</a>)</p>

### Goal

The goal of this project is to apply what I have learned on data modeling with Apache Cassandra using a Python driver. An ETL pipeline will be established to transfer data from .csv files in local directories into an Apache Cassandra database. Tables will be optimized to different queries, which will determine the choice of partition keys and clustering columns.

<p align="right">(<a href="#top">back to top</a>)</p>

### Data

This project processes event data stored as .csv files. All files will be loaded and pre-processed to build a baseline denormalized dataset.

<p align="right">(<a href="#top">back to top</a>)</p>


<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

To make use of this project, I recommend managing the required dependencies with Anaconda.

### Setting up a conda environment

Install miniconda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Install mamba:

```bash
conda install -n base -c conda-forge mamba
```

Install environment using provided file:

```bash
mamba create -f environment.yml # alternatively use environment_core.yml if base system is not debian
mamba activate sparkify_cassandra
```

### Installing and initializing an Apache Cassandra cluster

The [following instructions](https://www.hostinger.com/tutorials/set-up-and-install-cassandra-ubuntu/#How_to_Install_Cassandra_on_Ubuntu_1804_2004_and_2204) have been made for Ubuntu, consult the official Apache Cassandra [installation documentation](https://cassandra.apache.org/doc/latest/cassandra/getting_started/installing.html) if you are working under a different system

Ensure java is installed:
```bash
sudo apt-get update && sudo apt install default-jdk -y
```

Install Cassandra:
```bash
sudo apt install wget
wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
echo "deb http://www.apache.org/dist/cassandra/debian 40x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
sudo apt-get update
sudo apt install cassandra -y
```

Enable and start Cassandra service:
```bash
sudo systemctl enable cassandra
sudo systemctl start cassandra
sudo systemctl status cassandra
```

Open `/etc/cassandra/cassandra.yaml` and modify the settings as needed, for example:
```bash
cluster_name: 'Sparkify Cluster'
```

Finally, reload Cassandra and check status:
```bash
sudo systemctl stop cassandra && sudo systemctl start cassandra
nodetool status
```

## Usage

Project structure:

- `event_data`: where the .csv files are stored.
- `notebooks`: contains a single Jupyter notebook (`main.ipynb`) that runs the whole project.
- `src`: contains a single source file (`cql_queries.py`) with utility functions to generate CQL queries.

### Example query

The following is a complete example of one of the queries showcased in `notebooks/main.ipynb`:

**Get artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4:**

```python
# 1. Define PK columns
pk_cols = ("sessionId", "itemInSession")
sorted_cols = [*pk_cols, *(c for c in data_df.columns if c not in pk_cols)]

# 2. Create table
session.execute(
    get_create_table_query(
        "session_library",
        common_columns + [f"PRIMARY KEY ({', '.join(pk_cols)})"],
    )
)

# 3. Insert rows
for index, row in data_df.iterrows():
    try:
        session.execute(
            get_simple_insert_query("session_library", sorted_cols),
            tuple(row[sorted_cols].values),
        )
    except Exception as e:
        print(e)

# 4. Select query
select_cols = ("artist", "song", "length")

rows = session.execute(
    get_simple_select_query(
        "session_library",
        select_cols,
        {"sessionId": 338, "itemInSession": 4},
    )
)

for row in rows:
    print([getattr(row, c.lower()) for c in select_cols])
```

*Output:*

```bash
['Faithless', 'Music Matters (Mark Knight Dub)', Decimal('495.3073')]
```

When done interacting with the database, close the connection:

```python
session.shutdown()
cluster.shutdown()
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Additional Notes

Source files formatted using the following commands:

```bash
isort .
autoflake -r --in-place --remove-unused-variable --remove-all-unused-imports --ignore-init-module-imports .
black .
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

[Carlos Uziel Pérez Malla](https://www.carlosuziel-pm.dev/)

[GitHub](https://github.com/CarlosUziel) - [Google Scholar](https://scholar.google.es/citations?user=tEz_OeIAAAAJ&hl=es&oi=ao) - [LinkedIn](https://at.linkedin.com/in/carlos-uziel-p%C3%A9rez-malla-323aa5124) - [Twitter](https://twitter.com/perez_malla)

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

This README includes a summary of the official project description provided to the students of the [Data Engineer Nanodegree Program at Udacity](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

<p align="right">(<a href="#top">back to top</a>)</p>
