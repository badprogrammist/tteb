import db
import index
import tatoeba


def bunch(items, criteria=lambda x: True, size=1000):
    bunches = []

    for item in items:
        if criteria(item) and len(bunches) < size:
            bunches.append(item)

        if len(bunches) == size:
            print("Load sentences")
            yield bunches
            bunches = []

    yield bunches


def load_sentences(ttb, repository):
    languages = {"eng", "rus"}

    for sentences in bunch(ttb.sentences(),
                           lambda s: s.language in languages):
        repository.put_sentences(sentences)

        # TODO Move to repository
        sentences_ids = {sentence.id for sentence in sentences}
        repository.update_sentences_ids(sentences_ids)


def load_links(ttb, repository, bunch_size=1000):
    links = []
    sentence_id = None
    translates = []
    sentences_ids = set(repository.get_sentences_ids())

    for link in ttb.links():
        if (link.sentence_id not in sentences_ids
                or link.translate_id not in sentences_ids):
            continue

        if sentence_id != link.sentence_id:
            if len(links) < bunch_size:
                if sentence_id is not None:
                    links.append((sentence_id, translates))
            else:
                repository.put_links(links)
                links = []

            translates = []

        sentence_id = link.sentence_id
        translates.append(link.translate_id)

    repository.put_links(links)


def load():
    ttb = tatoeba.Tatoeba()
    repository = db.RocksRepository()

    load_sentences(ttb, repository)
    load_links(ttb, repository)

    index.index_sentences(repository)
