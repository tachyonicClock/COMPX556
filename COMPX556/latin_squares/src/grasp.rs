use std::{collections::HashMap, hash::Hash, time::Duration};

use indicatif::{ProgressBar, ProgressStyle};
use rand::seq::SliceRandom;
use std::time::{SystemTime};
use crate::{square::{SquareItem, Square}, local_search::local_search};


/**
 * A candidate is a plausible element of a solution. In a Latin Square
 * this is a treatment in a specific cell.
 */
#[derive(Clone, Copy, PartialEq, Eq, Hash)]
pub struct Candidate {
    row: usize,
    col: usize,
    treatment: SquareItem,
}

// Cost measures the quality of a solution.
type Cost = u32;
// A set of all possible candidates and their cost
type CandidateSet = HashMap<Candidate, Cost>;

impl Candidate {
    /**
     * Create a new candidate.
     */
    pub fn new(row: usize, col: usize, treatment: SquareItem) -> Candidate {
        Candidate {
            row: row,
            col: col,
            treatment: treatment,
        }
    }
}

/**
 * Instead of calculating the entire cost of a solution, we can update the cost
 * of a solution by only looking at the cells that were affected by the change.
 * 
 * This is much faster than calculating the entire cost of a solution O(n)
 */
pub fn incremental_cost(candidate: &Candidate, square: &Square) -> Cost {
    let mut cost = 0;

    // Look for duplicates in row and column
    for i in 0..square.size {
        cost += if square.data[candidate.row][i] == candidate.treatment {1} else {0};
        cost += if square.data[i][candidate.col] == candidate.treatment {1} else {0};
    }

    return cost;
}


/**
 * Generate a vector of all possible candidates for a square
 * Runs in n^2 and generates approximately n^3 candidates (less when more of the
 * square is already filled)
 */
pub fn generate_candidate_ground_set(square: &Square) -> CandidateSet {
    let mut candidates = CandidateSet::new();

    // Naively generate all candidates
    for i in 0..square.size {
        for j in 0..square.size {
            if matches!(square.data[i][j], SquareItem::Empty) {
                for t in 0..square.size {
                    let treatment =  SquareItem::Treatment(t as u32);
                    candidates.insert(Candidate::new(i, j, treatment), u32::MAX);
                }
            }
        }
    }

    // Remove invalid candidates
    for i in 0..square.size {
        for j in 0..square.size {
            match square.data[i][j] {
                SquareItem::Empty => {},
                SquareItem::Frozen(t) => {
                    // Remove treatment as candidate from row and column
                    for k in 0..square.size {
                        candidates.remove(&Candidate::new(i, k, SquareItem::Treatment(t)));
                        candidates.remove(&Candidate::new(k, j, SquareItem::Treatment(t)));
                    }
                }
                SquareItem::Treatment(t) => {
                    // Remove treatment as candidate from row and column
                    for k in 0..square.size {
                        candidates.remove(&Candidate::new(i, k, SquareItem::Treatment(t)));
                        candidates.remove(&Candidate::new(k, j, SquareItem::Treatment(t)));
                    }
                }
            }
        }
    }
    return candidates;
}

/**
 * Returns a subset of the candidate ground set that are the best candidates.
 * alpha defines how strict the selection is. An alpha of 0.0 is the strictest
 * and will only return the best candidate. An alpha of 1.0 will return all
 * candidates.
 */
pub fn create_restricted_candidate_list(alpha: f32, candidates: &CandidateSet) -> Vec<Candidate> {

    let mut min_cost = Cost::MAX;
    let mut max_cost = Cost::MIN;
    for cost in candidates.values() {
        if *cost < min_cost {
            min_cost = *cost;
        }
        if *cost > max_cost {
            max_cost = *cost;
        }
    }

    let threshold = min_cost + ((alpha*((max_cost-min_cost) as f32)) as Cost);

    let mut candidate_list = Vec::new();
    for (candidate, score) in candidates {
        if *score <= threshold {
            candidate_list.push(*candidate);
        }
    }
    return candidate_list;
}

