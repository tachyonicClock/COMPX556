use json;
use std::fmt;
use std::io::{Read, Write};

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
pub enum SquareItem {
    Empty,
    Treatment(u32),
}

#[derive(Clone)]
/// A square of symbols. Can contain latin squares.
pub struct Square {
    pub data: Vec<Vec<SquareItem>>,
    pub size: usize,
}

impl Square {
    /// Create empty square
    pub fn new(size: usize) -> Square {
        let mut square = Square {
            data: Vec::new(),
            size: size,
        };
        // Resize the square to the correct size
        square.data.resize(size, Vec::new());
        square.data.iter_mut().for_each(|v| v.resize(size, SquareItem::Empty));
        return square;
    }

    /// Create square from json file
    pub fn from_json(filename: &str) -> Square {
        // Load from json
        let mut file = std::fs::File::open(filename).expect("File not found");
        let mut contents = String::new();
        file.read_to_string(&mut contents).expect("Could not read file");
        let json_data = json::parse(&contents).expect("Could not parse json");

        let mut square = Square::new(json_data.len());
        for i in 0..json_data.len() {
            for j in 0..json_data.len() {
                match &json_data[i][j] {
                    json::JsonValue::Number(n) => {
                        let n: f32 = (*n).into();
                        square.data[i][j] = SquareItem::Treatment(n as u32);
                    }
                    json::JsonValue::Short(s) if s == "Empty" => {
                        square.data[i][j] = SquareItem::Empty;
                    }
                    _ => {
                        panic!("Json contains unexpected data for a latin square");
                    }
                }
            }
        }
        return square;
    }

    /// Save square to json file
    pub fn to_json(&self, filename: &str) {
        let json_string = json::stringify(self.data.clone());
        let mut file = std::fs::File::create(filename).expect("Could not create file");
        file.write_all(json_string.as_bytes()).expect("Could not write to file");
    }

    /// Score square ensures that the square is a valid latin square
    pub fn score_square(&self) -> u32 {
        let mut duplicates = 0;
        for row in 0..self.size {
            duplicates += self.check_row(row);
        }
        for col in 0..self.size {
            duplicates += self.check_col(col);
        }
        return duplicates;
    }

    /// Create a partial square from a complete square
    pub fn make_partial(&self, proportion: f32) -> Square {
        if proportion < 0.0 || proportion > 1.0 {
            panic!("Proportion must be between 0 and 1");
        }
        
        let mut partial_square = self.clone();

        // Remove items with certain probability
        for row in 0..self.size {
            for col in 0..self.size {
                if rand::random::<f32>() < proportion {
                    partial_square.data[row][col] = SquareItem::Empty;
                }
            }
        }

        return partial_square;
    }

    pub fn swap(&mut self, row1: usize, col1: usize, row2: usize, col2: usize) {
        let temp = self.data[row1][col1];
        self.data[row1][col1] = self.data[row2][col2];
        self.data[row2][col2] = temp;
    }

    pub fn swap_row(&mut self, row1: usize, row2: usize) {
        for col in 0..self.size {
            self.swap(row1, col, row2, col);
        }
    }

    pub fn swap_col(&mut self, col1: usize, col2: usize) {
        for row in 0..self.size {
            self.swap(row, col1, row, col2);
        }
    }


    /// Check a row for duplicates
    fn check_row(&self, row: usize) -> u32 {
        let mut exists = vec![false; self.size];
        
        for col in 0..self.size {
            let value = self.data[row][col];
            match value {
                SquareItem::Empty => {},
                SquareItem::Treatment(value) => {
                    exists[value as usize] = true;
                }
            }
        }
        // Count the number of false values in the vector
        return exists.iter().filter(|&x| !x).count() as u32;
    }
    
    /// Check a column for duplicates
    fn check_col(&self, col: usize) -> u32 {
        let mut exists = vec![false; self.size];
        for row in 0..self.size {
            let value = self.data[row][col];
            match value {
                SquareItem::Empty => {},
                SquareItem::Treatment(value) => {
                    exists[value as usize] = true;
                }
            }
        }
        // Count the number of false values in the vector
        return exists.iter().filter(|&x| !x).count() as u32;
    }
}

// Pretty print the square
impl std::fmt::Display for Square {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for i in 0..self.size {
            for j in 0..self.size {
                match self.data[i][j] {
                    SquareItem::Empty => write!(f, " . ")?,
                    SquareItem::Treatment(value) => write!(f, "{:02} ", value)?,
                }
            }
            write!(f, "\n\n")?;
        }
        return f.write_str("");
    }
}

impl From<SquareItem> for json::JsonValue {
    fn from(item: SquareItem) -> json::JsonValue {
        match item {
            SquareItem::Empty => json::JsonValue::String("Empty".to_string()),
            SquareItem::Treatment(value) => json::JsonValue::Number(value.into()),
        }
    }
}




#[cfg(test)]
pub mod tests {
    use rand::Rng;

    macro_rules! project_path {
        ($filename:expr) => {
            concat!(env!("CARGO_MANIFEST_DIR"), "/", $filename)
        };
    }

    pub const COMPLETE_SQUARES: [&'static str;6] = [
        project_path!("/data/complete/LatinSquare05.json"),
        project_path!("/data/complete/LatinSquare08.json"),
        project_path!("/data/complete/LatinSquare10.json"),
        project_path!("/data/complete/LatinSquare15.json"),
        project_path!("/data/complete/LatinSquare20.json"),
        project_path!("/data/complete/LatinSquare50.json"),
    ];

    #[test]
    fn score_complete_squares() {
        for filename in COMPLETE_SQUARES.iter() {
            let square = super::Square::from_json(&filename);
            assert_eq!(square.score_square(), 0);
        }
    }

    #[test]
    fn score_empty_square() {
        let square = super::Square::new(5);
        assert_eq!(square.score_square(), 50);
    }

    #[test]
    fn score_bad_square() {
        let n = 10;
        let mut rng = rand::thread_rng();

        for filename in COMPLETE_SQUARES.iter() {
            println!("{}", filename);
            let mut square = super::Square::from_json(&filename);
            // Randomly swap n elements
            for _ in 0..n {
                let i = rng.gen_range(0..square.size);
                let j = rng.gen_range(0..square.size);
                square.data[i][j] = super::SquareItem::Treatment(rng.gen_range(0..square.size) as u32);
            }
            assert_ne!(square.score_square(), 0);
        }
    }
}