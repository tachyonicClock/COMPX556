
## Bin Packing!


### Compile
```
make build
```

### Usage

```
Usage: ./packing <algorithm> <infile> <outfile> <log file> --max-iterations <num> --annealing
Algorithm can be one of:
  BL  - Bottom left heuristic
  LS  - Local Search
  LNS - Large neighbourhood search
  ALNS - Adaptive Large neighbourhood search
Outfile is the file to write the solution to.
Log file outputs results overtime
Max iterations is the maximum number of iterations to run for.
Annealing is a flag to enable simulated annealing.
```

```
Usage: renderer.py [OPTIONS]

Options:
  -i, --input TEXT      Input file  [required]
  -o, --output TEXT     Output file  [required]
  -h, --height INTEGER  Height of the image
  --help                Show this message and exit.
```

### Examples

Run bottom left heuristic
```
./packing BL problems/problem1.csv placements/1_BL.txt placements/1_BL.csv
python3 renderer.py -o placements/1_BL.png --height 50  -i placements/1_BL.txt
```

Run local search
```
./packing LS problems/problem1.csv placements/1_LS.txt placements/1_LS.csv
python3 renderer.py -o placements/1_LS.png --height 50  -i placements/1_LS.txt
```

Run large neighbourhood search
```
./packing LNS problems/problem1.csv placements/1_LNS.txt placements/1_LNS.csv
python3 renderer.py -o placements/1_LNS.png --height 50  -i placements/1_LNS.txt
```

Run adaptive large neighbourhood search with annealing
```
./packing ALNS problems/problem1.csv placements/1_ALNS_A.txt placements/1_ALNS_A.csv --max-iterations 5000 --annealing
python3 renderer.py -o placements/1_ALNS_A.png --height 50  -i placements/1_ALNS_A.txt
```