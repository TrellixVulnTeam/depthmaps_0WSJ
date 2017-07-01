"""Interactive data viewer.

Props @shoeffner:
https://github.com/shoeffner/ann3depth/blob/master/src/visualize/dataviewer.py
"""
import itertools
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image
from mpl_toolkits.mplot3d import Axes3D


class Dataviewer:

    def __init__(self, dataset, *,
                 rows=2,
                 keys=['image', 'depth'],
                 cmaps={'depth': 'jet'},
                 name=None):
        self.dataset = dataset
        self.rows = rows
        self.keys = keys

        self.current = 0

        self.figure, self.axes = plt.subplots(rows, len(self.keys))
        if name:
            self.figure.canvas.set_window_title(name)

        self.axes = self.axes.flatten()
        self.images = []
        for i, axes in enumerate(self.axes):
            cmap = cmaps[keys[i % len(keys)]] if keys[i % len(keys)] in cmaps \
                else None
            img = image.AxesImage(axes, cmap=cmap)
            axes.set_aspect('equal')
            self.images.append(axes.add_image(img))

        self.show_next()

        self.keycb = self.figure.canvas.mpl_connect(
            'key_press_event',
            lambda event: self.__key_press_event(event))

    def show_next(self):
        self.update_axes()

    def show_previous(self):
        self.current = (self.current - 2 * self.rows) % len(self.dataset)
        self.update_axes()

    def update_axes(self):
        first = self.current
        keys = enumerate(self.keys)
        for axes, img, (col, key) in zip(self.axes, self.images,
                                         itertools.cycle(keys)):
            sample = self.dataset[self.current]
            if hasattr(sample, key) and getattr(sample, key) is not None:
                data = np.squeeze(getattr(sample, key))
            elif isinstance(sample, (list, tuple)) and len(sample) > col:
                data = np.squeeze(sample[col])
            else:
                data = np.array([[1]])
            img.set_data(data)
            axes.set_xlim([0, data.shape[1]])
            axes.set_ylim([data.shape[0], 0])

            if key == self.keys[-1]:
                self.current = (self.current + 1) % len(self.dataset)

        self.figure.suptitle(f'Showing samples {first} to {self.current - 1}')
        self.figure.canvas.draw()

    def __key_press_event(self, event):
        events = {
            'q': lambda event: plt.close(self.figure),
            'escape': lambda event: plt.close(self.figure),
            'cmd+w': lambda event: plt.close(self.figure),
            'right': lambda event: self.show_next(),
            'down': lambda event: self.show_next(),
            'left': lambda event: self.show_previous(),
            'up': lambda event: self.show_previous()
        }
        try:
            events[event.key](event)
        except KeyError:
            print(f'Key pressed but no action available: {event.key}')


if __name__ == '__main__':
    import data

    DataBrowser(data.mixed(samples=16))
    plt.show()
