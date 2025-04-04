from functools import update_wrapper

import numpy as np

_scene = None
_new_position = lambda x, y: (x, y)
_global_center = [0.0, 0.0]
_scaling_coefficient = 1.0

_allways_reenter = True
_recenter_time = 1.0

valid_point_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
point_names = {}

valid_figure_labels = [chr(i) for i in range(ord('a'), ord('z') + 1)]
figure_names = {}


def init(scene):
    global _scene
    _scene = scene


def on_scene(func):
    def wrapper(*args, **kwargs):
        if _scene is None:
            raise Exception(f"Need scene to use function {func.__name__}")
        return func(*args, **kwargs)

    update_wrapper(wrapper, func)
    return wrapper


def _move_points(points, positions, run_time=2):
    _scene.play(
        *[point.x_tracker.animate.set_value(new_x) for point, (new_x, _) in zip(points, positions)],
        *[point.y_tracker.animate.set_value(new_y) for point, (_, new_y) in zip(points, positions)],
        run_time=run_time
    )


def recenter_camera2(run_time=2):
    global _scaling_coefficient, _new_position

    points = point_names.values()

    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    width = max_x - min_x
    height = max_y - min_y

    if abs(width) < 10 ** -6:
        width = 1
    if abs(height) < 10 ** -6:
        height = 1

    frame_width = _scene.camera.frame_width
    frame_height = _scene.camera.frame_height

    scale_x = frame_width / width
    scale_y = frame_height / height
    scale_factor = min(scale_x, scale_y)

    def new_position(x, y):
        return (x - min_x) * scale_factor - 3, (y - min_y) * scale_factor - 3

    _new_position = new_position

    _move_points(points, [_new_position(point.x, point.y) for point in points], run_time=run_time)


def recenter_camera(run_time=2):
    global _scaling_coefficient

    points = point_names.values()
    p_x = [point.x for point in points]
    p_y = [point.y for point in points]

    '''local_center = np.array([
        (max(p_x) + min(p_x)) / 2,
        (max(p_y) + min(p_y)) / 2,
        0.0
    ])'''

    width = max(p_x) - min(p_x)
    height = max(p_y) - min(p_y)

    if abs(width) < 10 ** -6:
        width = 1
    if abs(height) < 10 ** -6:
        height = 1

    aspect_ratio = _scene.camera.frame_width / _scene.camera.frame_height
    new_width = max(width, height * aspect_ratio)

    scaling_factor = new_width / _scene.camera.frame_width

    _global_center[0] += width / 2
    _global_center[1] += height / 2
    _scaling_coefficient *= scaling_factor

    def new_position(x, y):
        x_new = (x - _global_center[0]) / scaling_factor
        y_new = (y - _global_center[1]) / scaling_factor

        return x_new, y_new

    with open('log.txt', 'a') as file:
        print(f'width: {width}', file=file)
        print(f'height: {height}', file=file)
        print(f'aspect ratio: {aspect_ratio}', file=file)
        print(f'global center: {_global_center}', file=file)
        print(f'new_width: {new_width}', file=file)
        print(f'scaling factior: {scaling_factor}', file=file)
        print('\nPoints:', file=file)
        for point in points:
            print(f'\tposition: ({point.x}, {point.y})\tnew_position: {new_position(point.x, point.y)}', file=file)
        print('\n------------\n', file=file)

    _move_points(points, [new_position(point.x, point.y) for point in points], run_time=run_time)
