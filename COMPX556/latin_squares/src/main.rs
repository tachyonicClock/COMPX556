use std::time::Duration;

// #!feature(test)
use clap::{Parser, Subcommand};
#[macro_use] extern crate itertools;

mod square;
mod grasp;
mod local_search;
use crate::square::Square;

#[derive(Parser)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Print and score a latin square
    Score {
        #[clap(value_parser)]
        filename: String,
    },
    /// Turn a complete latin square into a partial latin square
    Partial {
        #[clap(value_parser)]
        proportion: f32,
        #[clap(value_parser)]
        in_filename: String,
        #[clap(value_parser)]
        out_filename: Option<String>,
    },
    /// Turn a complete latin square into a partial latin square
    Solve {
        #[clap(value_parser)]
        alpha: f32,
        #[clap(value_parser)]
        max_duration: f32,
        #[clap(value_parser)]
        in_filename: String,
        #[clap(value_parser)]
        out_filename: Option<String>,
    },
}

fn main() {
    let cli = Cli::parse();
    match &cli.command {
        Commands::Score { filename } => {
            let square = Square::from_json(&filename, true);
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());
        }
        Commands::Partial { proportion, in_filename, out_filename } => {
            let square = Square::from_json(in_filename, true);
            let partial_square = square.make_partial(*proportion);
            println!("{}", partial_square);
            println!("Score: {} (0 is a valid latin square)", partial_square.score_square());

            if let Some(out_filename) = out_filename {
                println!("Saving to {}", out_filename);
                partial_square.to_json(out_filename);
            }
        }
        Commands::Solve { alpha, in_filename, max_duration, out_filename } => {
            let square = Square::from_json(in_filename, true);
            let old_score = square.score_square() as f32;

            // float to duration
            let max_duration = Duration::from_secs_f32(*max_duration);
            let square = grasp::run_grasp(&square, *alpha, max_duration);
            let new_score = square.score_square() as f32;
            let percentage_change = (new_score - old_score) / old_score * 100.0;

            println!("{}", square);
            println!("Score: {} -> {} {}%", old_score, new_score, percentage_change);

            if let Some(out_filename) = out_filename {
                println!("Saving to {}", out_filename);
                square.to_json(out_filename);
            }
        }
    }
}