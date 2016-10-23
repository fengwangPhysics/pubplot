import matplotlib.pyplot as plt

rcParams = {'backend': 'pdf',
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 9,
    'lines.markersize': 3,
    'axes.titlesize': 9,
    'font.size': 9,
    'font.family': u'sans-serif',
    'font.sans-serif': ['Arial'],
    'text.usetex': False,
    'xtick.major.pad': 2,
    'ytick.major.pad': 2
}
plt.rcParams.update(rcParams)

class figure:
    """
    Main class, almost equivalent to plt.figure()
    """
    _FIGA4width = 210.25/25.4 # inches ~ 8.28inch
    _FIGmargin = 18./25.4 # left margin
    _FIGsep = 8./25.4 # middle column sep

    _FIGsingleWidth = (_FIGA4width - _FIGsep)/2. - _FIGmargin # ~3.27 inch
    _FIGdoubleWidth = _FIGA4width  - 2.*_FIGmargin # ~6.86 inch
    
    labelProp = {'fontweight': 'bold',
                'fontname': 'LiberationSerif',
                'va': 'top', 'ha': 'right', 'fontsize':9}


    def __init__(self, H=0.775, left=0.01, right=0.01, top=0.02, double=False, **kwargs):
        """
        Initialize `figure` class.
        
        Parameters
        ----------
            H : 
                the height of the figure, in unit of width
            left, right, top : optional
                margins of the figure, in unit of width (default: left, right 0.01, top 0.02)
            double : optional
                if True, use double column width as the figure width
            kwargs : optional
                other arguments passed to `plt.figure()`
        """
        if double:
            _FIGwidth = self._FIGdoubleWidth
        else: # single
            _FIGwidth = self._FIGsingleWidth
        self.H = H
        self.FIG = plt.figure(figsize=(_FIGwidth, _FIGwidth*H), **kwargs)
        self.axesList = []
        
        # margins
        self.left=left
        self.right=right
        self.top=top
        self.s = 1./(1.+self.left+self.right)

    
    def axes(self, xpos=0.1, ypos=0, W=0.9, H=0.675):
        """
        Add an `axes` class to the figure.
        The usage of `axes` is very similar to matplotlib, however, there are several
        differences:
         #. all units are in (figure width - left and right margins)
         #. origin is set at the upper left conner, rather than lower left as matplotlib
         #. the positive direction of y is downward 
        
        Parameters
        ----------
        xpos, ypos : optional
            set the position of the upper left conner of the axes, in unit of width
        W, H : optional
            set the width and height of the axes, in unit of width
        
        Returns
        -------
        ax
            `ax` class as same as matplotlib
        """
        ax = plt.axes([xpos*self.s+self.left, 1.-(ypos+H+self.top)/self.H, 
                       W*self.s, H/self.H])
        self.axesList.append(ax)
        return self.axesList[-1]

    def PanelLabel(self, label='(a)', pos=[(-0.07, 1.03)], prop=labelProp):
        """
        Add labels to the panels, commonly used for multipanel figures for publication
        
        Parameters
        ----------
        label:
            label style. E.g. for captical letters: use 'A'.
            Here is a guide for the usage for different journals:\n
            * PRL, PRB, PRE: '(a)'
            * Science: 'A'
            * Nature & its related journals: 'a'
            * PNAS: 'A'
        pos: array-like
            positions of the labels, in the unit of axes.
            If all positions of the labels are the same, just pass one coordinate,
            otherwise, a full list (length=number of axes) is needed.
        prop:
            extra properties for the label.
            see the full document in `plt.text()`
        
        See Also
        --------
        plt.text: matplotlib text
        """
        if 'a' in label:
            labels = [label.replace('a', letter) for letter in 'abcdefghijklmn']
        elif 'A' in label:
            labels = [label.replace('A', letter) for letter in 'ABCDEFGHIGKLMN']
        else:
            raise RuntimeError, "label pattern cannot be supported."
            
        if len(pos) == 1:
            pos = [pos[0] for i in self.axesList]
        #print pos
        
        for i, ax in enumerate(self.axesList):
            ax.text(pos[i][0], pos[i][1], labels[i], transform=ax.transAxes, **prop)


# Label line with line2D label data
from math import atan2,degrees
import numpy as np

def labelLine(line,x,label=None,align=True,**kwargs):
    """
    Label line with line2D label data (Low-level function)

    See Also
    --------
    labelLines: more user friendly function

    References
    ----------
    .. [1] http://stackoverflow.com/questions/16992038/inline-labels-in-matplotlib
    """
    ax = line.get_axes()
    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if (x < xdata[0]) or (x > xdata[-1]):
        print('x label location is outside data range!')
        return

    #Find corresponding y co-ordinate and angle of the
    ip = 1
    for i in range(len(xdata)):
        if x < xdata[i]:
            ip = i
            break

    y = ydata[ip-1] + (ydata[ip]-ydata[ip-1])*(x-xdata[ip-1])/(xdata[ip]-xdata[ip-1])

    if not label:
        label = line.get_label()

    if align:
        #Compute the slope
        dx = xdata[ip] - xdata[ip-1]
        dy = ydata[ip] - ydata[ip-1]
        ang = degrees(atan2(dy,dx))

        #Transform to screen co-ordinates
        pt = np.array([x,y]).reshape((1,2))
        trans_angle = ax.transData.transform_angles(np.array((ang,)),pt)[0]

    else:
        trans_angle = 0

    #Set a bunch of keyword arguments
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()

    if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
        kwargs['ha'] = 'center'

    if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
        kwargs['va'] = 'center'

    if 'backgroundcolor' not in kwargs:
        kwargs['backgroundcolor'] = ax.get_axis_bgcolor()

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = True

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 2.5

    ax.text(x,y,label,rotation=trans_angle,**kwargs)

def labelLines(ax, align=True, xvals=None, **kwargs):
    """
    Label line with line2D label data (user-level function)

    Parameters
    ----------
    ax:
        the `axes` class
    align: True, optional
        | If True, align the text along the line
        | If False, align the text horizontally
    xvals: None, optional
        The x position where the text appears
        If None, use `np.linspace(xmin,xmax,len(labLines)+2)[1:-1]`
    kwargs:
        other arguments for plt.text()

    See Also
    --------
        labelLine: low-level function

    References
    ----------
    .. [1] http://stackoverflow.com/questions/16992038/inline-labels-in-matplotlib
    """
    lines = ax.get_lines()
    labLines = []
    labels = []

    #Take only the lines which have labels other than the default ones
    for line in lines:
        label = line.get_label()
        if "_line" not in label:
            labLines.append(line)
            labels.append(label)

    if xvals is None:
        xmin,xmax = ax.get_xlim()
        xvals = np.linspace(xmin,xmax,len(labLines)+2)[1:-1]

    for line,x,label in zip(labLines,xvals,labels):
        labelLine(line,x,label,align,**kwargs)

def alignEndTickLabel(ax, which='y'):
    """align the two ends of the tick labels, to make them look better
      #. top: align `va` to "top"
      #. bottom: align `va` to "bottom"
      #. left: align `ha` to "left"
      #. right: align `ha` to "right"

    Parameters
    ----------
    ax:
        the `axes` class
    which: {'x', 'y'}, optional
        which axis to align
    """
    if which=='x':
        labels = ax.get_xticklabels()
        labels[0].set_horizontalalignment('left')
        labels[-1].set_horizontalalignment('right')
    elif which=='y':
        labels = ax.get_yticklabels()
        labels[0].set_verticalalignment('bottom')
        labels[-1].set_verticalalignment('top')
