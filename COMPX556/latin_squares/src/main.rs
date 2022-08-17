// #!feature(test)
use clap::{Parser, Subcommand};
mod grasp;
use grasp::square::Square;

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
        out_filename: String,

    },
}

fn main() {
    let cli = Cli::parse();
    match &cli.command {
        Commands::Score { filename } => {
            let square = Square::from_json(&filename);
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());
        }
        Commands::Partial { proportion, in_filename, out_filename } => {
            let square = Square::from_json(in_filename);
            let partial_square = square.make_partial(*proportion);
            println!("{}", partial_square);
            println!("Score: {} (0 is a valid latin square)", partial_square.score_square());
            partial_square.to_json(out_filename);
        }
    }
}