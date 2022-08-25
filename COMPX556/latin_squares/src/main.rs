// #!feature(test)
use clap::{Parser, Subcommand};
#[macro_use] extern crate itertools;

mod square;
mod grasp;
mod local_search;
use crate::square::Square;

use local_search::local_search;

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
        Commands::Solve { alpha, in_filename, out_filename } => {
            let square = Square::from_json(in_filename, true);
            println!("======= BEFORE ======");
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());
            let square = grasp::greedy_randomized_construction(*alpha, &square);
            let square = grasp::repair(&square);
            println!("======= AFTER ======");
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());

            let square = local_search(&square);

            println!("======= AFTER LS ======");
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());

            

            if let Some(out_filename) = out_filename {
                println!("Saving to {}", out_filename);
                square.to_json(out_filename);
            }
        }
    }
}