/**
 * Evaluate each candidate in the candidate set and set their cost.
 */
fn evaluate_candidates(candidates: &mut CandidateSet, square: &Square) {
    // Update candidate scores
    for (candidate, cost) in candidates.iter_mut() {
        *cost = incremental_cost(candidate, square);
    }
}

/**
 * Incrementally select candidates to add to a solution. The selection is
 * randomized but biased towards candidates with a lower cost.
 */
pub fn greedy_randomized_construction(alpha: f32, square: &Square) -> Square {
    let mut rng = rand::thread_rng();
    let mut square = square.clone();

    // Initialize candidate set
    let mut candidates = generate_candidate_ground_set(&square);
    evaluate_candidates(&mut candidates, &square);
    
    // While construction is possible
    while !candidates.is_empty() {
        
        // Create a restricted candidate
        let restricted_candidates = create_restricted_candidate_list(alpha, &candidates);
        
        // Pick a random candidate from the restricted candidate list
        let candidate = restricted_candidates.choose(&mut rng).unwrap();
        
        // Update treatment in square
        square.data[candidate.row][candidate.col] = candidate.treatment;
        
        // Update candidate set and update costs approx
        let mut to_remove = candidate.clone();
        for i in 0..square.size {
            let treatment = SquareItem::Treatment(i as u32);
            to_remove.treatment = treatment;
            candidates.remove(&to_remove);

            // Incrementally update the score
            let candidate_col = Candidate::new(candidate.row, i, candidate.treatment);
            let candidate_row = Candidate::new(i, candidate.col, candidate.treatment);
            candidates.get_mut(&candidate_col).map(|cost| *cost += 1);
            candidates.get_mut(&candidate_row).map(|cost| *cost += 1);
        }
    }

    return square;
}


/**
 * Attempt to replace a cell with the old treatment with the new treatment.
 */
pub fn replace_treatment(square: &mut Square, old_treatment: SquareItem, new_treatment: SquareItem) {
    let mut best_i = 0;
    let mut best_j = 0;
    let mut best_cost = Cost::MAX;

    for i in 0..square.size {
        for j in 0..square.size {
            if square.data[i][j] == old_treatment {
                square.data[i][j] = new_treatment;
                let cost = incremental_cost(&Candidate::new(i, j, new_treatment), square);
                if cost < best_cost {
                    best_i = i;
                    best_j = j;
                    best_cost = cost;
                }
                square.data[i][j] = old_treatment;
            }
        }
    }
    square.data[best_i][best_j] = new_treatment;
}

/**
 * A latin square only has hopes of being valid if and only if each treatment
 * exists n times in total.
 */
pub fn repair(square: &Square) -> Square {
    let mut square = square.clone();
    let mut counts = vec![0; square.size];
    
    // Count the number of each treatment in the square. There should be 
    // exactly n instances of each treatment. If not, repair the square.
    for i in 0..square.size {
        for j in 0..square.size {
            match square.data[i][j] {
                SquareItem::Treatment(t) => {
                    counts[t as usize] += 1;
                }
                SquareItem::Frozen(t) => {
                    counts[t as usize] += 1;
                }
                _ => {
                    panic!("Square should not be empty");
                }
            }
        }
    }

    // Replace the most common treatment with the least common treatment
    while !counts.iter().all(|&c| c == square.size) {
        let treatment_ranks = argsort(&counts);
        let least_common_treatment = treatment_ranks[0];
        let most_common_treatment = treatment_ranks[treatment_ranks.len()-1];

        replace_treatment(
            &mut square, 
            SquareItem::Treatment(most_common_treatment as u32), 
            SquareItem::Treatment(least_common_treatment as u32));

        counts[most_common_treatment] -= 1;
        counts[least_common_treatment] += 1;
    }


    return square;
}

/**
 * Perform randomized construction, repair, and local search.
 */
fn grasp_iteration(square: &Square, alpha: f32) -> Square {
    let mut square = greedy_randomized_construction(alpha, &square.clone());
    square = repair(&square);
    return local_search(&square);
}

/**
 * Perform Greedy Randomized Adaptive Search Procedures for a given max duration.
 */
