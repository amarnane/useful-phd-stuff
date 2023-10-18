import matplotlib as mpl
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import pathlib
import palettable

from cycler import cycler

from .filesys import append_timestamp2path, create_dirs_on_path

science_figsize_dict = {
    # elsevier sizing https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions/artwork-sizing
    # givin in mm there, converted to inches cause matplotlib archaic.
    'single_col': [3.3, 2.5], # nature recommended
    'one_and_half_col': [5.3, 4.0], # same aspect ratio
    'double_col': [7.3, 5.5], # scaled using elseviers recommendations
}

science_figure_mplstyle = {
    # # Set color cycle
    # # Set line style as well for black and white graphs
    # 'axes.prop_cycle' : (cycler('color', ['k', 'r', 'b', 'g']) + cycler('ls', ['-', '--', ':', '-.'])),

    # Figure size
    'figure.figsize' : [3.3, 3.3],  # max width is 3.5 for single column, 5.5 for one and a half, 7.5 for double
    'figure.dpi':150,

    # Font sizes
    'axes.labelsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'font.size': 8,

    # # Font Family
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'Lucida Grande', 'DejaVu Sans', 'Verdana', 'Geneva', 'Lucid', 'Avant Garde', 'sans-serif'],

    # Set x axis
    'xtick.direction' : 'in',
    'xtick.major.size' : 3,
    'xtick.major.width' : 0.5,
    'xtick.minor.size' : 1.5,
    'xtick.minor.width' : 0.5,
    'xtick.minor.visible' : True,
    'xtick.top' : True,

    # Set y axis
    'ytick.direction' : 'in',
    'ytick.major.size' : 3,
    'ytick.major.width' : 0.5,
    'ytick.minor.size' : 1.5,
    'ytick.minor.width' : 0.5,
    'ytick.minor.visible' : True,
    'ytick.right' : True,

    # Set line widths
    'axes.linewidth' : 0.5,
    'grid.linewidth' : 0.5,
    'lines.linewidth': 1.,
    'lines.markersize': 3,

    # Always save as 'tight'
    'savefig.bbox' : 'tight',
    'savefig.dpi' : 300,
    'savefig.pad_inches' : 0.01,  # Use virtually all space when we specify figure dimensions
}

catplot_figure_mplstyle = {
    # # Set color cycle
    # # Set line style as well for black and white graphs
    # 'axes.prop_cycle' : (cycler('color', ['k', 'r', 'b', 'g']) + cycler('ls', ['-', '--', ':', '-.'])),

    # Figure size
    'figure.figsize' : [3.3, 3.3],  # max width is 3.5 for single column, 5.5 for one and a half, 7.5 for double
    'figure.dpi':150,

    # Font sizes
    'axes.labelsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'font.size': 8,

    # # Font Family
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'Lucida Grande', 'DejaVu Sans', 'Verdana', 'Geneva', 'Lucid', 'Avant Garde', 'sans-serif'],

    # Set x axis
    'xtick.direction' : 'out',
    'xtick.major.size' : 3,
    'xtick.major.width' : 0.5,
    'xtick.minor.size' : 1.5,
    'xtick.minor.width' : 0.5,
    'xtick.minor.visible' : False,
    'xtick.top' : False,

    # Set y axis
    'ytick.direction' : 'in',
    'ytick.major.size' : 3,
    'ytick.major.width' : 0.5,
    'ytick.minor.size' : 1.5,
    'ytick.minor.width' : 0.5,
    'ytick.minor.visible' : False,
    'ytick.right' : False,

    # Set line widths
    'axes.linewidth' : 0.5,
    'grid.linewidth' : 0.5,
    'lines.linewidth': 1.,
    'lines.markersize': 3,

    # Always save as 'tight'
    'savefig.bbox' : 'tight',
    'savefig.dpi' : 300,
    'savefig.pad_inches' : 0.01,  # Use virtually all space when we specify figure dimensions
}


