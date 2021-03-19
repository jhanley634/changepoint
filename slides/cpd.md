
---
author: John Hanley
title: changepoint detection
copyright: 2021
---


<!---
Copyright 2021 John Hanley. MIT licensed.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
The software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall
the authors or copyright holders be liable for any claim, damages or
other liability, whether in an action of contract, tort or otherwise,
arising from, out of or in connection with the software or the use or
other dealings in the software.
--->


# change point detection

https://charles.doffy.net/files/sp-review-2020.pdf

the signal is assumed to be piecewise stationary … change point detection is cast as a model selection problem …

E.g. a generating process governed by a policy or SOP could be piecewise stationary,
and we wish to infer the date that an intervention had a measurable effect.


# two categories

- Problem 1 : specified number of changes K
- Problem 2 : unknown number of changes


# asymptotic consistency

Consider discrete samples from a continuous process.

(i) More samples won't change K, ..and..

(ii) More samples only moves the segmentation boundaries slightly
(small Hausdorff distance between true and estimated change points)

\blank
## remark

Nyquist says we still need _some_ samples.


# metrics

annotation error: wrong K

Hausdorff metric: worst segmentation mis-match (time axis)

Rand index: accurate agreement between segmentations
(nicely deals with wrong K)

F1-score: the usual precision recall balance, though it needs an error parameter M


\blank
## remark

Suppose the estimated segmentation inserts an extra segment beyond the truth.
Doesn't it seem like inserting early or late (at start or end) would
make the Hausdorff metric come out different?


# models, costs

(see Fig. 6 & Table 1)

- MLE: shifts in mean, scale, Poisson rate, variance, counts. Asymptotically consistent.
- Piecewise linear regression
- Mahalanobis
- non-parametric: empirical CDF, rank statistics, and kernel estimation.

\blank
## remark

> A natural extension to the mean-shift model consists in let- ting the variance abruptly change as well.

Could a change in manager's attention change the variance? With size-of-effect big enough to notice?


# models

- M1: $f$, single function, with parameters that change in each regime
- M2: $y_t=x'_t u_k+z'_t v + ε_t$ , observed co-variates plus noise
- M3: $F_k$, different function for each regime


# search

(see Fig. 7)

- `OPT`'s quadratic complexity, $O(K T^2)$, motivates subsampling or pruning, to reduce T.
- Complexity of `Pelt` is of the order $O(T)$, for sensible regime lengths.
- `Win` always enjoys linear complexity, $O(T)$ or maybe $O(w T)$. And then `PKSearch` may include a sort rather than threshold.
- Complexity of `BinSeg` is $O(T \log T)$; segments considered are not homogeneous. Cf wild binary segmentation.
- `BotUp`: similar, but doesn't guarantee asymptotic consistency.


# penalty

- linear, $l_0$: BIC, AIC, $pen_{l_0}$
- fused lasso
- complex penalties: intractable, not optimizable

# current challenges

- many dimensions
  - DNA: https://en.wikipedia.org/wiki/Copy_number_analysis
  - search over "cost function" space?
- supervised learning for calibration

The importance of convexity.

# python package

- general purpose methods included, ignoring niche ones
- K known, or not
- modular, with consistent interface
- scaling, caching
