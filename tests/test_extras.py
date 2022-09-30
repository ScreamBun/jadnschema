"""
Test JADN Schema transformations
Transformation -> Reduce Complexity
"""
import os

from unittest import TestCase, skip
from jadnschema import Schema, convert

schema = 'oc2ls-v1.1-lang_resolved'


# TODO: Add CommentLevels, requires dump.py rewrite
class Conversions(TestCase):
    _test_root = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    _base_schema = f'{_test_root}/schema/{schema}.jadn'
    _test_dir = f'{_test_root}/schema_gen'

    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir(cls._test_dir):
            os.makedirs(cls._test_dir)
        cls._schema_obj = Schema.parse_file(cls._base_schema)

    @skip
    def test_CDDL(self):
        convert.cddl_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.cddl_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # convert.cddl_load(open(os.path.join(self._test_dir, schema + '.all.cddl'), 'rb').read(), os.path.join(self._test_dir, schema + '.cddl.jadn'))

    def test_GraphViz(self):
        convert.dot_dump(self._schema_obj, os.path.join(self._test_dir, schema))

    def test_HTML(self):
        convert.html_dump(self._schema_obj, os.path.join(self._test_dir, schema))

    def test_JADN(self):
        convert.jadn_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.jadn_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)

    @skip
    def test_JAS(self):
        convert.jas_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.jas_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # convert.jas_load(open(os.path.join(self._test_dir, schema + '.jas'), 'rb').read(), os.path.join(self._test_dir, schema + '.jas.jadn'))

    @skip
    def test_JIDL(self):
        convert.jidl_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.jidl_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # with open(os.path.join(self._test_dir, schema + '.jidl.jadn'), "w") as f:
        #     convert.jidl_loads(open(os.path.join(self._test_dir, schema + '.jidl'), 'rb').read()).dump(f)

    def test_JSON(self):
        for e in convert.JsonEnumStyle:
            for i in convert.JsonImportStyle:
                convert.json_dump(self._schema_obj, os.path.join(self._test_dir, f'{schema}.all.{e}.{i}'), comm=convert.CommentLevels.ALL, enum=e, imp=i)
                convert.json_dump(self._schema_obj, os.path.join(self._test_dir, f'{schema}.all.{e}.{i}'), comm=convert.CommentLevels.ALL, enum=e, imp=i)
                # convert.json_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none.{e}.{i}'), comm=convert.CommentLevels.NONE, enum=e, imp=i)
        # convert.json_load(open(os.path.join(self._test_dir, schema + '.all.json'), 'rb').read(), os.path.join(self._test_dir, schema + '.json.jadn'))

    def test_MarkDown(self):
        convert.md_dump(schema=self._schema_obj, fname=os.path.join(self._test_dir, schema))

    @skip
    def test_ProtoBuf(self):
        convert.proto_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.proto_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # convert.proto_load(open(os.path.join(self._test_dir, schema + '.all.proto'), 'rb').read(), os.path.join(self._test_dir, schema + '.proto.jadn'))

    def test_Relax_NG(self):
        convert.relax_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.relax_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # convert.relax_load(open(os.path.join(self._test_dir, schema + '.all.rng'), 'rb').read(), os.path.join(self._test_dir, schema + '.rng.jadn'))

    @skip
    def test_Thrift(self):
        convert.thrift_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.all'), comm=convert.CommentLevels.ALL)
        convert.thrift_dump(self._schema_obj, os.path.join(self._test_dir, schema + '.none'), comm=convert.CommentLevels.NONE)
        # convert.thrift_load(open(os.path.join(self._test_dir, schema + '.all.thrift'), 'rb').read(), os.path.join(self._test_dir, schema + '.thrift.jadn'))

    # Tester Functions
    def test_Analyze(self):
        analysis = self._schema_obj.analyze()
        self.assertFalse(analysis["unreferenced"], f"Unreferenced Types: {', '.join(analysis['unreferenced'])}")
        self.assertFalse(analysis["undefined"], f"Undefined Types: {', '.join(analysis['undefined'])}")

    @skip
    def test_Unfold(self):
        with open(os.path.join(self._test_dir, schema + '.init_simple.jadn'), "w") as f:
            self._schema_obj.dump(f)

        simple_schema = self._schema_obj.unfold_extensions(simple=False)
        with open(os.path.join(self._test_dir, schema + '.simple.jadn'), "w") as f:
            simple_schema.dump(f)

    def test_prettyFormat(self):
        self._schema_obj.dump(f"{self._test_dir}/{schema}_reorg.jadn")
