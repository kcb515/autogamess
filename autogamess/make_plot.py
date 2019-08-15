from .config import *
from .get_data import get_data
from .data_finder import hessian
import matplotlib.pyplot as plt

def make_plot(file, savedir, cmap=['b', 'k', 'r', 'g', 'y', 'c']):
    """
    This function make vibrational frequency vs. IR/Raman intensity line plots.

    Parameters
    ----------
    file: string
        This should be a string that points to the log file of a hessian or
        Raman GAMESS(us) calculation. (FULL DIRECTORY STRING REQUIRED)
    savedir: string
        This should be a string that points to the directory in which you
        would like to save the png of the plot.(FULL DIRECTORY STRING REQUIRED)
    cmap: list [Optional]
        This should be a list of Matplotlib allowed color choices. Each symmetry
        will be plotted with a different color in the list.

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> file    = './AGv0-0-6_NH3_CCSD-T_CC6_hes.log'
    >>> savedir = './'
    >>>
    >>> ag.make_plot(file, savedir)
    >>>
    >>> cmap = ['b', 'r', 'k', 'c']
    >>> ag.make_plot(file, savedir, cmap)
    >>>
    """
    #variables declarations
    png  = '.png'

    #get data from file
    data  = get_data(file)

    #If hessian file, make Ir vs Vib Freq plot
    if '_hes' in file:
        ir = data.ir_inten
        vf = data.vib_freq

        #init plot plane
        fig, ax = plt.subplots()

        #iterate through data making lines
        i = 0
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ir[key])
            ax.vlines(x, 0, y, label=key, colors=cmap[i])
            i += 1

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_hes.log', '_ir-plot')

        #Add titles to plot then save
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Infrared Intensity $(Debey^2 \cdot \AA^{-2} \cdot amu^{-\frac{1}{2}})$')
        plt.title(title, fontsize=20)
        plt.savefig(savedir + name + png)

    #If raman file, make Raman vs Vib Freq plot
    if '_raman' in file:
        ra = data.raman
        vf = hessian(file)[0]

        #init plot plane
        fig, ax = plt.subplots()

        #iterate through data making lines
        i = 0
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ra[key])
            ax.vlines(x, 0, y, label=key, colors=cmap[i])
            i += 1

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_raman.log', '_raman-plot')

        #Add titles to plot then save
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Raman Intensity $(\AA^{4}\cdot mol^{-1})$')
        plt.title(title, fontsize=20)
        plt.savefig(savedir + name + png)

    return
