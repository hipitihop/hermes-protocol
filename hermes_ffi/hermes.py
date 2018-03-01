# -*- coding: utf-8 -*-

from ctypes import byref, POINTER, c_char_p
from ffi.ontology import CProtocolHandler, CDialogueFacade
from ffi.utils import *
from time import sleep

class Hermes(object):
    def __init__(self, mqtt_server_address):
        self._protocol_handler = POINTER(CProtocolHandler)()  # TODO: Destroy protocol handler
        self._facade = POINTER(CDialogueFacade)()

        lib.hermes_protocol_handler_new_mqtt(byref(self._protocol_handler), mqtt_server_address)

        lib.hermes_protocol_handler_dialogue_facade(self._protocol_handler,
                                                    byref(self._facade))

        # References to user-defined callbacks
        self._subscribe_intent_callback = callable

    def subscribe_intent(self, intent_name, user_callback_subscribe_intent):
        self._subscribe_intent_callback = user_callback_subscribe_intent
        hermes_dialogue_subscribe_intent(self._facade, c_char_p(intent_name), self._subscribe_intent_callback)
        return self

    def start(self):
        while 1:
            sleep(.1)
