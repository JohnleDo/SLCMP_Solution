import unittest
import numpy as np
import pandas as pd
from solution import SLCMP


class TestSLCMP(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        slcmp_data = [[64148, np.nan], [67118, np.nan], [40813, np.nan], [54923, np.nan]]
        plans_data = [["89379BJ2698184", "MO", "Gold", 326.14, 6],
                      ["92264NN0096790", "MO", "Silver", 361.15, 5],
                      ["35866RG6997149", "MO", "Silver", 234.6, 3],
                      ["78421VV7272023", "MO", "Silver", 290.05, 3],
                      ["26416WR0837524", "KS", "Silver", 239.13, 2],
                      ["73933HS6388428", "KS", "Silver", 236.85, 6],
                      ["22914KH3561750", "KS", "Silver", 232.91, 6],
                      ["22914KH3561755", "KS", "Silver", 232.91, 6],
                      ["71836DN6468604", "KS", "Gold", 313.17, 4],
                      ["23018XQ8604367", "WI", "Silver", 326.7, 15],
                      ["71685BQ4977053", "WI", "Catastrophic", 192.43, 11],
                      ["03388TX8996120", "WI", "Silver", 330.08, 11],
                      ["28341FR8516247", "WI", "Silver", 410.74, 15]]
        zips_data = [[64148, "MO", 29095, "Jackson", 3],
                     [67118, "KS", 20077, "Harper", 6],
                     [67118, "KS", 20095, "Kingman", 6],
                     [67118, "KS", 20173, "Sedgwick", 6],
                     [67118, "KS", 20191, "Sumner", 6],
                     [40813, "KY", 21013, "Bell", 8],
                     [54923, "WI", 55047, "Green Lake", 15],
                     [54923, "WI", 55137, "Waushara", 11],
                     [54923, "WI", 55139, "Winnebago", 11]]
        self.slcsp = SLCMP(pd.DataFrame(slcmp_data, columns=["zipcode", "rate"]),
                           pd.DataFrame(plans_data, columns=["plan_id", "state", "metal_level", "rate", "rate_area"]),
                           pd.DataFrame(zips_data, columns=["zipcode", "state", "county_code", "name", "rate_area"]))

    def test_organize_plans(self):
        expected_output = [["22914KH3561750", "KS", "Silver", 232.91, 6, 1.0],
                           ["22914KH3561755", "KS", "Silver", 232.91, 6, 1.0],
                           ["73933HS6388428", "KS", "Silver", 236.85, 6, 2.0],
                           ["26416WR0837524", "KS", "Silver", 239.13, 2, 1.0],
                           ["35866RG6997149", "MO", "Silver", 234.60, 3, 1.0],
                           ["78421VV7272023", "MO", "Silver", 290.05, 3, 2.0],
                           ["92264NN0096790", "MO", "Silver", 361.15, 5, 1.0],
                           ["23018XQ8604367", "WI", "Silver", 326.70, 15, 1.0],
                           ["03388TX8996120", "WI", "Silver", 330.08, 11, 1.0],
                           ["28341FR8516247", "WI", "Silver", 410.74, 15, 2.0]]
        self.slcsp.organize_plans("Silver")
        actual_output = self.slcsp.plans.reset_index(drop=True)
        assert actual_output.equals(pd.DataFrame(expected_output, columns=["plan_id", "state", "metal_level", "rate",
                                                                           "rate_area", "Rank"]))

    def test_find_rate_for_slcmp(self):
        expected_output = [[64148, 290.05],
                           [67118, 236.85],
                           [40813, np.nan],
                           [54923, np.nan]]
        self.slcsp.organize_plans("Silver")
        self.slcsp.find_rate_for_slcmp()
        actual_output = self.slcsp.slcmp.reset_index(drop=True)
        assert actual_output.equals(pd.DataFrame(expected_output, columns=["zipcode", "rate"]))


if __name__ == '__main__':
    unittest.main()
