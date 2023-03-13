import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format= "[%(asctime)s: %(levelname)s]: %(message)s"
    )

dir = "src"
# list of files:
list_of_files = [
    f"{dir}/data/UpperLake/README.md",
    f"{dir}/data/KaliyasotDam/README.md",
    f"{dir}/data/MotiaTalab/README.md",
    f"{dir}/data/NawabSiddiquiHasanKhanTalaab/README.md",
    f"{dir}/data/SarangpaniLake/README.md",
    f"{dir}/data/HathaikhedaDam/README.md",
    f"{dir}/data/LowerLake/README.md",
    f"{dir}/data/ManitLake/README.md",
    f"{dir}/data/JawaharBaalUdyanLake/README.md",
    f"{dir}/data/ShahpuraLake/README.md",
    f"{dir}/data/KerwaDam/README.md",
    f"{dir}/data/LendiyaTalab/README.md",
    f"{dir}/data/NawabMunshiHussainKhanTalab/README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating a directory at: {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating a new file: {filename} at path: {filepath}")
    else:
        logging.info(f"file is already present at: {filepath}")