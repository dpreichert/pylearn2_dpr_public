"""
This script makes a dataset of 32x32 contrast normalized, approximately
whitened CIFAR-100 images.

"""
import logging

from pylearn2.utils import serial
from pylearn2.datasets import preprocessing
from pylearn2.utils import string_utils
from pylearn2.datasets.cifar100 import CIFAR100


logger = logging.getLogger(__name__)

data_dir = string_utils.preprocess('${PYLEARN2_DATA_PATH}/cifar100')

logger.info('Loading CIFAR-100 train dataset...')
train = CIFAR100(which_set = 'train', gcn = 55.)

logger.info("Preparing output directory...")
output_dir = data_dir + '/pylearn2_gcn_whitened'
serial.mkdir( output_dir )
README = open(output_dir + '/README','w')

README.write("""
The .pkl files in this directory may be opened in python using
cPickle, pickle, or pylearn2.serial.load.

train.pkl, and test.pkl each contain
a pylearn2 Dataset object defining a labeled
dataset of a 32x32 contrast normalized, approximately whitened version of the CIFAR-100
dataset. train.pkl contains labeled train examples. test.pkl
contains labeled test examples.

preprocessor.pkl contains a pylearn2 ZCA object that was used
to approximately whiten the images. You may want to use this
object later to preprocess other images.

They were created with the pylearn2 script make_cifar100_gcn_whitened.py.

All other files in this directory, including this README, were
created by the same script and are necessary for the other files
to function correctly.
""")

README.close()

logger.info("Learning the preprocessor and " +
			"preprocessing the unsupervised train data...")
preprocessor = preprocessing.ZCA()
train.apply_preprocessor(preprocessor = preprocessor, can_fit = True)

logger.info('Saving the training data')
train.use_design_loc(output_dir+'/train.npy')
serial.save(output_dir + '/train.pkl', train)

logger.info("Loading the test data")
test = CIFAR100(which_set = 'test', gcn = 55.)

logger.info("Preprocessing the test data")
test.apply_preprocessor(preprocessor = preprocessor, can_fit = False)

logger.info("Saving the test data")
test.use_design_loc(output_dir+'/test.npy')
serial.save(output_dir+'/test.pkl', test)

serial.save(output_dir + '/preprocessor.pkl',preprocessor)
