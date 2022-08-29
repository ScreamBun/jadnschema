"""
Test JADN Schema transformations
Transformation -> Reduce Complexity
"""
import os

from unittest import TestCase, skip
from jadnschema import (
    convert,
    jadn,
    # Enums
    CommentLevels,
    JsonEnumStyle,
    JsonImportStyle
)


# TODO: Add CommentLevels, requires dump.py rewrite
class Conversions(TestCase):
    _test_root = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    _schema = 'oc2ls-v1.0.1-resolved'
    _base_schema = f'{_test_root}/schema/{_schema}.jadn'
    _test_dir = f'{_test_root}/schema_gen'

    def setUp(self) -> None:
        if not os.path.isdir(self._test_dir):
            os.makedirs(self._test_dir)
        self._schema_obj = jadn.load(self._base_schema)

    def test_CDDL(self):
        convert.cddl_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.cddl_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # convert.cddl_load(open(os.path.join(self._test_dir, self._schema + '.all.cddl'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.cddl.jadn'))

    def test_GraphViz(self):
        convert.dot_dump(self._schema_obj, os.path.join(self._test_dir, self._schema))

    def test_HTML(self):
        convert.html_dump(self._schema_obj, os.path.join(self._test_dir, self._schema))

    def test_JADN(self):
        convert.jadn_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.jadn_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)

    def test_JAS(self):
        convert.jas_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.jas_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # convert.jas_load(open(os.path.join(self._test_dir, self._schema + '.jas'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.jas.jadn'))

    def test_JIDL(self):
        convert.jidl_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.jidl_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # with open(os.path.join(self._test_dir, self._schema + '.jidl.jadn'), "w") as f:
        #     convert.jidl_loads(open(os.path.join(self._test_dir, self._schema + '.jidl'), 'rb').read()).dump(f)

    def test_JSON(self):
        for e in JsonEnumStyle:
            for i in JsonImportStyle:
                convert.json_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + f'.all.{e}.{i}'), comm=CommentLevels.ALL, enum=e, imp=i)
                # convert.json_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none.{e}.{i}'), comm=CommentLevels.NONE, enum=e, imp=i)
        # convert.json_load(open(os.path.join(self._test_dir, self._schema + '.all.json'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.json.jadn'))

    def test_MarkDown(self):
        convert.md_dump(schema=self._schema_obj, fname=os.path.join(self._test_dir, self._schema))

    @skip
    def test_ProtoBuf(self):
        convert.proto_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.proto_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # convert.proto_load(open(os.path.join(self._test_dir, self._schema + '.all.proto'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.proto.jadn'))

    def test_Relax_NG(self):
        convert.relax_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.relax_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # convert.relax_load(open(os.path.join(self._test_dir, self._schema + '.all.rng'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.rng.jadn'))

    def test_Thrift(self):
        convert.thrift_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.all'), comm=CommentLevels.ALL)
        convert.thrift_dump(self._schema_obj, os.path.join(self._test_dir, self._schema + '.none'), comm=CommentLevels.NONE)
        # convert.thrift_load(open(os.path.join(self._test_dir, self._schema + '.all.thrift'), 'rb').read(), os.path.join(self._test_dir, self._schema + '.thrift.jadn'))

    # Tester Functions
    @skip
    def test_Analyze(self):
        analysis = self._schema_obj.analyze()
        self.assertFalse(analysis["unreferenced"], f"Unreferenced Types: {', '.join(analysis['unreferenced'])}")
        self.assertFalse(analysis["undefined"], f"Undefined Types: {', '.join(analysis['undefined'])}")

    @skip
    def test_Unfold(self):
        with open(os.path.join(self._test_dir, self._schema + '.init_simple.jadn'), "w") as f:
            self._schema_obj.dump(f)

        simple_schema = self._schema_obj.unfold_extensions(simple=False)
        with open(os.path.join(self._test_dir, self._schema + '.simple.jadn'), "w") as f:
            simple_schema.dump(f)

    @skip
    def test_prettyFormat(self):
        self._schema_obj.dump(f"{self._test_dir}/{self._schema}_reorg.jadn")
