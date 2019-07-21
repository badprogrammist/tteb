import re
import string


class Teacher(object):
    def __init__(self, searcher, repository):
        self.repository = repository
        self.searcher = searcher
        self._split_ex = re.compile(r"|".join(string.whitespace))

    def _tokenize(self, text):
        return [token.lower()
                for token in self._split_ex.split(text)]

    def learn(self, text, pupil, blackboard, homelang="rus", learnlang="eng"):
        if text is None or text == "":
            blackboard.write("Nothing to learn")

        tokens = self._tokenize(text)
        sentence_ids = self.searcher.search(tokens)

        if len(sentence_ids) == 0:
            blackboard.write("There are no material to learn by")

        for sid in sentence_ids:
            sentence = self.repository.sentence(sid)
            if sentence.get("language") != learnlang:
                continue

            translate_ids = self.repository.translates(sid)

            if len(translate_ids) == 0:
                continue

            tidx = 0
            translate_sentence = self.repository.sentence(translate_ids[tidx])

            while translate_sentence.get("language") != homelang and tidx < len(translate_ids):
                translate_sentence = self.repository.sentence(translate_ids[tidx])
                tidx += 1

            if translate_sentence.get("language") != homelang:
                continue

            blackboard.write("")
            blackboard.write(translate_sentence.get("text"))

            answer = pupil.answer("Translate")

            blackboard.write("Your answered : {}".format(answer))
            blackboard.write("Correct answer: {}".format(sentence.get("text")))

