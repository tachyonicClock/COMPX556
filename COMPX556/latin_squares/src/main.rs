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
    GenSquare {
        /// Size of the square
        #[clap(value_parser)]
        order: usize,
    },
}

fn main() {
    let cli = Cli::parse();
    match &cli.command {
        Commands::GenSquare { order } => {
            println!("Generating {}x{} latin square:", order, order);

            let square = Square::new(*order);

            println!("{}", square);
        }
    }
}