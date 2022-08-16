use json;
use std::fmt;
use std::io::Read;


/// A square of symbols. Can contain latin squares.
pub struct Square {
    data: Vec<Vec<u32>>,
    size: usize,
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
        square.data.iter_mut().for_each(|v| v.resize(size, 0));
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
                square.data[i][j] = json_data[i][j].as_u64().expect("Failed to load latin square") as u32;
            }
        }
        return square;
    }

    /// Check a row for duplicates
    fn check_row(&self, row: usize) -> u32 {
        let mut duplicates = 0;
        let mut exists = vec![false; self.size];
        
        for col in 0..self.size {
            let value = self.data[row][col];
            if exists[value as usize] {
                duplicates += 1;
            }
            exists[value as usize] = true;
        }
        return duplicates;
    }
    
    /// Check a column for duplicates
    fn check_col(&self, col: usize) -> u32 {
        let mut duplicates = 0;
        let mut exists = vec![false; self.size];
        
        for row in 0..self.size {
            let value = self.data[row][col];
            if exists[value as usize] {
                duplicates += 1;
            }
            exists[value as usize] = true;
        }
        return duplicates;
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
}

// Pretty print the square
impl std::fmt::Display for Square {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for i in 0..self.size {
            for j in 0..self.size {
                write!(f, "{:02}  ", self.data[i][j])?;
            }
            write!(f, "\n\n")?;
        }
        return f.write_str("");
    }
}
