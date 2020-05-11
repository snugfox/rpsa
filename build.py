import os
from pathlib import Path
import shutil

file_path = Path(__file__)
proj_path = file_path.parent
rpsa_path = proj_path.joinpath("rpsa")
webui_path = rpsa_path.joinpath("webui")
model_path = proj_path.joinpath("model")
dist_path = proj_path.joinpath("dist")
dist_model_path = dist_path.joinpath("model")
dist_webui_path = dist_path.joinpath("webui")

if not dist_path.exists():
    dist_path.mkdir()
if not dist_webui_path.exists():
    dist_webui_path.mkdir()
if not dist_model_path.exists():
    dist_model_path.mkdir()

# Python code
for filename in rpsa_path.glob("*.py"):
    shutil.copy(filename, str(dist_path))

# Compiled WebUI
for filename in webui_path.joinpath("dist").glob("*"):
    shutil.copy(filename, str(dist_webui_path))

# Classifier model
for filename in model_path.glob("*.pkl"):
    shutil.copy(filename, str(dist_model_path))
