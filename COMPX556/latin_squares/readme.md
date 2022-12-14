# Usage

[Ensure rust and cargo are installed](https://doc.rust-lang.org/cargo/getting-started/installation.html). Then run the application using cargo.

```
cargo run -- --help
```
```
cargo run -- solve 0.1 30 data/benchmarks/Medium.json
```

## Methodology
 - Squares are scored by counting the number of duplicates (or missing values) 
   in each row/column. A score of 0 represents a perfect latin square.
 - Grasp iterations are stopped after 30s if no solution is found

## Easy Benchmark
50% 8x8 Latin Square
```
05  .  . 02 03  .  .  . 

04 07  . 05 02 06  . 03 

 .  .  .  .  . 00 01  . 

 . 00  . 07  . 01  .  . 

 . 01 05 06 07  . 02 04 

03  . 07  . 00  .  . 06 

02 05  . 03  . 04  . 00 

01 03 04 00  .  . 05 07

Score: 58
```

This easy benchmark is trivially solved in about 91 iterations.


## Medium Benchmark
80% of a 15x15 Latin Square
```
07 10 12 09 06 02 00  . 04 13 01 11 05  . 03 

02 01 11 12 07 04 09 05 13 06 14 08 03 00 10 

11 02 01 10 12  . 03  . 00 09 04  .  . 05 07 

03 09 06  . 05 10 04 11 01 14 12  . 08 02 00 

08 04 14 01 11 00 10 06 09 12 13 05 07 03 02 

04 14 08  . 02  .  .  . 06  .  . 00 10  . 01 

 . 13 05 14  . 09 01 07 12 11 06 03 02 10 04 

14 08 04  .  . 05  . 09 03 10 00 13 12 06 11 

01  .  . 07 10  .  . 00  . 03 08 04 09 13  . 

 . 00 13 04 14 03 02 12  . 01 09 06 11 07  . 

12 07  . 03 09 11 05  . 08 00 02 01 13  . 06 

09  .  .  . 00 12 14  .  . 08  . 10 04  . 13 

13  . 00  . 04 06 11 10 07 02  . 09 01 12  . 

10 12 07  . 03 01 13 08 14 05 11 02  . 04 09 

06 03  .  .  . 07 08  . 02 04  . 12 14 11  .

Score: 102
```

Scored 4 in 2986 iterations (30s).

## Very Hard Benchmarks

50% of a 20x20 latin square

```
 .  . 13 11 03  .  . 07  .  .  . 10  .  . 17  .  . 15  . 01 

09 16 02  .  .  . 18  .  .  .  .  . 08 06  .  . 05  .  . 07 

12  .  .  . 05  .  .  . 01 10 11  . 03 02 19 18  .  .  . 00 

 . 08  . 14 06  . 16  . 19  . 10  .  .  . 07 05  . 11 18  . 

17  . 07  . 01 09 15 18  .  . 03  .  .  . 16  . 04  . 11  . 

 .  . 01  .  .  . 00 08  .  . 16 18  . 15  . 07  .  . 19  . 

 . 05  . 15 18 00 12 17 10 11  . 04  .  . 01  . 13 19  .  . 

 .  . 15 03 00 16 07 02 08 06 05 12  . 10 09 14  . 18 04  . 

11 04  .  .  .  .  . 12 18  .  .  .  .  .  .  . 01  .  . 02 

 . 00 17 02 14  .  . 16  . 05  . 03 10  .  . 04 07  .  . 12 

 .  . 18  . 08  . 02  . 07  . 01  .  .  . 11  . 03  . 05  . 

 .  . 11  .  .  .  .  .  .  .  . 08  .  . 02 01 14  . 10  . 

 . 03 12  .  .  . 06  .  .  .  . 11  . 09  .  . 08  .  . 10 

10  .  .  . 04  . 01 13  . 18 09  .  .  .  .  . 19  .  . 03 

 .  .  .  .  . 07 09 11  .  .  . 01 06 05 15 03 18  .  .  . 

18 02 03  . 16 10 05 01  .  . 17  .  .  .  . 13 06 00 12  . 

 .  . 05  .  .  . 03  .  . 07 19  .  . 13 10  .  .  .  .  . 

00 01 19  .  .  .  . 09  . 03 02 05 14  . 13  .  .  .  . 06 

04 11 10  .  .  . 14  . 02  . 13  .  .  . 03  .  .  .  .  . 

 . 15 04 12  . 02  . 03 09 08  .  . 19 01  . 00 10  .  .  . 

Score: 436
```

Scored 40 in 285 iterations (30s).