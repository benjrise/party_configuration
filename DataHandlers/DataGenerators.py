
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import Sequence
from ibmfl.data.data_handler import DataHandler
from ibmfl.exceptions import FLException
import logging as log
import numpy as np
from math import ceil
import os

class CatsDogsDataGenerator(DataHandler):

    def __init__(self, data_config):
        super().__init__()
        
        # Specify the directory of training and testing dataset files.
        self.train_file = data_config['training_set']
        self.test_file = data_config['testing_set']
        # Load the batch size if any
        if 'batch_size' in data_config:
            self.batch_size = data_config['batch_size']
        #  self.set_batch_size(self.batch_size)
        else:
            self.batch_size = 5
        
        # Set up the data generators with the `DataGenerator` class (see below for its definition)
        self.train_datagenerator = ImageDataGenerator(rescale=1./255)\
        .flow_from_directory(directory=self.train_file, target_size=(224,224), classes = ['cat', 'dog'], batch_size = self.batch_size)
        self.test_datagenerator = ImageDataGenerator(rescale=1./255)\
        .flow_from_directory(directory=self.train_file, target_size=(224,224), classes = ['cat', 'dog'], batch_size = self.batch_size)
            
    def get_data(self):
        """
        Return a tuple of data generators for training and testing purposes.
        """
        return self.train_datagenerator, self.test_datagenerator


class Cifar10KerasDataGenerator(DataHandler):

    def __init__(self, data_config):
        
        super().__init__()
        # Specify the directory of training and testing dataset files.
        self.file_name = data_config['data_set']
        
        # Set up the data generators with the `DataGenerator` class (see below for its definition)
        try:
            data_train = np.load(self.file_name)
            self.x_train = data_train['x_train']
            self.y_train = data_train['y_train']
            self.x_test = data_train['x_test']
            self.y_test = data_train['y_test']
        except:
            raise IOError('Unable to load training data from path '
                              'provided in config file: ' +
                              self.file_name)
        
        # Load the batch size if any
        if 'batch_size' in data_config:
            self.batch_size = data_config['batch_size']
            #self.set_batch_size(self.batch_size)

        self.preprocess_data()

    def get_data(self):
        """
        Return a tuple of data generators for training and testing purposes.
        """
        return DataGenerator(self.x_train, self.y_train, self.batch_size), DataGenerator(self.x_test, self.y_test, self.batch_size)

    def preprocess_data(self):
        """
        Preprocesses the training and testing dataset.

        :return: None
        """
        num_classes = 10
        img_rows, img_cols = 32, 32
        self.x_train = self.x_train.reshape(self.x_train.shape[0], img_rows, img_cols, 3) #*(1/255.0)
        self.x_test = self.x_test.reshape(self.x_test.shape[0], img_rows, img_cols, 3) #*(1/255.0)

        # convert class vectors to binary class matrices
        self.y_train = np.eye(num_classes)[self.y_train]
        self.y_test = np.eye(num_classes)[self.y_test]
    
    # def set_batch_size(self, batch_size):
    #     """
    #     Set up the batch size for loading the training data samples.
    #     """
    #     self.batch_size = batch_size


class DataGenerator(Sequence):
    def __init__(self, x_data, y_data, batch_size):
        self.x, self.y = x_data, y_data
        self.batch_size = batch_size
        self.num_batches = ceil(len(x_data) / batch_size)
        self.batch_idx = np.array_split(range(len(x_data)), self.num_batches)

    def __len__(self):
        return len(self.batch_idx)

    def __getitem__(self, idx):
        batch_x = self.x[self.batch_idx[idx]]
        batch_y = self.y[self.batch_idx[idx]]
        return batch_x, batch_y

#