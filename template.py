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
    f"{dir}/visualizations/UpperLake/README.md",
    f"{dir}/visualizations/KaliyasotDam/README.md",
    f"{dir}/visualizations/MotiaTalab/README.md",
    f"{dir}/visualizations/NawabSiddiquiHasanKhanTalaab/README.md",
    f"{dir}/visualizations/SarangpaniLake/README.md",
    f"{dir}/visualizations/HathaikhedaDam/README.md",
    f"{dir}/visualizations/LowerLake/README.md",
    f"{dir}/visualizations/ManitLake/README.md",
    f"{dir}/visualizations/JawaharBaalUdyanLake/README.md",
    f"{dir}/visualizations/ShahpuraLake/README.md",
    f"{dir}/visualizations/KerwaDam/README.md",
    f"{dir}/visualizations/LendiyaTalab/README.md",
    f"{dir}/visualizations/NawabMunshiHussainKhanTalab/README.md",
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