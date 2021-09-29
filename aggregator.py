import re
import os
import sys
import logging

num_parties = 2
# agg_config = {
#     'connection': {
#         'info': {
#             'ip': '127.0.0.1',
#             'port': 5000,
#             'tls_config': {
#                 'enable': 'false'
#             }
#         },
#         'name': 'FlaskConnection',
#         'path': 'ibmfl.connection.flask_connection',
#         'sync': 'False'
#     },
#     'fusion': {
#         'name': 'IterAvgFusionHandler',
#         'path': 'ibmfl.aggregator.fusion.iter_avg_fusion_handler'
#     },
#     'hyperparams': {
#         'global': {
#             'max_timeout': 60,
#             'num_parties': num_parties,
#             'perc_quorum': 1,
#             'rounds': 5,
#             'termination_accuracy': 0.9
#         },
#         'local': {
#             'optimizer': {
#                 'lr': 0.01
#             },
#             'training': {
#                 'epochs': 3,
#                 'steps_per_epoch' : 5,
#                 'batch_size' : 5
#             }
#         }
#     },
#     'protocol_handler': {
#         'name': 'ProtoHandler',
#         'path': 'ibmfl.aggregator.protohandler.proto_handler'
#     }
# }

agg_config = {
    'connection': {
        'info': {
            'ip': '127.0.0.1',
            'port': 5000,
            'tls_config': {
                'enable': 'false'
            }
        },
        'name': 'FlaskConnection',
        'path': 'ibmfl.connection.flask_connection',
        'sync': 'False'
    },
    'fusion': {
        'name': 'IterAvgFusionHandler',
        'path': 'ibmfl.aggregator.fusion.iter_avg_fusion_handler'
    },
    'hyperparams': {
        'global': {
             #'max_timeout': 300,
            'num_parties': num_parties,
            'perc_quorum': 1,
            'rounds': 10,
            'termination_accuracy': 0.9
        },
        'local': {
            'optimizer': {
                'lr': 0.01
            },
            'training': {
                'epochs': 1,
                'steps_per_epoch' : 25000//64,
                # 'batch_size' : 5
            }
        }
    },
    'protocol_handler': {
        'name': 'ProtoHandler',
        'path': 'ibmfl.aggregator.protohandler.proto_handler'
    }
}





from ibmfl.aggregator.aggregator import Aggregator
from ibmfl.aggregator.states import States
agg = Aggregator(config_dict=agg_config)

while 1:
        msg = sys.stdin.readline()
        # TODO: move it to Aggregator
        if re.match('START', msg):
            agg.proto_handler.state = States.CLI_WAIT
            logging.info("State: " + str(agg.proto_handler.state))
            # Start server
            agg.start()

        elif re.match('STOP', msg):
            agg.proto_handler.state = States.STOP
            logging.info("State: " + str(agg.proto_handler.state))
            agg.stop()
            break

        elif re.match('TRAIN', msg):
            agg.proto_handler.state = States.TRAIN
            logging.info("State: " + str(agg.proto_handler.state))
            success = agg.start_training()
            if not success:
                agg.stop()
                break

        elif re.match('SAVE', msg):
            agg.proto_handler.state = States.SAVE
            logging.info("State: " + str(agg.proto_handler.state))
            agg.save_model()

        elif re.match('EVAL', msg):
            agg.proto_handler.state = States.EVAL
            logging.info("State: " + str(agg.proto_handler.state))
            agg.eval_model()

        elif re.match('SYNC', msg):
            agg.proto_handler.state = States.SYNC
            logging.info("State: " + str(agg.proto_handler.state))
            agg.model_synch()
exit()