colormaps = {
    'Prism_10':palettable.cartocolors.qualitative.Prism_10.mpl_colors,
    'Bold_10': palettable.cartocolors.qualitative.Bold_10.mpl_colors,
    'Vivid_10': palettable.cartocolors.qualitative.Vivid_10.mpl_colors,
    'Safe_10': palettable.cartocolors.qualitative.Safe_10.mpl_colors,
    'Antique_10': palettable.cartocolors.qualitative.Antique_10.mpl_colors,
    'Set1_9': palettable.colorbrewer.qualitative.Set1_9.mpl_colors,
    'Dark2_8': palettable.colorbrewer.qualitative.Dark2_8.mpl_colors,
    'Set3_12': palettable.colorbrewer.qualitative.Set3_12.mpl_colors,
    'Paired_12': palettable.colorbrewer.qualitative.Paired_12.mpl_colors,
}


def set_science_style(style_params=None, colorset='Vivid_10', linestyles=False):
    # colorsets: https://matplotlib.org/stable/tutorials/colors/colormaps.html
    if style_params in ['science', 'catplot']:
        style_dict = {'science':science_figure_mplstyle, 'catplot':catplot_figure_mplstyle}
        style_params = style_dict[style_params]
    elif style_params is None:
        style_params = science_figure_mplstyle

    if isinstance(colorset, list):
        colors = colorset

    if isinstance(colorset, str):
        if colorset in colormaps.keys():
            colors = colormaps[colorset]
        else:    
            colors = mpl.colormaps[colorset].colors
    
    if linestyles:
        lsset = [(0,()), (0, (5,5)), (0,(3,5,1,5)), (0,(1,1)), (0, (3,5,1,5,1,5)), (5,(10,3)), (0,(3,1,1,1,1,1)), (0, (2,5))]
        
        lslen = len(lsset)
        collen = len(colors)
        idx = min([lslen,collen])
        prop_cycle = mpl.rcsetup.cycler(color=colors[:idx], linestyle=lsset[:idx])
    else:
        prop_cycle = mpl.rcsetup.cycler(color=colors)

    style_params['axes.prop_cycle'] = prop_cycle
    mpl.rcParams.update(style_params)


def path_add_format_and_timestamp(name, folder, pformat, append_time=False):
    """Function to add suffix to a path to change its format and/or append timestamp. Used for saving matplotlib
    figures.

    Args:
        name (str or pathlib.Path): filename of figure (or file)
        folder (pathlib.Path): parent folder for path
        pformat (str): desired format
        append_time (bool, optional): append time to path aswell. Defaults to False.

    Returns:
        pathlib.Path: adjusted path
    """
    if append_time:
        name = append_timestamp2path(name)
    
    path = folder / (str(name) + '.' + pformat)
    return path

def save_mpl_figure(fig, savepath, svg=True, dpi=300, append_time=False, bbox_inches='tight',**kwargs):
    """Save a matplotlib figure as png (and svg). If savepath contains additional format 
    e.g. .pdf then 3 (or 2 if svg=False) copies are saved in different formats. savepath 
    should inlcude name + format. The parent directory for savepath does not need to exist, it
    will be created as part of function. Any additional plt.savefig keyword arguments are accepted (**kwargs argument) 


    
    Args:
        fig (plt.Figure): figure to save
        savepath (pathlib.Path): save path for figure. Should be filename with format e.g. path/to/myfigure.png
        svg (bool, optional): Flag to save svg or not. Defaults to True.
        dpi (int, optional): dpi for figure. Defaults to 300.
        bbox_inches (str, optional): set tight layout for figure before saving. in general improves visuals 
                            (but can cause problems if figure very complicated)
        append_time (bool, optional): add timestamp to save path. Defaults to False.
    """
    savepath = pathlib.Path(savepath)

    name = savepath.stem
    folder = savepath.parent
    
    format = savepath.suffix[1:] # suffix includes "." (.png rather than png)
                                # if empty [1:] doesn't raise error, '' accepts [1:]

    if not folder.exists():
        folder = create_dirs_on_path(folder)

    if svg:
        format_list = ['png', 'svg']
    else:
        format_list = ['png']

    if format and (format not in format_list): # check specified format in list
        format_list.append(format)

    for format in format_list:
        figpath = path_add_format_and_timestamp(name, folder, format, append_time=append_time)
        fig.savefig(figpath, bbox_inches=bbox_inches, dpi=dpi, **kwargs)
    
    return
    