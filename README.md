<!--- Project Logo --->
# LRBench
<!--- a href=""><img src="" alt=""></a --->
-----------------
[![GitHub license](https://img.shields.io/badge/license-apache-green.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)
[![Version](https://img.shields.io/badge/version-0.0.1-red.svg?style=flat)]()
<!---
[![Travis Status]()]()
[![Jenkins Status]()]()
[![Coverage Status]()]()
--->
## Introduction

A learning rate benchmarking and recommending tool, which will help practitioners efficiently select and compose good learning rate policies.

* Semi-automatic Learning Rate Tuning
* Evaluation: A set of Useful Metrics, covering Utility, Cost, and Robustness.
* Verification: Near-optimal Learning Rate

### The impact of learning rates

The following figure shows the impacts of different learning rates. The FIX (black, k=0.025) reached the local optimum, while the NSTEP (red, k=0.05, γ=0.1, l=[150, 180]) converged to the global optimum. For TRIEXP (yellow, k0=0.05, k1=0.3, γ=0.1, l=100), even though it was the fastest, it failed to converge with high fluctuation.

![Comparison of three learning rate functions: FIX, NSTEP, and TRIEXP](examples/visualization/FIX-NSTEP-TRIEXP-Comparison.gif)

If you find this tool useful, please cite the following paper:

    @INPROCEEDINGS{lrbench2019,
        author={Wu, Yanzhao and Liu, Ling and Bae, Juhyun and Chow, Ka-Ho and Iyengar, Arun and Pu, Calton and Wei, Wenqi and Yu, Lei and Zhang, Qi},
        booktitle={2019 IEEE International Conference on Big Data (Big Data)},
        title={Demystifying Learning Rate Policies for High Accuracy Training of Deep Neural Networks},
        year={2019},
        volume={},
        number={},
        pages={1971-1980},  
        doi={10.1109/BigData47090.2019.9006104}
    }
 
## Problem


## Installation
If you would like to use LRBench as a Python module, you can simply run the following command to install LRBench.

    pip install LRBench

If you would like to have access to the web GUI of LRBench, you can follow these steps:

    git clone https://github.com/git-disl/LRBench.git 
    cd LRBench 
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

## Supported Platforms


## Development / Contributing


## Issues


## Status


## Contributors

See the [people page](https://github.com/git-disl/LRBench/graphs/contributors) for the full listing of contributors.

## License

Copyright (c) 20XX-20XX [Georgia Tech DiSL](https://github.com/git-disl)  
Licensed under the [Apache License](LICENSE).

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TP71L8ZFZT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-TP71L8ZFZT');
</script>
