import pytest
from ml_data_analysis import topClassesByYear, missingValues, avgDistanceFromEquator
from gcd_algorithm import greatCircleDistance

def test_topClassesByYear():
    data = {'meteorite_landings': []}
    assert topClassesByYear(data, 'recclass', 'year') == {}

    data = {'meteorite_landings': [{'recclass': 'H5', 'year': '2000'},
                                    {'recclass': 'L6', 'year': '2000'},
                                    {'recclass': 'H5', 'year': '2001'},
                                    {'recclass': 'H5', 'year': '2001'},
                                    {'recclass': '', 'year': '2001'},
                                    {'recclass': 'H5', 'year': ''},
                                    {'recclass': '', 'year': ''}]}
    assert topClassesByYear(data, 'recclass', 'year') == {'2000': {'H5': 1, 'L6': 1}, '2001': {'H5': 2}}

    pass

def test_missingValues():
    data = {'meteorite_landings': []}
    assert missingValues(data) == {}

    data = {'meteorite_landings': [{'recclass': 'H5', 'year': '2000'},
                                    {'recclass': '', 'year': '2001'},
                                    {'recclass': 'L6', 'year': '2001'},
                                    {'recclass': 'H5', 'year': ''},
                                    {'recclass': '', 'year': ''}]}
    assert missingValues(data) == {'recclass': 2, 'year': 2}

    pass

def test_avgDistanceFromEquator():
    data = {'meteorite_landings': []}
    assert avgDistanceFromEquator(data, 'reclat', 'reclong') == 0

    data = {'meteorite_landings': [{'reclat': '10', 'reclong': '20'},
                                    {'reclat': '0', 'reclong': '0'},
                                    {'reclat': '45', 'reclong': '90'},
                                    {'reclat': '45', 'reclong': ''},
                                    {'reclat': '', 'reclong': '90'},
                                    {'reclat': '', 'reclong': ''}]}
    assert avgDistanceFromEquator(data, 'reclat', 'reclong') == ((greatCircleDistance(10, 0, 10, 20) + greatCircleDistance(0, 0, 0, 0) + greatCircleDistance(45, 0, 45, 90)) / 3)

    pass
