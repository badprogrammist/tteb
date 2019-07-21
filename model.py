import attr


@attr.s
class Sentence(object):
    id = attr.ib()
    language = attr.ib()
    text = attr.ib()


@attr.s
class Link(object):
    sentence_id = attr.ib()
    translate_id = attr.ib()
