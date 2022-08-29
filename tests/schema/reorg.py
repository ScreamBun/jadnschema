import json
import os

from jadnschema import jadn

base = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    for file in os.listdir(base):
        if file.endswith(".jadn"):
            print(file)
            with open(os.path.join(base, file), "r+") as f:
                cont = json.load(f)
                f.seek(0)
                jadn.dump(cont, f)
