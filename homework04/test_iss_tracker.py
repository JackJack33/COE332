#!/usr/bin/env python3

import pytest
import math
from iss_tracker import fetch_data, format_data, calculate_data_range, find_closest_epoch, calculate_average_speed, calculate_instantaneous_speed

test_data_dict = {
    'ndm': {
        'oem': {
            'body': {
                'segment': {
                    'data': {
                        'stateVector': [
                            {
                                'EPOCH': '1000-001T00:00:00.000Z',
                                'X': {'#text': '1'},
                                'Y': {'#text': '-2'},
                                'Z': {'#text': '3'},
                                'X_DOT': {'#text': '4'},
                                'Y_DOT': {'#text': '-5'},
                                'Z_DOT': {'#text': '6'}
                            },
                            {
                                'EPOCH': '1000-002T00:00:00.000Z',
                                'X': {'#text': '-7'},
                                'Y': {'#text': '8'},
                                'Z': {'#text': '-9'},
                                'X_DOT': {'#text': '10'},
                                'Y_DOT': {'#text': '-11'},
                                'Z_DOT': {'#text': '12'}
                            },
                            {
                                'EPOCH': '1000-003T00:00:00.000Z',
                                'X': {'#text': '13'},
                                'Y': {'#text': '-14'},
                                'Z': {'#text': '15'},
                                'X_DOT': {'#text': '16'},
                                'Y_DOT': {'#text': '-17'},
                                'Z_DOT': {'#text': '18'}
                            },
                            {
                                'EPOCH': '1000-004T00:00:00.000Z',
                                'X': {'#text': '-19'},
                                'Y': {'#text': '20'},
                                'Z': {'#text': '-21'},
                                'X_DOT': {'#text': '22'},
                                'Y_DOT': {'#text': '-23'},
                                'Z_DOT': {'#text': '24'}
                            }
                        ]
                    }
                }
            }
        }
    }
}

test_formatted_data = [
    {
        'timestamp': '1000-01-01 00:00:00.000000',
        'x': 1.0,
        'y': -2.0,
        'z': 3.0,
        'dx': 4.0,
        'dy': -5.0,
        'dz': 6.0
    },
    {
        'timestamp': '1000-01-02 00:00:00.000000',
        'x': -7.0,
        'y': 8.0,
        'z': -9.0,
        'dx': 10.0,
        'dy': -11.0,
        'dz': 12.0
    },
    {
        'timestamp': '1000-01-03 00:00:00.000000',
        'x': 13.0,
        'y': -14.0,
        'z': 15.0,
        'dx': 16.0,
        'dy': -17.0,
        'dz': 18.0
    },
    {
        'timestamp': '1000-01-04 00:00:00.000000',
        'x': -19.0,
        'y': 20.0,
        'z': -21.0,
        'dx': 22.0,
        'dy': -23.0,
        'dz': 24.0
    }
    ]

def test_fetch_data():
    data_dict = fetch_data()
    assert isinstance(data_dict, dict)
    assert len(data_dict) > 0

def test_format_data():
    formatted_data = format_data(test_data_dict)
    assert isinstance(formatted_data, list)
    assert all(isinstance(item, dict) for item in formatted_data)
    assert formatted_data == test_formatted_data

def test_calculate_data_range():
    formatted_data = format_data(test_data_dict)
    first_epoch, last_epoch = calculate_data_range(formatted_data)
    assert isinstance(first_epoch, str)
    assert isinstance(last_epoch, str)
    assert first_epoch == '1000-01-01 00:00:00.000000'
    assert last_epoch == '1000-01-04 00:00:00.000000'

def test_find_closest_epoch():
    formatted_data = format_data(test_data_dict)
    closest_epoch = find_closest_epoch(formatted_data)
    assert isinstance(closest_epoch, dict)
    assert closest_epoch['timestamp'] == '1000-01-04 00:00:00.000000'

def test_calculate_average_speed():
    formatted_data = format_data(test_data_dict)
    average_speed = calculate_average_speed(formatted_data)
    assert isinstance(average_speed, float)
    assert math.isclose(average_speed, 24.31, rel_tol=1)

def test_calculate_instantaneous_speed():
    formatted_data = format_data(test_data_dict)
    closest_epoch = find_closest_epoch(formatted_data)
    instantaneous_speed = calculate_instantaneous_speed(closest_epoch)
    assert isinstance(instantaneous_speed, float)
    assert math.isclose(instantaneous_speed, 39.86, rel_tol=1)
