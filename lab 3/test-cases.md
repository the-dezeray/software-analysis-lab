# Lab 3 - my test cases (11 cases)

| # | Input | Expected | Covers |
|---|-------|----------|--------|
| 1 | (-1, True) | ValueError | EP1 |
| 2 | (0, False) | 0 | EP2 |
| 3 | (0.01, True) | 0.008 | EP3, lower edge |
| 4 | (100, True) | 80 | EP3 |
| 5 | (100, False) | 100 | EP3 |
| 6 | (9999.99, True) | 7999.992 | EP3, upper edge |
| 7 | (10000, True) | 8000 | EP4 |
| 8 | (10000.01, False) | ValueError | EP5 |
| 9 | ("100", True) | TypeError | EP6 |
| 10 | (100, 1) | TypeError | EP8 |
| 11 | (100, None) | TypeError | EP8 |

File: tests/test_discount_lab3.py

## Results

Ran `pytest -v`. My file: 7 passed, 4 failed.
Failed: 1, 8, 10, 11 - all DID NOT RAISE.
This means the code has no range or type checks for price and flag.
