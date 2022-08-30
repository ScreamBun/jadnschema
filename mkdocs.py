import pdoc

from pathlib import Path

modules = ["jadnschema"]  # Public submodules are auto-imported
doc_path = Path("docs")
pdoc.pdoc(*modules, output_directory=doc_path, format="html")
