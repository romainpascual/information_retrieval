class Reader:
    def __init__(self, file):
        self.lines = Reader.read_file(file)
        self.line_count = len(self.lines)
        self.line_pointer = 0

    @staticmethod
    def read_file(file):
        with open(file, 'r') as collection:
            lines = list(map(lambda s: s.strip(), collection.readlines()))
        return lines

    def get_next_doc(self):
        try:
            while self.lines[self.line_pointer][0:2] != '.I':
                self.line_pointer += 1
        except IndexError:
            pass  # we reached EOF

    def get_docs(self):
        while True:
            self.get_next_doc()
            if self.line_pointer >= self.line_count:
                break
            docID = int(self.lines[self.line_pointer].split(' ')[1])
            self.line_pointer += 1
            assert self.lines[self.line_pointer] == '.T'  # sanity check
            self.line_pointer += 1
            docTitle = self.lines[self.line_pointer]
            yield docID, docTitle


reader = Reader("data/CACM/cacm.all")

docID_docTitle = dict()

for docID, docTitle in reader.get_docs():
    docID_docTitle[docID] = docTitle

print(docID_docTitle)