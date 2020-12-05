import csv

class CsvFile:
    def __init__(self, filename):
        self.name = filename
        self.fieldnames = None
        self.index = None
        self.file = self.__init_file(filename)
    
    def __init_file(self, file):
        file_d = {}
        try:
            count = 1
            with open(file) as csvfile:
                csv_reader = csv.DictReader(csvfile, delimiter=',')
                self.fieldnames = csv_reader.fieldnames
                for row in csv_reader:
                    file_d[count] = row
                    count += 1
            return file_d
        except IOError as error:
            print(error)

    def filter(self, fieldname, value):
        for index, row in enumerate(self.file):
            if row[fieldname] != value:
                del self.file[index]

    def indexOn(self, fieldname):
        replacement = {}
        for _, row in enumerate(self.file):
            if row[fieldname]:
                val = row[fieldname]
                replacement[val] = row
        self.file = replacement

    def joinOnIndex(self, other, index, fieldname=None):
        """this is an unfinished function"""
        for _, row in enumerate(self.file):
            key = row
        return key

    def writeFile(self, filename=None):
        pass