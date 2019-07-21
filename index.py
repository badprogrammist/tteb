from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StandardAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.query import Term, And

SENTENCE_SCHEMA = Schema(id=ID(stored=True, unique=True),
                         language=ID(),
                         text=TEXT(analyzer=StandardAnalyzer(stoplist=None)))

DEFAULT_PATH = "index"


def index_sentences(repository, path=DEFAULT_PATH):
    ix = create_in(path,
                   schema=SENTENCE_SCHEMA,
                   indexname="sentences")
    count = 0
    writer = ix.writer(limitmb=512,
                       procs=1,
                       multisegment=True)
    for sentence in repository.sentences():
        writer.add_document(id=sentence.get("id"),
                            language=sentence.get("language"),
                            text=sentence.get("text"))
        count += 1
        if count == 1000:
            writer.commit(merge=False)
            writer = ix.writer(limitmb=512,
                               procs=1,
                               multisegment=True)
            print("Index {} sentences".format(count))
            count = 0

    writer.commit(merge=False)
    print("Index {} sentences".format(count))


class Searcher(object):
    def __init__(self, path=DEFAULT_PATH):
        ix = open_dir(path,
                      indexname="sentences")
        self._searcher = ix.searcher()

    def search(self, tokens):
        if len(tokens) > 1:
            query = And([Term("text", token) for token in tokens])
        else:
            query = Term("text", tokens[0])

        results = self._searcher.search(query,
                                        limit=None)
        return [hit.fields().get("id") for hit in results]


def searcher():
    return Searcher()
