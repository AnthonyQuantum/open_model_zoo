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

import numpy as np

import cv2
from sklearn.metrics.pairwise import cosine_distances # pylint: disable=import-error
from tqdm import tqdm

from image_retrieval_demo.common import from_list, crop_resize

from openvino.inference_engine import IECore # pylint: disable=no-name-in-module

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common'))
from ie_config_helper import create_default_config


class IEModel(): # pylint: disable=too-few-public-methods
    """ Class that allows worknig with Inference Engine model. """

    def __init__(self, model_path, device):
        ie = IECore()

        path = '.'.join(model_path.split('.')[:-1])
        self.net = ie.read_network(path + '.xml', path + '.bin')
        self.output_name = list(self.net.outputs.keys())[0]
        self.exec_net = ie.load_network(network=self.net, device_name=device, create_default_config(device))

    def predict(self, image):
        ''' Takes input image and returns L2-normalized embedding vector. '''

        assert len(image.shape) == 4
        image = np.transpose(image, (0, 3, 1, 2))
        out = self.exec_net.infer(inputs={'Placeholder': image})[self.output_name]
        return out


class ImageRetrieval:
    """ Class representing Image Retrieval algorithm. """

    def __init__(self, model_path, device, gallery_path, input_size):
        self.impaths, self.gallery_classes, _, self.text_label_to_class_id = from_list(
            gallery_path, multiple_images_per_label=False)
        self.input_size = input_size
        self.model = IEModel(model_path, device)
        self.embeddings = self.compute_gallery_embeddings()

    def compute_embedding(self, image):
        ''' Takes input image and computes embedding vector. '''

        image = crop_resize(image, self.input_size)
        embedding = self.model.predict(image)
        return embedding

    def search_in_gallery(self, embedding):
        ''' Takes input embedding vector and searches it in the gallery. '''

        distances = cosine_distances(embedding, self.embeddings).reshape([-1])
        sorted_indexes = np.argsort(distances)
        return sorted_indexes, distances

    def compute_gallery_embeddings(self):
        ''' Computes embedding vectors for the gallery. '''

        images = []

        for full_path in tqdm(self.impaths, desc='Reading gallery images.'):
            image = cv2.imread(full_path)
            if image is None:
                print("ERROR: cannot find image, full_path =", full_path)
            image = crop_resize(image, self.input_size)
            images.append(image)

        embeddings = [None for _ in self.impaths]

        index = 0
        for image in tqdm(images, desc='Computing embeddings of gallery images.'):
            embeddings[index] = self.model.predict(image).reshape([-1])
            index += 1

        return embeddings
