import pandas as pd


class SLCMP:
    def __init__(self, slcmp, plans, zips):
        self.slcmp = slcmp
        self.plans = plans
        self.zips = zips

    def organize_plans(self, metal_level):
        """
        This function will get rid of rows that aren't of the metal_level specified. Then we organize them for easier
        reading (this part isn't really needed but its nice to have for debugging). After that we will then rank them
        based on the state and rate_area of their price to determine the second lowest cost later on.
        """
        self.plans = self.plans[self.plans["metal_level"] == metal_level]
        self.plans = self.plans.sort_values(["state", "rate"])
        self.plans["Rank"] = self.plans.groupby(["state", "rate_area"])["rate"].rank(method="dense")

    def find_rate_for_slcmp(self):
        """
        This function will go through the self.slcmp and check each zipcode in that dataframe. For each zipcode in the self.slcmp it
        will then locate the same zipcode found in the self.zips dataframe. This should return a list of zipcodes that match it or not.
        When we get that list we will then check if we have more than one rate_area for that zipcode so that we can avoid looking for a
        second low cost for it due to it being ambigous with two rate_areas instead of one. Now that we have a list we then iterate through
        all the potential zipcodes we got from self.zips and try to find a match in our self.plans dataframe with the extra criteria of "rate_area".
        If we get a match then we store it into a list called info. Then we check if our info list is empty, if not then we take the first value it
        has in the list since there should only be one match unless we have a duplicate then it still doesn't matter and set it to our SLCSP in the rate
        column.
        """
        for slcmp_index, slcmp_row in self.slcmp.iterrows():
            zipcodes = self.zips.loc[(self.zips["zipcode"] == slcmp_row["zipcode"])]
            check_rate_area = zipcodes["rate_area"].drop_duplicates()

            if len(check_rate_area) <= 1:
                for zipcode_index, zipcode_row in zipcodes.iterrows():
                    info = self.plans.loc[(self.plans["state"] == zipcode_row["state"]) &
                                          (self.plans["rate_area"] == zipcode_row["rate_area"]) &
                                          (self.plans["Rank"] == 2.0)]
                if not info.empty:
                    self.slcmp.loc[slcmp_index, "rate"] = info.iloc[0]["rate"]


if __name__ == '__main__':
    slcsp = SLCMP(pd.read_csv("slcsp.csv"), pd.read_csv("plans.csv"), pd.read_csv("zips.csv"))
    slcsp.organize_plans("Silver")
    slcsp.find_rate_for_slcmp()
    print(slcsp.slcmp.to_string())
