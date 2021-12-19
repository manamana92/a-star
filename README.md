# a-star
A general A-star implementation evaluated on the 8-puzzle.
To modifiy the heuristic type, the `dist_mink` and `dist_null`
functions can be swapped in `__main__`.

# Files
- `puzzle.py` - The python script that takes the start node as parameters
- `puzzle` - The bash scrip that takes the start node as parameters and runs the above python script.
- `test_1` - A test script that runs the python script on `1 4 2 6 3 5 _ 7 8`
- `test_2` - A test script that runs the python script on `1 4 2 6 _  3 5 7 8`
