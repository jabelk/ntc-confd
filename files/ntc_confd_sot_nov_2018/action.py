"""
*********************************************************************
* ConfD Actions intro example                                       *
* Implements a couple of actions                                    *
*                                                                   *
* (C) 2017 Tail-f Systems                                           *
* Permission to use this code as a starting point hereby granted    *
*                                                                   *
* See the README file for more information                          *
*********************************************************************
"""
from __future__ import print_function

import sys
from ntc_sot_ns import ns

from confd.dp import Action, Daemon
from confd.maapi import Maapi
from confd.log import Log
# demo REST Call from training
from dynamo import main as dynamo_main

#logger class used by Daemon
class MyLog(object):
    def info(self, arg):
        print("info: %s" % arg)
    def error(self, arg):
        print("error: %s" % arg)

class DynamoAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info("Making REST CALL")
        rest_call = dynamo_main()
        # no input for now
        #ans_play = input.ansible_playbook
        res = "Result from REST Call \n\n" + str(rest_call) + "\n\n"
        output.rest_output = res

def load_schemas():
    with Maapi():
        pass

if __name__ == "__main__":
    # load in the application schema
    load_schemas()
    logger = Log(MyLog(), add_timestamp=True)
    d = Daemon(name='myactiond', log=logger)

    a = []
    # Register the Action into application
    a.append(DynamoAction(daemon=d, actionpoint='act-dynamo_rest_call', log=logger))

    logger.info('--- Daemon myaction STARTED ---')
    # start listening for possible action callbacks
    d.start()
    print('Hit <ENTER> to quit')
    # wait for Enter to end the python listen for actions
    sys.stdin.read(1)
    d.finish()
    logger.info('--- Daemon myaction FINISHED ---')
