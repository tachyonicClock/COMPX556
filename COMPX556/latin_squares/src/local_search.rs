use rand::Rng;

use crate::square::Square;


pub fn local_search(square: &Square) -> Square {
    let mut rng = rand::thread_rng();
    let mut square = square.clone();
    let mut best_square = square.clone();
    let mut best_score = square.score_square();

    let mut improvement = true;
    let n = square.size;
    let total = n.pow(3)/2;
    println!("Iterations {}", total);
    while improvement {
        improvement = false;

        for (i, j, k, use_rows) in iproduct!(0..n, 0..n/2, n/2..n, [true, false]) {
            let x = if use_rows {j} else {i};
            let xx = if use_rows {k} else {i};
            let y = if use_rows {i} else {j};
            let yy = if use_rows {i} else {k};

            let old_score = 
                square.check_col(x) + square.check_col(xx) + 
                square.check_row(y) + square.check_row(yy);

            square.swap(x, y, xx, yy);

            let new_score = 
                square.check_col(x) + square.check_col(xx) + 
                square.check_row(y) + square.check_row(yy);

            if new_score < old_score {
                let score = square.score_square();
                if score < best_score {
                    best_square = square.clone();
                    best_score = score;
                    improvement = true;
                    println!("Found improvement {}", best_score);
                    break
                }
            }
            square.swap(x, y, xx, yy);
        }

        // 4 Random numbers
        // for iter in 0..100_000 {
        //     let i = rng.gen_range(0..n/2);
        //     let ii = rng.gen_range(n/2..n);
        //     let j = rng.gen_range(0..n/2);
        //     let jj = rng.gen_range(n/2..n);

        //     let old_score = 
        //         square.check_col(j) + square.check_col(jj) + 
        //         square.check_row(i) + square.check_row(ii);

        //     // Swap the two numbers
        //     square.swap(i, j, ii, jj);

        //     let new_score = 
        //         square.check_col(j) + square.check_col(jj) + 
        //         square.check_row(i) + square.check_row(ii);

        //     if new_score < old_score {
        //         best_square = square.clone();
        //         best_score = square.score_square();
        //         improvement = true;
        //         println!("{} Improvement {}", iter, best_score);
        //         break;
        //     }

        //     square.swap(i, j, ii, jj);
        // }

        // for (i, ii, j, jj) in iproduct!(0..half_n, 0..half_n, half_n..n, half_n..n) {

        //     square.swap(i, j, ii, jj);

        //     // Swap back
        //     square.swap(i, j, ii, jj);
        // }
        square = best_square.clone();
    }
    return square;
}