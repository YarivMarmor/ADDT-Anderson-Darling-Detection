"""Faithful checkpoint computations based on user-provided ADD VBA procedure.

IMPORTANT: caller must pass the transformed dataArray as constructed by the
original AndersonDarlingForm. That transformation code has not yet been supplied.
This is a research prototype, not a validated equivalent of the Excel tool.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import erf, log, sqrt
from typing import Iterable
import numpy as np

@dataclass(frozen=True)
class Checkpoint:
    checkpoint: int
    ad_left: float
    ad_right: float
    ad_difference: float

def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def _vba_score_segment(segment: np.ndarray, mode: int, *, right: bool) -> float:
    n = len(segment)
    if not n:
        return 0.0
    if mode == 0:
        # Intentionally replicate the distinct left/right terms and denominators
        # present in the pasted VBA, rather than substituting standard AD.
        acc = 0.0
        for index, x in enumerate(segment):
            y = _normal_cdf(float(x))
            if y <= 0:
                log_y, log_one_minus_y = (-10.0 if right else -10000.0), 0.0
            elif y >= 1:
                log_y, log_one_minus_y = 0.0, (-10.0 if right else -10000.0)
            else:
                log_y, log_one_minus_y = log(y), log(1.0 - y)
            if right:
                # VBA uses k=1,...,n; (2*k+1), (2*(n-k)+1), divisor n+1.
                k = index + 1
                acc -= ((2*k + 1)*log_y + (2*(n-k) + 1)*log_one_minus_y) / (n+1)
            else:
                # VBA: (2*(j+1)-1) and (2*(n-j-1)+1), divisor n.
                acc -= ((2*index + 1)*log_y + (2*(n-index)-1)*log_one_minus_y) / n
        return acc - n
    if mode not in (1,2):
        raise ValueError('Distribution mode must be 0 (Normal), 1 or 2 (form labels pending).')
    # VBA calls Yj=dataArray(j); it does NOT compute the uniform or
    # exponential CDF here. Do not infer a transformation without form code.
    acc = 0.0
    for index, y in enumerate(segment):
        k = index + 1
        c = (k - 3/8) / (n + 1/4)
        c1 = (k + 1 - 3/8) / (n + 1/4)
        if k == 1:
            acc += (y-c)**2 / (1-c)
        if k == n:
            acc += (y-c)**2 / c
        if 1 < k < n:
            acc += (y-c)**2 * (c1-c) / (c*(1-c))
    return float(n*acc if mode == 1 else acc)

def analyze(transformed_data: Iterable[float], mode: int = 0) -> list[Checkpoint]:
    """Compute checkpoints; input must already be transformed like VBA dataArray.

    VBA rounds incoming data to 16 decimals and then sorts each partition.
    Unlike the original bubble sort, numpy sorts are not numerically lossy.
    """
    x = np.asarray(list(transformed_data), dtype=float)
    if x.ndim != 1 or len(x) < 2 or not np.all(np.isfinite(x)):
        raise ValueError('Need at least two finite one-dimensional numeric values')
    if mode not in (0,1,2):
        raise ValueError('Unknown distribution mode')
    x = np.round(x, 16)
    result = []
    for i in range(len(x)):
        left = np.sort(x[:i+1]); right = np.sort(x[i+1:])
        al = _vba_score_segment(left, mode, right=False)
        ar = _vba_score_segment(right, mode, right=True)
        result.append(Checkpoint(i+1, al, ar, abs(al-ar)))
    return result
