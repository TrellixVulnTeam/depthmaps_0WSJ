import tensorflow as tf

from lib import Dataviewer
from datasets import Make3D, Nyu
from models import Simple, Eigen2014


dataset = Make3D()
model = Simple(dataset, workers=2)

print('First epoch will be slow due to data preprocessing and caching...')
model.train(epochs=5, save_frequency=1)

results = model.evaluate()
Dataviewer(results, name='Results', keys=['image', 'depth', 'result'],
           cmaps={'depth': 'gray', 'result': 'gray'})
plt.show(True)
