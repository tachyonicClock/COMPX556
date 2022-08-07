#!/bin/bash

function run_experiments() {
    echo "Run: $1 Problem: $2"
    mkdir -p "runs/run_$1"
    ./packing LNS  "problems/problem$2.csv" "runs/run_$1/$2_LNS.txt"    "runs/run_$1/$2_LNS.csv" --max-iterations 1000 > "runs/run_$1/$2_LNS.out" 2>&1
    ./packing ALNS "problems/problem$2.csv" "runs/run_$1/$2_ALNS.txt"   "runs/run_$1/$2_ALNS.csv" --max-iterations 1000 > "runs/run_$1/$2_ALNS.out" 2>&1
    ./packing LNS  "problems/problem$2.csv" "runs/run_$1/$2_LNS_A.txt"  "runs/run_$1/$2_LNS_A.csv" --max-iterations 1000 --annealing > "runs/run_$1/$2_LNS_A.out" 2>&1
    ./packing ALNS "problems/problem$2.csv" "runs/run_$1/$2_ALNS_A.txt" "runs/run_$1/$2_ALNS_A.csv" --max-iterations 1000 --annealing > "runs/run_$1/$2_ALNS_A.out" 2>&1
}

# For loop
for problem in {3..4}
do
    for run in {1..10}
    do
            sleep 1
            run_experiments $run $problem &
    done
    wait
done