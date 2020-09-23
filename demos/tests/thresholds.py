# Copyright (c) 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

THRESHOLDS = {
    'object_detection_demo_yolov3_async': {
        'yolo-v3-tf': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.005, 0.005, 0.005]
            }
        }
    },
    'segmentation_demo': {
        'road-segmentation-adas-0001': {
            'CPU': {
                'road-segmentation-adas': [0.01, 0.01, 0.01]
            }
        },
        'semantic-segmentation-adas-0001': {
            'CPU': {
                'semantic-segmentation-adas': [0.01, 0.01, 0.01]
            }
        },
        'deeplabv3': {
            'CPU': {
                'semantic-segmentation-adas': [0.01, 0.01, 0.01]
            }
        }
    },
    'py/object_detection_demo_yolov3_async': {
        'yolo-v1-tiny-tf': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.007, 0.007, 0.007]
            }
        },
        'yolo-v2-tiny-tf': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.007, 0.007, 0.007]
            }
        },
        'yolo-v2-tf': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.007, 0.007, 0.007]
            }
        },
        'yolo-v3-tf': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.007, 0.007, 0.007]
            }
        },
        'mobilefacedet-v1-mxnet': {
            'CPU': {
                'object-detection-demo-ssd-async': [0.007, 0.007, 0.007]
            }
        }
    }
}