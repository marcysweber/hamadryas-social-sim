class Formatter():
    def __init__(self, data):
        self.data = data

    def format(self):
        matrix = [[0] * 10 for i in range(len(self.data))]

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

        headers = ["Rep", "Pop_Size", "Ad_Sex_Ratio", "Ad_Juv_Ratio",
                   "within_omu_relat_mean","within_omu_relat_var","across_omu_relat_mean","across_omu_relat_var"]

        matrix.insert(0, headers)

        return matrix


