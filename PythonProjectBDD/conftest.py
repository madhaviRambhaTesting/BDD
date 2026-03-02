"""
conftest.py – root-level pytest configuration
──────────────────────────────────────────────
Adds the PythonProjectBDD directory to sys.path so that all
sub-packages (features.pages, tests.support, POM_BDD) resolve
correctly regardless of the working directory.

Stories  : MDP-310 | MDP-312
Framework: pytest-bdd
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(__file__))
