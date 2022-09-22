import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import gp

class Square():
    """A square"""
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def split(self):
        """Split the square into four equal squares"""
        return [
            Square(self.x, self.y, self.width/2, self.height/2),
            Square(self.x + self.width/2, self.y, self.width/2, self.height/2),
            Square(self.x, self.y + self.height/2, self.width/2, self.height/2),
            Square(self.x + self.width/2, self.y + self.height/2, self.width/2, self.height/2)
        ]

    def center(self):
        """Return the center of the square"""
        return (self.x + self.width/2, self.y + self.height/2)

def _recursive_plot(ax, gene: gp.Gene, square: Square):
    """Recursively plot the gene"""
    if isinstance(gene, gp.Quadrant):
        plot_quadrant(gene, square)
        for child, child_square in zip(gene.children, square.split()):
            _recursive_plot(ax, child, child_square)
    elif isinstance(gene, gp.Bunker):
        # Plot square
        ax.add_patch(Rectangle((square.x, square.y), 3, 3))
        for child, child_square in zip(gene.children, Square(square.x, square.y, 3, 3).split()):
            _recursive_plot(ax, child, child_square)

    else:
        plt.text(*square.center(), str(gene), ha="center", va="center")

def plot_quadrant(quadrant: gp.Quadrant, square: Square):
    plt.vlines(square.x + square.width/2, square.y, square.y + square.height)
    plt.hlines(square.y + square.height/2, square.x, square.x + square.width)


def plot_gene(gene: gp.Gene):
    """Plot the gene"""
    fig, ax = plt.subplots(figsize=(8,8))
    plt.grid()
    _recursive_plot(ax, gene, Square(0, 0, 16, 16))
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_ylim(16, 0)
    ax.set_xlim(0, 16)
    plt.show()