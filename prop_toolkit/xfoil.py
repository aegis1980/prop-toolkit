"""
Modified from here

https://gist.github.com/helo9/9954e836b470f267bf5b5825f9ff2a50

"""

import os

import subprocess as sp
import re

import numpy as np

from prop_toolkit import XFOIL699_PATH,TEMP_PATH


def run_xfoil(in_file,re, polar_file = None,*args,**kwargs):
    """calculate airfoil polar and load results
    
    Parameters
    ----------
    afile: string
        path to aifoil dat file
    re: float
        fixed reynoldsnumber for polar calculation
    *args, **kwargs
        have a look at calcpolar for further information
        
    Returns
    -------
    dict
        airfoil polar
    """
    temp = False
    if not polar_file:
        polar_file = os.path.join(TEMP_PATH, "temp.dat")
        temp = True                          
                                
    
    calc_polar(in_file, polar_file,re, *args, **kwargs)
    data = read_polar(polar_file)
    
    if temp:
        _delete_polar(polar_file)

    return data


def calc_polar(afile:str, polarfile:str,re : float, a_start = -45, a_end=45, a_step=5, refine=True, max_iter=200, n=None):
    """run xfoil to generate polar file
    
    Parameters
    ----------
    afile: string
        path to airfoil dat file
    re: float
        fixed reynoldsnumber
    alfaseq: iterateable, optional
        sequence of angles of attack
    clseq: iterateable, optional
        sequence of lift coefficients (either those or alfaseq must be defined)
    refine: bool
        shall xfoil refine airfoil
    maxiter: int
        maximal number of boundary layer iterations
    n: int
        boundary layer parameter
    """
    
    import subprocess as sp
    import sys,os
    
    if(os.name == 'posix'):
        xfoilbin = 'xfoil'
    elif(os.name == 'nt'):
        xfoilbin = os.path.join(XFOIL699_PATH,'xfoil.exe')
    else:
        print('Betriebssystem %s wird nicht unterstützt'%os.name)   
    
    
    pxfoil = sp.Popen([xfoilbin], stdin=sp.PIPE, stdout=None, stderr=None)
    
    def write2xfoil(string):
        if(sys.version_info > (3,0)):
            string = string.encode('ascii')
            
        pxfoil.stdin.write(string)
        

    write2xfoil('LOAD ' + afile + '\n')
        
    if(refine):
        write2xfoil('PANE\n')

    write2xfoil('OPER\n')
    if n != None:
        write2xfoil('VPAR\n')
        write2xfoil('N '+str(n)+'\n')
        write2xfoil('\n')
    write2xfoil('ITER '+str(max_iter)+'\n')
    write2xfoil('VISC\n')
    write2xfoil(str(re) + '\n')
    write2xfoil('PACC\n')
    write2xfoil('\n')
    write2xfoil('\n')
    
 
    alfaseq = range(a_start, a_end+ a_step,a_step)
        
    for a in alfaseq:
        write2xfoil('A ' + str(a) + '\n')
        
    write2xfoil('PWRT 1\n')
    write2xfoil(polarfile + '\n')
    write2xfoil('\n')

    pxfoil.communicate(str('quit').encode('ascii'))

def read_polar(infile):
    """read xfoil polar results from file
    
    Parameters
    ----------
    infile: string
        path to polar file
     
    Returns
    -------
    dict
        airfoil polar splitted up into dictionary
    """
    
    regex = re.compile('(?:\s*([+-]?\d*.\d*))')
    
    with open(infile) as f:
        lines = f.readlines()
        
        alpha          = []
        cl          = []
        cd          = []
        cdp         = []
        cm          = []
        xtr_top     = []
        xtr_bottom  = []
        
        
        for line in lines[12:]:
            linedata = regex.findall(line)
            alpha.append(float(linedata[0]))
            cl.append(float(linedata[1]))       
            cd.append(float(linedata[2]))
            cdp.append(float(linedata[3]))
            cm.append(float(linedata[4]))
            xtr_top.append(float(linedata[5]))
            xtr_bottom.append(float(linedata[6]))
            
        return {'a': np.array(a), 'cl': np.array(cl) , 'cd': np.array(cd), 'cdp': np.array(cdp),
             'cm': np.array(cm), 'xtr_top': np.array(xtr_top), 'xtr_bottom': np.array(xtr_bottom)}



def _delete_polar(infile):
    """ deletes polar file """
    os.remove(infile)
    


if __name__ == '__main__':

    from prop_toolkit import DATA_PATH

    in_file = os.path.join(DATA_PATH,'a1.dat')
    #out_file = os.path.join(DATA_PATH,'a1_1.dat)
    data = run_xfoil(in_file,50000,None)
