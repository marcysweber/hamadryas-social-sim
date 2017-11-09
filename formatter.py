class Formatter():
    def __init__(self, data):
        self.data = data

    def format(self):
        matrix = [[0] * 14 for i in range(len(self.data))]

        for i in range(len(self.data)):
            row = matrix[i]
            row[0] = i
            row[1] = self.data[i]["pop_size"]
            row[2] = self.data[i]["adult_sex_ratio"]
            row[3] = self.data[i]["adult_to_nonadult_ratio"]

            row[4] = self.data[i]["within_omu_relat_mean"]
            row[5] = self.data[i]["within_omu_relat_var"]
            row[6] = self.data[i]["within_dyads"]
            row[7] = self.data[i]["across_omu_relat_mean"]
            row[8] = self.data[i]["across_omu_relat_var"]
            row[9] = self.data[i]["across_dyads"]

            row[10] = self.data[i]["initial_units"]
            row[11] = self.data[i]["opportunistic_takeovers"]
            row[12] = self.data[i]["inheritances"]
            row[13] = self.data[i]["challenge_takeovers"]


        headers = ["Rep", "Pop_Size", "Ad_Sex_Ratio", "Ad_Juv_Ratio",
                   "within_omu_relat_mean","within_omu_relat_var", "within_dyads_count",
                   "across_omu_relat_mean","across_omu_relat_var", "across_dyads_count",
                   "initial_units", "opportunistic_takeovers", "inheritances", "challenge_takeovers"]

        matrix.insert(0, headers)

        return matrix


