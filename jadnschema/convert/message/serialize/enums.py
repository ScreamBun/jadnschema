from ....utils import EnumBase


class SerialFormats(str, EnumBase):
    """
    The format of an OpenC2 Serialization
    """
    # Binary Format
    CBOR = 'cbor'
    # Text Format
    JSON = 'json'
    # Extra
    # Binary
    BINN = 'binn'
    BSON = 'bson'
    ION = 'ion'
    MSGPACK = 'msgpack'
    SMILE = 'smile'
    # Text
    BENCODE = 'bencode'
    EDN = 'edn'
    S_EXPRESSION = 'sexp'
    TOML = 'toml'
    UBJSON = 'ubjson'
    XML = 'xml'
    YAML = 'yaml'

    @classmethod
    def is_binary(cls, fmt: 'SerialFormats') -> bool:
        """
        Determine if the format is binary or text based
        :param fmt: Serialization
        """
        return fmt in (cls.BINN, cls.BSON, cls.CBOR, cls.ION, cls.MSGPACK, cls.SMILE, cls.UBJSON)
