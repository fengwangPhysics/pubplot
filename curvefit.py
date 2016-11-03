from scipy.optimize import curve_fit
import numpy as np

def curvefit(function, datax, datay, returnCov=False, **kwargs):
    """Curve fitting
    
    This function is almost exactly as `scipy.optimize.curve_fit`,
    except that it estimates the error of the fitting parameters.
    
    Parameters:
    -----------
    function: callable
        The model function, f(x,...). It must take the independent variable as the first argument and the parameters to fit as separate remaining arguments.
    datax: 1D array
        the independent variable
    datay: 1D array
        the independent variable
    returnCov: 1D array
        If True: return the covariance matrix of the fitting parameters.
    kwargs:
        Other keyword arguments to pass to `scipy.optimize.curve_fit`.
        The most useful ones are `p0` and `sigma`, for setting initial guessing and uncertainties of the `datay`.
        See https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.curve_fit.html
    
    Returns:
    --------
    popt: array
        Optimal values for the parameters
    error:
        1-sigma uncertainties of the fitting parameters `popt`.
    pcov: 2d array
        The estimated covariance of `popt`.
    """
    popt, pcov = curve_fit(function, datax, datay, **kwargs)
    error = []
    for i in xrange(len(popt)):
        try:
            error.append(np.sqrt(pcov[i][i]))
        except:
            error.append(0.0)
    if returnCov:
        return popt, error, pcov
    else:
        return popt, error
