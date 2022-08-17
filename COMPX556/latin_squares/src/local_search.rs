use crate::square::Square;

pub fn local_search(square: &Square) -> Square {
    let mut square = square.clone();
    let mut best_square = square.clone();
    let mut best_score = square.score_square();

    let mut improvement = true;
    let n = square.size;
    let half_n = n / 2;
    println!("Iterations {}", n.pow(4)/2);
    while improvement {
        improvement = false;

        for (i, j, swap_row) in iproduct!(0..half_n, half_n..n, [true, false]) {
            if swap_row {
                square.swap_row(i, j);
            } else {
                square.swap_col(i, j);
            }


            let score = square.score_square();
            if score < best_score {
                best_square = square.clone();
                best_score = score;
                improvement = true;
            }

            if swap_row {
                square.swap_row(i, j);
            } else {
                square.swap_col(i, j);
            }
        }

        // for (i, ii, j, jj) in iproduct!(0..half_n, 0..half_n, half_n..n, half_n..n) {

        //     square.swap(i, j, ii, jj);
        //     let score = square.score_square();

        //     if score < best_score {
        //         println!("Improvement {}", score);
        //         best_square = square.clone();
        //         best_score = score;
        //         improvement = true;
        //     }

        //     // Swap back
        //     square.swap(i, j, ii, jj);
        // }
        square = best_square.clone();
    }
    return square;
}