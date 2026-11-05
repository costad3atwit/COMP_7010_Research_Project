# COMP_7010_Research_Project
Exploring the real-time performance of O(nlog(n)) sorting algorithms when faced with various adversarial inputs.

## To run the code:
1. Create and activate a python virtual environment in the project root directory with the following
    1. `python -m venv venv`
    2. `source venv/bin/activate`
2. run `pip install -r requirements.txt`
3. run `pytest -s src/algorithms.py` for verbose output containing the actual comparison count for each sorting algorithm or `pytest -s src/algorithms.py` to just see pass/fail