#!/usr/bin/env python
__author__ = "Ian Goodfellow"
"""
Usage: python num_parameters.py <model_file>.pkl

Prints the number of parameters in a saved model (total number of scalar
elements in all the arrays parameterizing the model).
"""

import logging
import sys

from pylearn2.utils import serial


logger = logging.getLogger(__name__)


def num_parameters(model):
    params = model.get_params()
    return sum(map(lambda x: x.get_value().size, params))

if __name__ == '__main__':
    _, model_path = sys.argv
    model = serial.load(model_path)
    logger.info(num_parameters(model))
