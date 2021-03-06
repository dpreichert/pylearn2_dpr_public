import unittest

import numpy
import scipy.sparse
import logging

from pylearn2.testing.skip import skip_if_no_data
import pylearn2.datasets.utlc as utlc

logger = logging.getLogger(__name__)


def test_ule():
    skip_if_no_data()
    # Test loading of transfer data
    train, valid, test, transfer = utlc.load_ndarray_dataset("ule", normalize=True, transfer=True)
    assert train.shape[0]==transfer.shape[0]


#@unittest.skip("Slow and needs >8 GB of RAM")
def test_all_utlc():
    skip_if_no_data()
    for name in ['avicenna','harry','ule']:   # not testing rita, because it requires a lot of memorz and is slow
        logger.info("Loading %s", name)
        train, valid, test = utlc.load_ndarray_dataset(name, normalize=True)
        logger.info("dtype, max, min, mean, std")
        logger.info("%d %d %d %d %d", train.dtype, train.max(),
                    train.min(), train.mean(), train.std())
        assert isinstance(train, numpy.ndarray), "train is not an ndarray in %s dataset" % name
        assert isinstance(valid, numpy.ndarray), "valid is not an ndarray in %s dataset" % name
        assert isinstance(test, numpy.ndarray), "test is not an ndarray in %s dataset" % name
        assert train.shape[1]==test.shape[1]==valid.shape[1], "shapes of datasets does not match for %s" % name

def test_sparse_ule():
    skip_if_no_data()
    # Test loading of transfer data
    train, valid, test, transfer = utlc.load_sparse_dataset("ule", normalize=True, transfer=True)
    assert train.shape[0]==transfer.shape[0]

def test_all_sparse_utlc():
    skip_if_no_data()
    for name in ['harry','terry','ule']:
        logger.info("Loading sparse %s", name)
        train, valid, test = utlc.load_sparse_dataset(name, normalize=True)
        nb_elem = numpy.prod(train.shape)
        mi = train.data.min()
        ma = train.data.max()
        mi = min(0, mi)
        ma = max(0, ma)
        su = train.data.sum()
        mean = float(su)/nb_elem
        logger.info("%s dtype, max, min, mean, nb non-zero, nb element, " +
                    "sparse", name)
        logger.info("%d %d %d %d %d %d %d", train.dtype, ma, mi, mean,
                    train.nnz, nb_elem, (nb_elem-float(train.nnz))/nb_elem)
        logger.info("%s max, min, mean, std (all stats on non-zero element)",
                    name)
        logger.info("%d %d %d %d", train.data.max(), train.data.min(),
                    train.data.mean(), train.data.std())
        assert scipy.sparse.issparse(train), "train is not sparse for %s dataset" % name
        assert scipy.sparse.issparse(valid), "valid is not sparse for %s dataset" % name
        assert scipy.sparse.issparse(test), "test is not sparse for %s dataset" % name
        assert train.shape[1]==test.shape[1]==valid.shape[1], "shapes of sparse %s dataset do  not match" % name
