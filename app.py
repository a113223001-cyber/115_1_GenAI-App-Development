from pathlib import Path
import runpy

project_app = Path(__file__).resolve().parent / "Midterm Mini-Project" / "app.py"
runpy.run_path(str(project_app), run_name="__main__")
