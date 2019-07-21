import attr
import rocksdb
import json


class RocksRepository(object):

    def __init__(self, path="db"):
        class SentencePrefix(rocksdb.interfaces.SliceTransform):
            def name(self):
                return b'sentence'

            def transform(self, src):
                return (0, 8)

            def in_domain(self, src):
                return len(src) >= 8

            def in_range(self, dst):
                return len(dst) == 8

        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.max_open_files = 300000
        opts.write_buffer_size = 67108864
        opts.max_write_buffer_number = 3
        opts.target_file_size_base = 67108864
        opts.prefix_extractor = SentencePrefix()

        opts.table_factory = rocksdb.BlockBasedTableFactory(
            filter_policy=rocksdb.BloomFilterPolicy(10),
            block_cache=rocksdb.LRUCache(500 * (1024 ** 2)),
            block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
        self._db = rocksdb.DB(path, opts)

    @staticmethod
    def _sentence_key(sid):
        return "sentence:{}".format(sid).encode("utf-8")

    def put_sentences(self, sentences):
        batch = rocksdb.WriteBatch()

        for sentence in sentences:
            sentence_dict = attr.asdict(sentence)
            dump = json.dumps(sentence_dict)
            batch.put(self._sentence_key(sentence.id), dump.encode("utf-8"))

        self._db.write(batch)
        print("Save {} sentences".format(len(sentences)))

    def update_sentences_ids(self, ids):
        saved_ids = self.get_sentences_ids()
        saved_ids.extend(list(ids))
        self._db.put(b"ids:sentence", json.dumps(saved_ids).encode("utf-8"))

    def sentence(self, sid):
        raw = self._db.get(self._sentence_key(sid))
        return json.loads(raw)

    def sentences(self):
        prefix = b'sentence'
        it = self._db.iteritems()
        it.seek(prefix)
        for key, sentence in it:
            if key.startswith(prefix):
                yield json.loads(sentence)

    def get_sentences_ids(self):
        dump = self._db.get(b"ids:sentence")
        if dump is None:
            dump = b"[]"
        return json.loads(dump)

    @staticmethod
    def _link_id(sid):
        return "link:{}".format(sid).encode("utf-8")

    def put_links(self, links):
        batch = rocksdb.WriteBatch()

        for sentence_id, translates in links:
            dump = json.dumps(translates)
            batch.put(self._link_id(sentence_id), dump.encode("utf-8"))

        self._db.write(batch)
        print("Save {} links".format(len(links)))

    def translates(self, sid):
        raw = self._db.get(self._link_id(sid))
        return json.loads(raw) if raw is not None else []
