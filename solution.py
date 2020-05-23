import pandas as pd


class SLCMP:
    def __init__(self, slcmp, plans, zips):
        self.slcmp = slcmp
        self.plans = plans
        self.zips = zips

    def organize_plans(self, metal_level):
        """
        This function will get rid of rows that aren't of the metal_level of Silver. Then it will get rid of
        duplicates based on state, rate, and rate_area while just keeping the first occurance.
        """
        self.plans = self.plans[self.plans["metal_level"] == metal_level]
        self.plans = self.plans.sort_values(["state", "rate"])
        self.plans = self.plans.drop_duplicates(subset=["state", "rate", "rate_area"], keep="first")

    def find_slcmp_in_plans(self):
        """
        This function will find the second smallest Silver value per rate_area and state. This is done by finding the
        smallest rate value's index within a group based on the columns state and rate area. Then it will remove it from
        the original dataframe and then proceed to obtain the next smallest value just like before which is basically our
        second smallest value. After that we'll locate all those values with the index we got with our original dataframe to
        get the full information.
        """
        firstMinindexes = self.plans.groupby(["state", "rate_area"]).idxmin()
        self.plans = self.plans.drop(firstMinindexes["rate"])
        secondMinindexes = self.plans.groupby(["state", "rate_area"]).idxmin()
        self.plans = self.plans.loc[secondMinindexes["rate"].tolist()]

    def find_rate_for_slcmp(self):
        """
        This function will go through the self.slcmp and check each zipcode in that dataframe. For each zipcode in the self.slcmp it
        will then locate the same zipcode found in the self.zips dataframe. This should return a list of zipcodes that match it or not.
        When we get that list we will then check if we have more than one rate_area for that zipcode so that we can avoid looking for a
        second low cost for it due to it being ambigous with two rate_areas instead of one. Now that we have a list we then iterate through
        all the potential zipcodes we got from self.zips and try to find a match in our self.plans dataframe with the extra criteria of "rate_area".
        If we get a match then we store it into a list called info (reason for storing it into a list is because there can be the case of multiple
        matches of even no matches). Then we check if our info list is empty, if not then we take the first value it has in the list because from
        the previous functions we already got rid of the lowest value and they should be organized from smallest to biggest value. And with all
        that we add that value to the column "rate" for that zipcode in self.slcmp
        """
        for slcmp_index, slcmp_row in self.slcmp.iterrows():
            zipcodes = self.zips.loc[(self.zips["zipcode"] == slcmp_row["zipcode"])]
            check_rate_area = zipcodes["rate_area"].drop_duplicates()

            if len(check_rate_area) <= 1:
                for zipcode_index, zipcode_row in zipcodes.iterrows():
                    info = self.plans.loc[(self.plans["state"] == zipcode_row["state"]) & (self.plans["rate_area"] == zipcode_row["rate_area"])]
                    if not info.empty:
                        self.slcmp.loc[slcmp_index, "rate"] = info.iloc[0]["rate"]


if __name__ == '__main__':
    slcsp = SLCMP(pd.read_csv("slcsp.csv"), pd.read_csv("plans.csv"), pd.read_csv("zips.csv"))
    slcsp.organize_plans("Silver")
    slcsp.find_slcmp_in_plans()
    slcsp.find_rate_for_slcmp()
