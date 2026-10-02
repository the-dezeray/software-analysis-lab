# Lab 3 - AI vs my tests

Prompt I used: "Give EP classes and 10 boundary test cases (input, expected)
for calculate_discount(price, is_premium) where price is 0-10000 and
is_premium is bool. True = 20% off."

AI gave 10 cases. 6 were the same as mine (0, 100, 10000 with True/False).
What it missed: it did not test 9999.99, 10000.01, or None.

What it got wrong:
- AI said (-1, True) -> 0, "clamped". Should be ValueError.
- AI said (999999, True) -> valid. Should be ValueError, over max.
- AI said (100, 1) -> 80, "truthy ok". Should be TypeError, must be bool.
- AI said 5000 is a boundary. It is not, just a normal value.

So AI got about 6/10 right. It is ok for normal cases but bad for
invalid and edge cases. I had to fix all its expected outputs by hand.
