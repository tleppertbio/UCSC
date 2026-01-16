#!/bin/bash
set -beu -o pipefail

python3 ../mask_maple.py -l test.list -m mask1.bed -d out
diff -r expected out
