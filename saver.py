import csv


class Saver:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def save(self):
        file = open(self.file_name, 'w')
        writer = csv.writer(file)

        for row in self.data:
            writer.writerow(row)
