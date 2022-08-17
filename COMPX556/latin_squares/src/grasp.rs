use rand::seq::SliceRandom;

pub mod square;

#[derive(Clone, Copy, PartialEq, Eq)]
pub struct Candidate {
    row: usize,
    col: usize,
    treatment: square::SquareItem,
}

impl Candidate {
    pub fn new(row: usize, col: usize, treatment: square::SquareItem) -> Candidate {
        Candidate {
            row: row,
            col: col,
            treatment: treatment,
        }
    }
}

/// Calculate the cost of a given candidate O(n)
pub fn incremental_cost(candidate: &Candidate, square: &square::Square) -> i32 {
    let mut cost = 0;

    // Look for duplicate in row
    for i in 0..square.size {
        cost += if square.data[candidate.row][i] == candidate.treatment {1} else {0};
        cost += if square.data[i][candidate.col] == candidate.treatment {1} else {0};
    }

    return cost;
}

/// Generate a vector of all possible candidates for a square
/// Runs in n^2 and generates approximately n^3 candidates (less when more of the
/// square is filled)
pub fn generate_candidate_ground_set(square: &square::Square) -> Vec<Candidate> {
    let mut candidates = Vec::new();
    for i in 0..square.size {
        for j in 0..square.size {
            if matches!(square.data[i][j], square::SquareItem::Empty) {
                for t in 0..square.size {
                    candidates.push(Candidate { row: i, col: j, treatment: square::SquareItem::Treatment(t as u32)});
                }
            }
        }
    }
    return candidates;
}

pub fn create_restricted_candidate_list(alpha: f32, candidates: &Vec<Candidate>, candidate_cost: &Vec<i32>) -> Vec<Candidate> {
    let min_cost = candidate_cost.iter().min().unwrap();
    let max_cost = candidate_cost.iter().max().unwrap();
    let threshold = min_cost + ((alpha*((max_cost-min_cost) as f32)) as i32);

    let mut candidate_list = Vec::new();
    for (i, candidate) in candidates.iter().enumerate() {
        if candidate_cost[i] <= threshold {
            candidate_list.push(*candidate);
        }
    }

    return candidate_list;
}

fn evaluate_candidates(candidates: &Vec<Candidate>, square: &square::Square) -> Vec<i32> {
    let mut candidate_cost = Vec::new();
    for candidate in candidates {
        candidate_cost.push(incremental_cost(candidate, square));
    }
    return candidate_cost;
}

/// Greedy randomized
pub fn greedy_randomized_construction(alpha: f32, square: &square::Square) -> square::Square {
    let mut rng = rand::thread_rng();
    let mut square = square.clone();

    // Initialize candidate set
    let mut candidates = generate_candidate_ground_set(&square);
    
    // While construction is possible
    while !candidates.is_empty() {
        // Evaluate the candidates
        let candidate_cost = evaluate_candidates(&candidates, &square);
        
        // Create a restricted candidate list
        let restricted_candidates = create_restricted_candidate_list(alpha, &candidates, &candidate_cost);

        // Pick a random candidate from the restricted candidate list
        let candidate = restricted_candidates.choose(&mut rng).unwrap();

        // Update treatment in square
        square.data[candidate.row][candidate.col] = candidate.treatment;
        
        // Update candidate set
        candidates.retain(|x| x.row != candidate.row && x.col != candidate.col);
    }

    return square;
}



#[cfg(test)]
mod tests {
    use crate::grasp::{square, Candidate};
    use std::time::{Duration, Instant};


    #[test]
    fn empty_ground_set() {
        for filename in square::tests::COMPLETE_SQUARES {
            let square = square::Square::from_json(&filename);
            let candidates = super::generate_candidate_ground_set(&square);
            assert_eq!(candidates.len(), 0);
        }
    }

    #[test]
    fn generate_ground_sets() {
        let proportion = 0.2;
        let delta  = 0.2;

        // This test is probabilistic so we only run it for large enough squares
        for filename in &square::tests::COMPLETE_SQUARES[4..] {
            let square = square::Square::from_json(&filename);
            let square = square.make_partial(proportion);

            let candidates = super::generate_candidate_ground_set(&square);

            println!("{} #candidates {}", filename, candidates.len());

            let expectation = ((square.size.pow(3)) as f32)*(proportion);

            assert!(candidates.len() as f32 > expectation - (expectation*delta), "Expected {} < {}", expectation, candidates.len());
            assert!(candidates.len() as f32 <= expectation + (expectation*delta), "Expected {} > {}", expectation, candidates.len());
        }
    }

    #[test]
    fn incremental_cost() {
        let mut square = square::Square::new(3);
        let candidate = super::Candidate { row: 0, col: 0, treatment: square::SquareItem::Treatment(0)};
        assert_eq!(super::incremental_cost(&candidate, &square), 0);
        square.data[0][1] = square::SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 1);
        square.data[1][0] = square::SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 2);
        square.data[2][0] = square::SquareItem::Treatment(0);
        square.data[0][2] = square::SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 4);
    }

    #[test]
    fn restricted_candidate_list() {
        let alpha = 0.2;
        // let candidate = super::Candidate { row: 0, col: 0, treatment: square::SquareItem::Treatment(0)};
        let mut candidates = Vec::new();
        for t in 0..10 {
            candidates.push(super::Candidate::new(0, 0, square::SquareItem::Treatment(t as u32)));
        }

        let candidate_cost = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].to_vec();
        let restricted_candidates = super::create_restricted_candidate_list(alpha, &candidates, &candidate_cost);
        assert_eq!(restricted_candidates.len(), 2);
        assert!(restricted_candidates.contains(&candidates[0]));
        assert!(restricted_candidates.contains(&candidates[1]));
    }

    #[test]
    fn greedy_randomized_construction() {
        let proportion = 0.5;


        for filename in &square::tests::COMPLETE_SQUARES[0..6] {
            let start = Instant::now();
            println!("{}", filename);
            let square = square::Square::from_json(&filename);
            let square = square.make_partial(proportion);
            let score = square.score_square();
            let square = super::greedy_randomized_construction(0.2, &square);
            let score_new = square.score_square();
            assert!(score_new < score, "Expected {} < {}", score_new, score);
            let duration = start.elapsed();
            println!("{:?}", duration);
        }
    }

}