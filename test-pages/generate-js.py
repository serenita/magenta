#!/usr/bin/env python3

import random

total = 0

total_js = """
document.addEventListener('readystatechange', function() {
  if (document.readyState == 'complete') {
    document.getElementById('total').textContent = total;
    document.getElementById('result').textContent = total == {} ? 'Correct' : 'Wrong';
  }
});
"""

for i in range(100):
    number = random.randrange(1000)
    with open("data/data-{}.js".format(i), "w") as f:
        print("total += {}".format(number), file=f)
    total += number

with open("data/total.js", "w") as f:
    print(total_js.format(total), file=f)

print("The total is", total)
