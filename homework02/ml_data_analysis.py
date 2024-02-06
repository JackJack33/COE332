#!/usr/bin/env python3

import csv
import numpy as np
import logging
from gcd_algorithm import greatCircleDistance

def topClassesByYear(ml_data: dict, classKey: str, yearKey: str) -> dict:
    """
    Computes the top meteorite classes by year

    Args:
        ml_data (dict): The data dictionary containing meteorite data
        classKey (str): The key representing the meteorite class
        yearKey (str): The key representing the year

    Returns:
        dict: A dictionary containing the top meteorite classes for each year
    """

    year_class_counts = {}

    for row in ml_data['meteorite_landings']:
        try:
            m_year = row[yearKey]
            m_class = row[classKey]

            if m_year == '': raise ValueError
            if m_class == '': raise ValueError

            if int(m_year) > 2024: raise ValueError

            if m_year not in year_class_counts:
                year_class_counts[m_year] = {}

            if m_class not in year_class_counts[m_year]:
                year_class_counts[m_year][m_class] = 0

            year_class_counts[m_year][m_class] += 1

        except ValueError:
            logging.warning(f'Encountered incompatible value ({row[yearKey]}, {row[classKey]}) in topClassesByYear')

    sorted_years = sorted(year_class_counts.keys())
    sorted_year_class_counts = {}
    for year in sorted_years:
        sorted_year_class_counts[year] = dict(sorted(year_class_counts[year].items(),
                                              key=lambda x: x[1],
                                              reverse=True))
    return sorted_year_class_counts

def missingValues(ml_data: dict) -> dict:
    """
    Computes the count of missing values in each column of the dataset

    Args:
        ml_data (dict): The data dictionary containing meteorite data

    Returns:
        dict: A dictionary containing the count of missing values for each column
    """

    missing_value_counts = {}

    if not ml_data['meteorite_landings']:
        return missing_value_counts

    for column in ml_data['meteorite_landings'][0].keys():

        missing_count = 0
        for row in ml_data['meteorite_landings']:
            if row[column] == '':
                missing_count += 1

        missing_value_counts[column] = missing_count

    return missing_value_counts

def avgDistanceFromEquator(ml_data: dict, latKey: str, lonKey: str) -> float:
    """
    Computes the average distance from the equator based on latitude and longitude data

    Args:
        ml_data (dict): The data dictionary containing meteorite data
        latKey (str): The key representing latitude
        lonKey (str): The key representing longitude

    Returns:
        float: The average distance from the equator
    """

    total_distance = 0
    total_points = 0

    for row in ml_data['meteorite_landings']:
        try:
            lat = float(row[latKey])
            lon = float(row[lonKey])

            total_distance += greatCircleDistance(lat, 0, lat, lon)
            total_points += 1
        except ValueError:
            logging.warning(f'Encountered incompatible value ({row[latKey]}, {row[lonKey]}) in avgDistanceFromEquator')

    logging.debug(f'Total Dist: {total_distance}, Total Pts: {total_points}')
    return total_distance / total_points if total_points > 0 else 0


def main():
    ml_data = {}
    ml_data['meteorite_landings'] = []
    with open('Meteorite_Landings_20240205.csv', 'r', encoding='cp850') as f:
        reader = csv.DictReader(f, delimiter=',')
        for index, row in enumerate(reader):
            try:
                ml_data['meteorite_landings'].append(dict(row))
            except:
                logging.error(f'Unable to load row {index} in csv file')

    logging.debug(f'Loaded csv file with {len(ml_data['meteorite_landings'])} rows')

    top_classes = topClassesByYear(ml_data, 'recclass', 'year')
    missing_values = missingValues(ml_data)
    avg_distance = avgDistanceFromEquator(ml_data, 'reclat', 'reclong')

    logging.debug('Done computing functions')

    # Top classes by year
    year_range = [2008, 2010] # inclusive

    print()
    print('Top Meteorite Classes by Year:')
    for year, classes in top_classes.items():
        if not (year_range[0] <= int(year) <= year_range[1]): continue
        print(f'Year: {year}')
        for index, (meteorite_class, count) in enumerate(classes.items()):
            print(f"{index+1})  Class: {meteorite_class}, Count: {count}")
            if index >= 4: break
        print()

    # Missing values
    print("Missing Values:")
    for column, count in missing_values.items():
        print(f"{column}: {count}")

    # Avg distance from equator
    print()
    print(f"Average Distance from Equator: {avg_distance:.2f} kilometers")

    logging.debug('Done printing summaries')

if __name__ == '__main__':
    main()
