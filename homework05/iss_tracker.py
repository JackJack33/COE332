#!/usr/bin/env python3

import requests
import xmltodict
import math
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"

def fetch_data() -> Dict[str, Any]:
    """
    Fetches data from the url variable and parses it as XML using xmltodict

    Returns:
        Dict[str, Any]: The parsed XML data as a dictionary
    """
    try:
        response = requests.get(url)
        if (response.status_code != 200):
            raise requests.exceptions.RequestException
        xml_data = response.text
        return xmltodict.parse(xml_data)
    except requests.exceptions.RequestException as exception:
        logging.error(f"Error fetching data: {exception} {response}")
        return
    except xmltodict.expat.ExpatError as exception:
        logging.error(f"Error parsing XML data: {exception} {response}")
        return

def format_data(data_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses/formats the XML dictionary into a list of dictionaries

    Args:
        data_dict (Dict[str, Any]): Dictionary containing the XML data

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing formatted data
    """
    formatted_data = []

    try:
        data_list = data_dict['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        logging.error("Error: Missing or incorrect key in data dictionary")
        return formatted_data

    for stateVector in data_list:
        try:
            timestamp = datetime.strptime(stateVector['EPOCH'], "%Y-%jT%H:%M:%S.%fZ")
            timestamp = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            formatted_data.append({
                'timestamp': timestamp,
                'x': float(stateVector['X']['#text']),
                'y': float(stateVector['Y']['#text']),
                'z': float(stateVector['Z']['#text']),
                'dx': float(stateVector['X_DOT']['#text']),
                'dy': float(stateVector['Y_DOT']['#text']),
                'dz': float(stateVector['Z_DOT']['#text']),
            })
        except KeyError:
            logging.error("Error: Missing or incorrect key in state vector")
            continue
        except (ValueError, TypeError):
            logging.error("Error: Unable to parse data to the correct format")
            continue

    return formatted_data

def calculate_data_range(formatted_data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Calculates the range of data based on the first and last timestamps

    Args:
        formatted_data (List[Dict[str, Any]]): A list of dictionaries containing formatted data

    Returns:
        tuple[str]: The first and last timestamps
    """
    try:
        first_epoch = formatted_data[0]['timestamp']
        last_epoch = formatted_data[-1]['timestamp']
        return first_epoch, last_epoch
    except IndexError:
        logging.error("Error: Empty formatted_data list")
        return

def find_closest_epoch(formatted_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Finds the epoch closest to the current time in the formatted data

    Args:
        formatted_data (List[Dict[str, Any]]): A list of dictionaries containing formatted data

    Returns:
        Dict[str, [str,float]]: The dictionary representing the closest epoch
    """
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S.%f')
        closest_epoch = min(formatted_data, key=lambda x: abs(current_time - datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S.%f')))
        return closest_epoch
    except (ValueError, TypeError):
        logging.error("Error: Unable to calculate closest epoch")
        return

def calculate_average_speed(formatted_data: List[Dict[str, Any]]) -> float:
    """
    Calculates the average speed based on the formatted data

    Args:
        formatted_data (List[Dict[str, Any]]): A list of dictionaries containing formatted data

    Returns:
        float: The average speed
    """
    try:
        total_speed = 0
        for data in formatted_data:
            total_speed += math.sqrt(data['dx'] ** 2 + data['dy'] ** 2 + data['dz'] ** 2)
        return total_speed / len(formatted_data)
    except (KeyError, TypeError):
        logging.error("Error: Missing or incorrect keys in closest_epoch")
        return
    except ZeroDivisionError:
        logging.error("Error: Empty formatted_data list (division by zero)")
        return

def calculate_instantaneous_speed(closest_epoch: Dict[str, Any]) -> float:
    """
    Calculates the instantaneous speed based on the closest epoch

    Args:
        closest_epoch (Dict[str, Any]): The dictionary representing the closest epoch

    Returns:
        float: The instantaneous speed
    """
    try:
        instantaneous_speed = math.sqrt(closest_epoch['dx'] ** 2 + closest_epoch['dy'] ** 2 + closest_epoch['dz'] ** 2)
        return instantaneous_speed
    except (KeyError, TypeError):
        logging.error("Error: Missing or incorrect keys in closest_epoch")
        return

@app.route('/epochs', methods=['GET'])
def get_epochs():
    """
    Fetches data and returns subset of epochs based on parameters

    Returns:
    - list: Formatted epochs data
    """
    data_dict = fetch_data()
    formatted_data = format_data(data_dict)

    limit = request.args.get('limit', default=None, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if limit is not None:
        formatted_data = formatted_data[offset:offset+limit]
    else:
        formatted_data = formatted_data[offset:]

    return formatted_data

@app.route('/epochs/<epoch>', methods=['GET'])
def get_epoch(epoch):
    """
    Fetches data and returns specific epoch

    Args:
    - epoch (str): The timestamp for the epoch in format 'YYYY-MM-DD__HH_MM_SS.SSSSSS'

    Returns:
    - dict: A dictionary containing the epoch data if found
    """
    epoch = epoch.replace("__", " ").replace("_", ":")
    data_dict = fetch_data()
    formatted_data = format_data(data_dict)
    for data in formatted_data:
        if data['timestamp'] == epoch:
            return data
    return {'error': 'Epoch not found'}, 404

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def get_epoch_speed(epoch):
    """
    Fetches data and returns a specific epoch's instantaneous speed

    Args:
    - epoch (str): The timestamp for the epoch in format 'YYYY-MM-DD__HH_MM_SS.SSSSSS'

    Returns:
    - dict: A dictionary containing the epoch's state vector and instantaneous speed
    """
    epoch = epoch.replace("__", " ").replace("_", ":")
    data_dict = fetch_data()
    formatted_data = format_data(data_dict)
    for data in formatted_data:
        if data['timestamp'] == epoch:
            speed = calculate_instantaneous_speed(data)
            return {'speed': speed}
    return {'error': 'Epoch not found'}, 404

@app.route('/now', methods=['GET'])
def get_now():
    """
    Retrieves data for the closest epoch to the current time and calculates its speed

    Returns:
    - dict: A dictionary containing the closest epoch timestamp and its associated speed
    """
    data_dict = fetch_data()
    formatted_data = format_data(data_dict)
    closest_epoch = find_closest_epoch(formatted_data)
    speed = calculate_instantaneous_speed(closest_epoch)
    return {'closest_epoch': closest_epoch, 'speed': speed}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
