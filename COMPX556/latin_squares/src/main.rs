use clap::{Parser, Subcommand};
mod square;
use square::Square;

#[derive(Parser)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate a new latin square
    Validate {
        /// Size of the square
        #[clap(value_parser)]
        filename: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match &cli.command {
        Commands::Validate { filename } => {
            let square = Square::from_json(&filename);
            println!("{}", square);
            println!("Score: {} (0 is a valid latin square)", square.score_square());
        }
    }
}