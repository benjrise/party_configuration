import sys
import re
party_id = 1
#sys.path.append('../..')
import os


num_parties = 2  ## number of participating parties

def get_party_config(party_id):
    party_config = {
        'aggregator':
            {
                'ip': '127.0.0.1',
                'port': 5000
            },
        'connection': {
            'info': {
                'ip': '127.0.0.1',
                'port': 8085 + party_id,
                'id': 'party' + str(party_id),
                'tls_config': {
                    'enable': False
                }
            },
            'name': 'FlaskConnection',
            'path': 'ibmfl.connection.flask_connection',
            'sync': False
        },

        'data': {
            'info': {
                'data_set': 'CIFAR10/random/data_party' + str(party_id) + '.npz',
                'batch_size' : 64
            },
            'name': 'Cifar10KerasDataGenerator',
            'path': 'DataHandlers/DataGenerators.py'
        },

        'local_training': {
            'name': 'LocalTrainingHandler',
            'path': 'ibmfl.party.training.local_training_handler'
        },

        'model': {
            'name': 'KerasFLModel',
            'path': 'ibmfl.model.keras_fl_model',
            'spec': {
                'model_definition': 'Models/keras_classifier_cifar10/compiled_keras.h5',
                'model_name': 'keras-cnn'
            }
        },
        
        'protocol_handler': {
            'name': 'PartyProtocolHandler',
            'path': 'ibmfl.party.party_protocol_handler'
        }
    }
    return party_config

from ibmfl.party.party import Party
import tensorflow as tf

party_config = get_party_config(party_id)

party = Party(config_dict=party_config)
party.start()
party.proto_handler.is_private = False 
while 1:
    msg = sys.stdin.readline()
    if re.match('REG', msg):
        party.register_party()
    msg = sys.stdin.readline()
    if re.match('STOP', msg):
        party.stop()
        break
exit()
#party.proto_handler.is_private = False  ## allows sharing of metrics with aggregator