import pandas as pd
import numpy as np
import FPLDataReader as fpldr
#Helpers
def concatenate_three_times(numpy_array, include = [1,1,1]):
    return np.concatenate((numpy_array * include[0], numpy_array* include[1], numpy_array* include[2]))

class ConstraintMaker:
    def __init__(self, data, budget = 100):
        self.data = data
        self.constraints = []
        self.number_of_players = data.shape[0]
        self.b_goalie = 1*np.array(data["Pos"] == "GK")
        self.b_defender = 1*np.array(data["Pos"] == "DEF")
        self.b_midfielder = 1*np.array(data["Pos"] == "MID")
        self.b_forward = 1*np.array(data["Pos"] == "FWD")
        self.n = 3 * self.number_of_players
        self.prices = np.array(data["Price"])
        self.budget = budget
        self.team = np.zeros((20, self.number_of_players))
        for i, team in enumerate(data["Team"].unique()):
            self.team[i] = 1*np.array(data["Team"] == team)

    def get_goalie_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_goalie, [1,0,0]),
             "c" : -1},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_goalie, [1,0,0]),
             "c" : 1},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_goalie, [1,1,0]),
             "c" : -2},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_goalie, [1,1,0]),
             "c" : 2}
            ]
    def get_defender_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_defender, [1,0,0]),
             "c" : -5},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_defender, [1,0,0]),
             "c" : 3},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_defender, [1,1,0]),
             "c" : -5},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_defender, [1,1,0]),
             "c" : 5}
            ]
    def get_midfielder_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_midfielder, [1,0,0]),
             "c" : -5},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_midfielder, [1,0,0]),
             "c" : 3},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_midfielder, [1,1,0]),
             "c" : -5},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_midfielder, [1,1,0]),
             "c" : 5}
            ]
    def get_forward_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_forward, [1,0,0]),
             "c" : -3},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_forward, [1,0,0]),
             "c" : 1},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.b_forward, [1,1,0]),
             "c" : -3},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-self.b_forward, [1,1,0]),
             "c" : 3}
            ]
    def get_starting_11_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(np.ones(self.number_of_players), [1,0,0]),
             "c" : -11},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-np.ones(self.number_of_players), [1,0,0]),
             "c" : 11}
            ]
    def get_substitute_constraints(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(np.ones(self.number_of_players), [0,1,0]),
             "c" : -4},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-np.ones(self.number_of_players), [0,1,0]),
             "c" : 4}
            ]
    def get_captain_constraints(self):
        captain_constraints = [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(np.ones(self.number_of_players), [0,0,1]),
             "c" : -1},
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(-np.ones(self.number_of_players), [0,0,1]),
             "c" : 1}
            ] #ensures that there is only one captain
        captain_in_starting_11_a_matrix = np.zeros((self.n,self.n))
        captain_in_starting_11_a_matrix[:self.number_of_players,(2*self.number_of_players):] = 1
        captain_in_starting_11_b_vector = np.zeros(self.n)
        captain_constraints.append(
            {"A" : captain_in_starting_11_a_matrix,
             "b": captain_in_starting_11_b_vector,
             "c" : -1}
            )
        captain_constraints.append(
            {"A" : -captain_in_starting_11_a_matrix,
             "b": -captain_in_starting_11_b_vector,
             "c" : 1}
            )
        return captain_constraints
    
    def get_budget_constraint(self):
        return [
            {"A" : np.zeros((self.n,self.n)),
             "b": concatenate_three_times(self.prices, [1,1,0]),
             "c" : -self.budget}
            ]
    def get_team_constraints(self):
        team_constraints = []
        for i in range(20):
            team_constraints.append(
                {"A" : np.zeros((self.n,self.n)),
                 "b": concatenate_three_times(self.team[i], [1,1,0]),
                 "c" : -3},
                )
        return team_constraints
    def get_quadratic_constraints(self):
        #These constraints assure that any player is either selected or not.
        #No fractions.
        quadratic_constraints = []
        for i in range(self.number_of_players):
            temp_a_matrix = np.zeros((self.n,self.n))
            temp_a_matrix[i,i] = 1
            temp_b_vector = np.zeros(self.n)
            temp_b_vector[i] = -1
            quadratic_constraints.append(
                {"A" :  concatenate_three_times(temp_a_matrix, [1,1,0]),
                    "b": concatenate_three_times(temp_b_vector, [1,1,0]),
                    "c" : 0}
                    )
            quadratic_constraints.append(
                {"A" :  concatenate_three_times(-temp_a_matrix, [1,1,0]),
                    "b": concatenate_three_times(-temp_b_vector, [1,1,0]),
                    "c" : 0}
                    )
        return quadratic_constraints
    

#Perform dimensionality tests
data_reader = fpldr.DataReader("fpl-form-predicted-points.csv")
data_reader.remove_low_probability_players(0.8, 4, 5)
data_reader.set_important_data(["Team", "Name", "Pos", "Price"])
data = data_reader.get_important_data()
constraint_maker = ConstraintMaker(data)
assert constraint_maker.get_goalie_constraints()[0]["A"].shape == (3*data.shape[0], 3*data.shape[0])
assert constraint_maker.get_defender_constraints()[0]["A"].shape == (3*data.shape[0], 3*data.shape[0])
assert constraint_maker.get_midfielder_constraints()[0]["A"].shape == (3*data.shape[0], 3*data.shape[0])


        