# Lab 3 - EP and BVA tables (my work)

Function: `calculate_discount(price, is_premium)` in app/tasks.py

Spec I used: price must be a number from 0 to 10000.
is_premium must be True or False. True = price*0.8, False = same price.
Anything else should give ValueError or TypeError.

## EP table

| ID | Input | Class | Valid? |
|----|-------|-------|--------|
| EP1 | price < 0 | negative | no |
| EP2 | price = 0 | zero | yes |
| EP3 | 0 < price < 10000 | normal | yes |
| EP4 | price = 10000 | max | yes |
| EP5 | price > 10000 | too big | no |
| EP6 | price = str/None | not a number | no |
| EP7 | is_premium = True/False | bool | yes |
| EP8 | is_premium = 1/None/"true" | not bool | no |

## BVA table

| Boundary | Below | On | Above |
|----------|-------|----|-------|
| 0 | -0.01 (invalid) | 0 (valid) | 0.01 (valid) |
| 10000 | 9999.99 (valid) | 10000 (valid) | 10000.01 (invalid) |
