"""
 Copyright (c) 2019 Intel Corporation
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys
import os

import logging as log
import numpy as np
import cv2 as cv

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common'))
from ie_config_helper import create_default_config


class IEModel:
    """Class for inference of models in the Inference Engine format"""
    def __init__(self, exec_net, inputs_info, input_key, output_key):
        self.net = exec_net
        self.inputs_info = inputs_info
        self.input_key = input_key
        self.output_key = output_key
        self.reqs_ids = []

    def _preprocess(self, img):
        _, _, h, w = self.get_input_shape()
        img = np.expand_dims(cv.resize(img, (w, h)).transpose(2, 0, 1), axis=0)
        return img

    def forward(self, img):
        """Performs forward pass of the wrapped IE model"""
        res = self.net.infer(inputs={self.input_key: self._preprocess(img)})
        return np.copy(res[self.output_key])

    def forward_async(self, img):
        id = len(self.reqs_ids)
        self.net.start_async(request_id=id,
                             inputs={self.input_key: self._preprocess(img)})
        self.reqs_ids.append(id)

    def grab_all_async(self):
        outputs = []
        for id in self.reqs_ids:
            self.net.requests[id].wait(-1)
            res = self.net.requests[id].output_blobs[self.output_key].buffer
            outputs.append(np.copy(res))
        self.reqs_ids = []
        return outputs

    def get_input_shape(self):
        """Returns an input shape of the wrapped IE model"""
        return self.inputs_info[self.input_key].input_data.shape


def load_ie_model(ie, model_xml, device, plugin_dir, num_reqs=1):
    """Loads a model in the Inference Engine format"""
    # Plugin initialization for specified device
    log.info("Initializing Inference Engine plugin for %s ", device)

    # Read IR
    log.info("Loading network")
    net = ie.read_network(model_xml, os.path.splitext(model_xml)[0] + ".bin")

    if "CPU" in device:
        supported_layers = ie.query_network(net, "CPU")
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if not_supported_layers:
            log.error("Following layers are not supported by the plugin for specified device %s:\n %s",
                      device, ', '.join(not_supported_layers))
            sys.exit(1)

    assert len(net.input_info) == 1 or len(net.input_info) == 2, \
        "Supports topologies with only 1 or 2 inputs"
    assert len(net.outputs) == 1 or len(net.outputs) == 4 or len(net.outputs) == 5, \
        "Supports topologies with only 1, 4 or 5 outputs"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.input_info))
    out_blob = next(iter(net.outputs))
    net.batch_size = 1

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name=device, create_default_config(device_string),
                               num_requests=num_reqs)
    model = IEModel(exec_net, net.input_info, input_blob, out_blob)
    return model
