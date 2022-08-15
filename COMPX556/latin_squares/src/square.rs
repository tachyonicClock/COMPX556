use std::fmt;

/// A square of symbols. Can contain latin squares.
pub struct Square {
    data: Vec<Vec<u32>>,
    size: usize
}


impl Square {
    /// Create empty square
    pub fn new(size: usize) -> Square {
        let mut square = Square {
            data: Vec::new(),
            size: size
        };
        // Resize the square to the correct size
        square.data.resize(size, Vec::new());
        square.data.iter_mut().for_each(|v| v.resize(size, 0));
        return square;
    }

    pub fn generate_latin_square(&mut self) {

    }
}

// Pretty print the square
impl std::fmt::Display for Square {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for i in 0..self.size {
            for j in 0..self.size {
                write!(f, "{:02}  ", self.data[i][j])?;
            }
            write!(f, "\n\n");
        }
        return f.write_str("");
    }
}