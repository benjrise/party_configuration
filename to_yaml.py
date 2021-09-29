import yaml

party_id = 0
party_config = {
        'aggregator':
            {
                'ip': '213.52.128.114',
                'port': 5000
            },
        'connection': {
            'info': {
                'ip': '0.0.0.0',
                'port': 5000,
                'id': 'party' + str(party_id),
                'tls_config': {
                    'enable': False
                }
            },
            'name': 'FlaskConnection',
            'path': 'ibmfl.connection.flask_connection',
            'sync': True
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
  
with open('party_test.yaml', 'w') as file:
    documents = yaml.dump(party_config, file)