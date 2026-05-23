"""
This module provides functions for visualizing persistent homology results,
including persistence barcodes and persistence diagrams.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib as mpl


def plot_persistence_barcode(
    barcodes: Dict[str, List[List[float]]],
    title: str = "Persistence Barcode",
    max_epsilon: float = 5.0,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    dpi: int = 300,
    legend_loc: str = "upper right",
    legend_fontsize: Optional[float] = None,
):
    """
    Plot persistence barcode for multiple dimensions with gradient fills.

    Args:
        barcodes: Dictionary mapping dimension names (e.g., 'H0', 'H1') to lists of [birth, death] pairs.
        title: Title of the plot.
        max_epsilon: Maximum value for the x-axis (epsilon).
        figsize: Size of the figure.
        save_path: Path to save the plot. If None, the plot is displayed.
        dpi: DPI for the saved plot.
        legend_loc: Legend position. Matplotlib loc string: 'upper right', 'upper left',
            'lower left', 'lower right', 'right', 'center left', 'center right',
            'lower center', 'upper center', 'center'; or (x, y) in axes coords (0-1).
        legend_fontsize: Legend font size (e.g. 10, 12). If None, use matplotlib default.
    """
    # Premium colors
    COLORS = {
        'H0': '#5DADE2',  # Soft Blue
        'H1': '#E74C3C',  # Soft Red
        'H2': '#58D68D',  # Soft Green
        'other': '#AF7AC5' # Soft Purple
    }
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Sort dimensions for consistent plotting
    dims = sorted(barcodes.keys())
    
    current_y = 0
    
    # Custom color generator if needed
    try:
        cmap = plt.cm.get_cmap("tab10")
    except Exception:
        cmap = mpl.colormaps["tab10"]
    
    for i, dim in enumerate(dims):
        intervals = barcodes[dim]
        # Determine base color
        if dim in COLORS:
            base_color_hex = COLORS[dim]
        elif f"H{i}" in COLORS:
            base_color_hex = COLORS[f"H{i}"]
        else:
            base_color_hex = mpl.colors.to_hex(cmap(i))
            
        base_rgb = mpl.colors.to_rgb(base_color_hex)
        
        # Sort intervals by birth time, then by death time
        intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
        
        for birth, death in intervals:
            # Handle infinite death time
            if death == float('inf'):
                death = max_epsilon
            
            # Clip death to max_epsilon for visualization
            death = min(death, max_epsilon)
            
            if death <= birth:
                continue
                
            # Create gradient data: (1, N, 4) array (RGBA)
            # Gradient transparency from 0.9 to 0.4
            width_px = 100
            gradient = np.linspace(0.9, 0.3, width_px).reshape(1, -1)
            
            # Construct RGBA image
            # Shape (1, width_px, 4)
            img_data = np.zeros((1, width_px, 4))
            img_data[:, :, 0] = base_rgb[0] # R
            img_data[:, :, 1] = base_rgb[1] # G
            img_data[:, :, 2] = base_rgb[2] # B
            img_data[:, :, 3] = gradient    # Alpha
            
            # Show gradient bar
            # Extent: [left, right, bottom, top]
            ax.imshow(
                img_data, 
                aspect='auto', 
                extent=[birth, death, current_y - 0.4, current_y + 0.4],
                origin='lower'
            )
            
            current_y += 1
            
        # Add a small gap between dimensions
        current_y += 1
        
    ax.set_xlabel("Distance Threshold ($\\epsilon$)", fontsize=12)
    ax.set_ylabel("Bars", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold', color='#2C3E50')
    ax.set_yticks([])  # Hide y-axis ticks
    
    # Custom Grid
    ax.grid(True, axis='x', linestyle='--', alpha=0.5, color='#EAEDED')
    ax.set_xlim(0, max_epsilon)
    ax.set_ylim(-1, current_y)
    
    # Keep all spines for outer border
    for spine in ax.spines:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('#BDC3C7')
    
    # Create a custom legend
    from matplotlib.lines import Line2D
    legend_elements = []
    for i, dim in enumerate(dims):
        if dim in COLORS:
            c = COLORS[dim]
        elif f"H{i}" in COLORS:
            c = COLORS[f"H{i}"]
        else:
            c = cmap(i)
        legend_elements.append(Line2D([0], [0], color=c, lw=4, label=dim, alpha=0.8))
        
    legend_kw = {"handles": legend_elements, "loc": legend_loc, "frameon": False}
    if legend_fontsize is not None:
        legend_kw["fontsize"] = legend_fontsize
    ax.legend(**legend_kw)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        svg_path = Path(save_path).with_suffix('.svg')
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_persistence_diagram(
    barcodes: Dict[str, List[List[float]]],
    title: str = "Persistence Diagram",
    max_epsilon: float = 5.0,
    figsize: Tuple[int, int] = (8, 8),
    save_path: Optional[str] = None,
    dpi: int = 300,
    legend_loc: str = "lower right",
    legend_fontsize: Optional[float] = None,
):
    """
    Plot persistence diagram (Birth vs Death) for multiple dimensions.

    Args:
        barcodes: Dictionary mapping dimension names (e.g., 'H0', 'H1') to lists of [birth, death] pairs.
        title: Title of the plot.
        max_epsilon: Maximum value for the x-axis and y-axis.
        figsize: Size of the figure.
        save_path: Path to save the plot. If None, the plot is displayed.
        dpi: DPI for the saved plot.
        legend_loc: Legend position (same options as plot_persistence_barcode).
        legend_fontsize: Legend font size (e.g. 10, 12). If None, use matplotlib default.
    """
    plt.figure(figsize=figsize)
    
    dims = sorted(barcodes.keys())
    try:
        colors = plt.cm.get_cmap("tab10")
    except Exception:
        colors = mpl.colormaps["tab10"]
    
    for i, dim in enumerate(dims):
        intervals = np.array(barcodes[dim])
        if len(intervals) == 0:
            continue
            
        births = intervals[:, 0]
        deaths = intervals[:, 1]
        
        # Replace infinity with max_epsilon for visualization
        deaths = np.where(np.isinf(deaths), max_epsilon, deaths)
        
        plt.scatter(births, deaths, color=colors(i), label=dim, alpha=0.7, edgecolors='white', s=50)
        
    # Plot diagonal line (birth = death)
    plt.plot([0, max_epsilon], [0, max_epsilon], 'k--', alpha=0.5)
    
    plt.xlabel("Birth ($\\epsilon$)", fontsize=12)
    plt.ylabel("Death ($\\epsilon$)", fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlim(0, max_epsilon)
    plt.ylim(0, max_epsilon)
    plt.grid(True, linestyle='--', alpha=0.6)
    legend_kw = {"loc": legend_loc}
    if legend_fontsize is not None:
        legend_kw["fontsize"] = legend_fontsize
    plt.legend(**legend_kw)
    
    # Keep all spines for outer border
    ax = plt.gca()
    for spine in ax.spines:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('#BDC3C7')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        svg_path = Path(save_path).with_suffix('.svg')
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()
    else:
        plt.show()
