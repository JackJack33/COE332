# Meteorite Landings Data Analysis

## Overview

This project involves tracking the International Space Station by fetching data from NASA's website and analyzing various parameters (range, closest epoch, average speed, and instantaneous speed) in Python.

### Scripts
`iss_tracker.py`
This script contains functions for fetching ISS data, formatting the data, calculating data range, finding the closest epoch, calculating speeds. Functions include `fetch_data()`, `format_data()`, `calculate_data_range()`, `find_closest_epoch()`, `calculate_average_speed()`, and `calculate_instantaneous_speed()`.

`test_iss_tracker.py`
This is the pytest file for `iss_tracker.py`.

### Running the Code
#### Non-Containerized
1. Make sure Python3 and necessary dependencies (`requests`, `xmltodict`, `math`, `logging`, `datetime`, `pytest`) are installed on your computer.
2. Download or clone this repository into a directory.
3. Run the main script (`iss_tracker.py`) and/or the test script (`test_iss_tracker.py`).
#### Containerized
1. Make sure Docker is intalled on your computer
2. Download or clone this repository into a directory.
5. In the directory, run `docker build -t iss_tracker:1.0 .` And wait for the Docker image to generate.
6. In the directory, run `docker run --rm -it iss_tracker:1.0`
7. Run `cd home`
8. Run `iss_tracker.py` and/or the test script `test_iss_tracker.py`

### Interpretation
- The `fetch_data()` function fetches the ISS data from NASA's website.
- The `format_data()` function parses the XML data into a list of dictionaries, each representing a state vector of the ISS at a specific timestamp.
- The `calculate_data_range()` function calculates the range of data based on the first and last timestamps.
- The `find_closest_epoch()` function finds the epoch closest to the current time.
- The `calculate_average_speed()` function computes the average speed of the ISS using the formatted data.
- The `calculate_instantaneous_speed()` function calculates the instantaneous speed of the ISS at the closest epoch.