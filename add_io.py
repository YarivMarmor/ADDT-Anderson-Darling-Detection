"""Load and transform data according to AndersonDarlingForm.frm."""
from pathlib import Path
import numpy as np

def load_values(path):
    raw = Path(path).read_text(encoding='utf-8-sig')
    vals=[]
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            vals.append(float(line.strip()))
        except ValueError as e:
            raise ValueError(f'Non-numeric value on line {line_no}: {line!r}') from e
    arr=np.asarray(vals,dtype=float)
    if len(arr)<3 or not np.isfinite(arr).all():
        raise ValueError('At least three finite observations required')
    return arr

def default_parameters(raw, mode):
    """Form defaults: sample standard deviation (n-1), uniform mean +/- sqrt(3)*SD."""
    mean=float(np.mean(raw)); sd=float(np.std(raw,ddof=1))
    if mode==0:return mean,sd
    if mode==1:return mean-np.sqrt(3)*sd,mean+np.sqrt(3)*sd
    if mode==2:return mean,None
    raise ValueError('Unknown distribution')

def transform(raw,mode,param1,param2=None):
    raw=np.asarray(raw,dtype=float)
    if mode==0:
        if param2 is None or param2<=0:raise ValueError('Normal SD must be positive')
        result=(raw-param1)/param2
    elif mode==1:
        if param2 is None or param2<=param1:raise ValueError('Uniform upper bound must exceed lower bound')
        result=(np.clip(raw,param1,param2)-param1)/(param2-param1)
    elif mode==2:
        if param1<=0:raise ValueError('Exponential scale/mean must be positive')
        result=1-np.exp(-raw/param1)
    else:raise ValueError('Unknown distribution')
    if not np.isfinite(result).all():raise ValueError('Transform produced nonfinite values')
    return result