pub fn run_grasp(square: &Square, alpha: f32, max_duration: Duration) -> Square {
    // Get start time to ensure we don't exceed max_duration
    let start_time = SystemTime::now();
    let mut best_square = grasp_iteration(&square, alpha);
    let mut best_score = square.score_square();
    let mut elapsed = start_time.elapsed().unwrap();
    let mut iterations = 1.0;
    let pb_len = 1000.0;

    let style = ProgressStyle::with_template("{bar:40.cyan/blue} {pos:>7}/{len:7} {msg}").unwrap();
    let pb = ProgressBar::new(pb_len as u64).with_message("GRASP").with_style(style);
    pb.println(format!("Running grasp for up to {:.2?} seconds", max_duration));

    while elapsed < max_duration && best_score != 0 {
        let square = grasp_iteration(&square, alpha);
        let score = square.score_square();
        iterations += 1.0;

        if score < best_score {
            best_square = square;
            best_score = score;
        }
        
        elapsed = start_time.elapsed().unwrap();
        
        let progress = elapsed.as_secs_f32()/max_duration.as_secs_f32();
        pb.set_position((progress * pb_len) as u64);
        pb.set_message(format!("Score: {}, {:.1} its/s", best_score, iterations/elapsed.as_secs_f32()));
    }

    println!("Finished after {:.0} iterations", iterations);

    return best_square;
}

/**
 * Argsort will return the indices that would sort a vector.
 */
pub fn argsort<T: Ord>(data: &[T]) -> Vec<usize> {
    let mut indices = (0..data.len()).collect::<Vec<_>>();
    indices.sort_by_key(|&i| &data[i]);
    return indices;
}



#[cfg(test)]
mod tests {
    use std::time::{Instant};
    use crate::square::{SquareItem, Square, tests};
    use crate::grasp::{CandidateSet, Cost, Candidate, repair};

    #[test]
    fn empty_ground_set() {
        for filename in tests::COMPLETE_SQUARES {
            let square = Square::from_json(&filename, true);
            let candidates = super::generate_candidate_ground_set(&square);
            assert_eq!(candidates.len(), 0);
        }
    }

    #[test]
    fn incremental_cost() {
        let mut square = Square::new(3);
        let candidate = super::Candidate { row: 0, col: 0, treatment: SquareItem::Treatment(0)};
        assert_eq!(super::incremental_cost(&candidate, &square), 0);
        square.data[0][1] = SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 1);
        square.data[1][0] = SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 2);
        square.data[2][0] = SquareItem::Treatment(0);
        square.data[0][2] = SquareItem::Treatment(0);
        assert_eq!(super::incremental_cost(&candidate, &square), 4);
    }

    #[test]
    fn restricted_candidate_list() {
        let alpha = 0.2;
        // let candidate = super::Candidate { row: 0, col: 0, treatment: SquareItem::Treatment(0)};
        let mut candidates = CandidateSet::new();
        for t in 0..10 {
            candidates.insert(Candidate::new(0, 0, SquareItem::Treatment(t as u32)), t as Cost);
        }

        let restricted_candidates = super::create_restricted_candidate_list(alpha, &candidates);
        assert_eq!(restricted_candidates.len(), 2);
        assert!(restricted_candidates.contains(&Candidate::new(0, 0, SquareItem::Treatment(0))));
        assert!(restricted_candidates.contains(&Candidate::new(0, 0, SquareItem::Treatment(1))));
    }

    #[test]
    fn greedy_randomized_construction() {
        let proportion = 0.5;


        for filename in &tests::COMPLETE_SQUARES[0..6] {
            let start = Instant::now();
            println!("{}", filename);
            let square = Square::from_json(&filename, true);
            let square = square.make_partial(proportion);
            let score = square.score_square();
            let square = super::greedy_randomized_construction(0.2, &square);
            let score_new = square.score_square();
            assert!(score_new < score, "Expected {} < {}", score_new, score);
            let duration = start.elapsed();
            println!("{:?}", duration);
            repair(&square);
        }
    }

}