class Formatter():
    def __init__(self, data):
        self.data = data

    def format(self):
        total_max = self.get_max() + 1
        matrix = [[0] * (total_max + 4) for i in range(len(self.data))]

        for i in range(len(self.data)):
            row = matrix[i]
            row[0] = i
            row[1] = self.data[i]["pop size"]
            row[2] = self.data[i]["adult sex ratio"]
            row[3] = self.data[i]["adult to nonadult ratio"]

            for n_offspring in self.data[i]["sires"].keys():
                row[n_offspring + 4] = self.data[i]["sires"][n_offspring]

        headers = ["Rep", "Pop_Size", "Ad_Sex_Ratio", "Ad_Juv_Ratio"] + range(total_max)

        matrix.insert(0, headers)

        return matrix

    def get_max(self):
        sires = [x["sires"] for x in self.data]

        sire_max = 0

        for rep in sires:
            offspring_freq_list = rep.keys()
            offspring_freq_list.sort()
            rep_max = offspring_freq_list[-1]
            if rep_max > sire_max:
                sire_max = rep_max

        return sire_max
