import textdistance
import difflib

class FileSimilarity:
    def __init__(self, file1, file2):
        self._file1 = file1
        self._file2 = file2

    def get_similarity(self):
        sim =  textdistance.Jaccard(qval = 5).normalized_similarity(self._file1, self._file2)
        return sim


