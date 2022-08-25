use crate::square::{Square, SquareItem};


pub fn local_search(square: &Square) -> Square {
    let mut square = square.clone();
    let mut best_square = square.clone();
    let mut best_score = square.score_square();

    let mut improvement = true;
    let n = square.size;
    while improvement {
        improvement = false;

        for (i, j, k, use_rows) in iproduct!(0..n, 0..n/2, n/2..n, [true, false]) {
            let x = if use_rows {j} else {i};
            let xx = if use_rows {k} else {i};
            let y = if use_rows {i} else {j};
            let yy = if use_rows {i} else {k};

            if matches!(square.data[x][y], SquareItem::Frozen(_)) ||
               matches!(square.data[xx][yy], SquareItem::Frozen(_)) {
                continue;
            }

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
                    break
                }
            }
            square.swap(x, y, xx, yy);
        }
        square = best_square.clone();
    }
    return square;
}