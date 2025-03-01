
import math
import numpy as np


def gaussian_2d(xy_dim, xy_sigma):
    """ Generates a 2D Gaussian PSF
    
    Parameters:
    ----------
        xy_dim (int): the size of the PSF in the xy plane
        xy_sigma (float): the sigma of the Gaussian in the xy plane in pixels
    Returns:
    -------
        psf (numpy array): the PSF
    """
    muu = 0.0
    gauss = np.empty([xy_dim,xy_dim])
    x_, y_ = np.meshgrid(np.linspace(-(xy_dim//2),xy_dim//2,xy_dim), np.linspace(-(xy_dim//2),xy_dim//2,xy_dim))
    for x in range(xy_dim):
        for y in range(xy_dim):
            tx=x_[y,x]
            ty=y_[y,x]
            
            gauss[y,x]=np.exp(-( (tx-muu)**2 / ( 2.0 * xy_sigma**2 ) ) )*np.exp(-( (ty-muu)**2 / ( 2.0 * xy_sigma**2 ) ) )

    #gauss=gauss+0.000000000001
    gauss=gauss/gauss.sum()

    return gauss

def pad(img, paddedsize, mode, constant_values=0):
    """ pad image to paddedsize

    Args:
        img ([type]): image to pad 
        paddedsize ([type]): size to pad to 
        mode ([type]): one of the np.pad modes

    Returns:
        padded [nd array]: padded image
        padding [tuple]: tuple containing the padding used
    """
    padding = tuple(map(lambda i,j: ( math.ceil((i-j)/2), math.floor((i-j)/2) ),paddedsize,img.shape))

    if mode == 'constant':
        return np.pad(img, padding,mode, constant_values=constant_values), padding
    else:
        return np.pad(img, padding,mode), padding

import numpy as np
import math

def handle_prime(p,x,a):
    log = math.log(p)
    power=p

    while power <= x + a.shape[0]:
        j=x%power
        if j>0:
            j=power-j

        while j < a.shape[0]:
            a[j]+=log
            j+=power

        power*=p
    

def next_smooth(x):
    """[summary]
    author Johannes Schindelin
    author Brian Northan

    A class to determine the next smooth number (a number divisable only)
    by prime numbers up to k (in this case we fix k at 7).
    
    Based on A. Granville, Finding smooth numbers computationally.
    
    Args:
        x ([type]): number to test

    Returns:
        [type]: next smooth number larger than x
    """
    z = int(10*math.log2(x))
    delta = 0.000001

    a = np.zeros(z)

    handle_prime(2,x,a)
    handle_prime(3,x,a)
    handle_prime(5,x,a)
    handle_prime(7,x,a)

    log = math.log(x)
    for i in range(a.shape[0]):
        if a[i] >=log-delta:
            return x+i

    return -1

def get_next_smooth(size):
    """ for an nd tuble compute the next smooth size for each element

    Args:
        size ([type]): nd input tuple 

    Returns:
        [type]: tuple containing the next smooth size for each input element
    """
    return tuple(map(lambda i: next_smooth(i), size))


