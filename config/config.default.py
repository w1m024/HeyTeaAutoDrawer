# -*- coding: utf-8 -*-
# Default configuration values for HeyTeaAutoDraw
# This file is intended to be the source of truth for default CONFIG
# and may be used to reset the runtime config while preserving certain
# runtime-determined values (like screen/image sizes).

CONFIG = {
    'draw_config': {
        'DELAY': 3,
        'ENABLE_JITTER': True,
        'JITTER_AMOUNT': 1.5,
        'JITTER_FREQUENCY': 2,
        'SPEED_FACTOR': 1,
    },
    'image_config': {
        'BRUSH_STEP': 3,
        'CANNY_THRESH1': 50,
        'CANNY_THRESH2': 150,
        'EPSILON_FACTOR': 0.0001,
        'H_IMG': 0,
        'THRESHOLD_VALUE': 0,
        'W_IMG': 0,
    },
    'screen_config': {
        'H': 0,
        'W': 0,
        'X_A': 0,
        'Y_A': 0,
    },
}
