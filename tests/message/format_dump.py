import json

from jadnschema.convert import SerialFormats
from jadnschema.convert.message.serialize import encode_msg

orig_file = "query_pairs"
orig_fmt = SerialFormats.JSON


if __name__ == "__main__":
    with open(f"{orig_file}.json", "r", encoding="utf-8") as f:
        original_obj = json.load(f)

    for enc in SerialFormats:
        if enc == orig_fmt:
            continue
        print(f"converting to {enc}")
        with open(f"{orig_file}.{enc}", "wb") as f:
            msg = encode_msg(original_obj, enc, True)
            f.write(msg if isinstance(msg, bytes) else msg.encode("utf-8"))
