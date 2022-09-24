import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gp
from gp.rectangle import  Rectangle




def _recursive_plot(ax, gene: gp.Gene, quad: Rectangle):
    """Recursively plot the gene"""
    if isinstance(gene, gp.Quadrant):
        plot_quadrant(gene, quad)
        for child, child_square in zip(gene.children, quad.quarters()):
            _recursive_plot(ax, child, child_square)
    elif isinstance(gene, gp.Bunker):
        # Plot square
        x, y = quad.center()
        x, y = (x-1.5, y-1.5)
        ax.add_patch(patches.Rectangle((x, y), 3, 3))
        for child, child_square in zip(gene.children, Rectangle(x, y, 3, 3).quarters()):
            _recursive_plot(ax, child, child_square)

    else:
        plt.text(*quad.center(), str(gene), ha="center", va="center")


def plot_quadrant(quadrant: gp.Quadrant, quad: Rectangle):
    plt.vlines(quad.x + quad.width/2, quad.y, quad.y + quad.height)
    plt.hlines(quad.y + quad.height/2, quad.x, quad.x + quad.width)


def plot_gene(gene: gp.Gene, save_file: str):
    """Plot the gene"""
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.grid()
    _recursive_plot(ax, gene, Rectangle(0, 0, 16, 16))
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_ylim(16, 0)
    ax.set_xlim(0, 16)
    plt.savefig(save_file)
