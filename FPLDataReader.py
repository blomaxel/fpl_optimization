import pandas as pd
import numpy as np

class DataReader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.all_data = pd.read_csv(data_path)
        self.kept_data = pd.DataFrame()

    def set_important_data(self, important_attribute_headers : list[str]):
        self.kept_data = self.all_data[important_attribute_headers]

    def get_important_data(self):
        return self.kept_data
    
    def remove_low_probability_players(self, threshold, current_gw, number_of_gw):
        for i in range(current_gw, current_gw + number_of_gw):
            self.kept_data = self.kept_data[self.kept_data[f'{i}_prob'] > threshold]

    def remove_immediate_low_probability_players(self, threshold, current_gw):
        self.remove_low_probability_players(threshold, current_gw, 1)

def test_data_reader(path = "fpl-form-predicted-points.csv"):
    data_reader = DataReader(path)
    current_gw = 4
    number_of_gw = 5
    important_attribute_headers = ['Team', 'Name', 'Pos', 'Price']
    for i in range(current_gw, current_gw + number_of_gw):
        important_attribute_headers.append(f'{i}_pts_no_prob')
        important_attribute_headers.append(f'{i}_prob')
    data_reader.set_important_data(important_attribute_headers)
    data_reader.remove_low_probability_players(0.8, current_gw, number_of_gw)
    print(data_reader.get_important_data().shape)
