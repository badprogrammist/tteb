import csv
import model


def rows(csv_filename):
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            yield row


class Tatoeba(object):
    def __init__(self,
                 sentences_csv="sentences.csv",
                 links_csv="links.csv"):
        self.sentences_csv = sentences_csv
        self.links_csv = links_csv

    def sentences(self):
        for row in rows(self.sentences_csv):
            yield model.Sentence(*row)

    def links(self):
        for row in rows(self.links_csv):
            yield model.Link(*row)
