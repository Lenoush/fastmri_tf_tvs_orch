import os.path as op
import time

import sys
sys.path.append('/volatile/Lena/Codes/Modèles/fastmri_tf_vs_torch/fastmri_compare/autre')



from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow_addons.callbacks import TQDMProgressBar

from fastmri_tf.data.sequences.fastmri_sequences import ZeroFilled2DSequence
from fastmri_tf.models.functional_models.unet import unet





# paths
train_path = '/volatile/FastMRI/brain_multicoil_train/multicoil_train/'
val_path = '/volatile/FastMRI/brain_multicoil_train/multicoil_train/'
# test_path = '/media/Zaccharie/UHRes/singlecoil_test/'



n_samples_train = 34742
n_samples_val = 7135

n_volumes_train = 973
n_volumes_val = 199





# generators
AF = 4
train_gen = ZeroFilled2DSequence(train_path, af=AF, norm=True)
val_gen = ZeroFilled2DSequence(val_path, af=AF, norm=True)





run_params = {
    'n_layers': 4,
    'pool': 'max',
    "layers_n_channels": [16, 32, 64, 128],
    'layers_n_non_lins': 2,
}
n_epochs = 300
run_id = f'unet_af{AF}_{int(time.time())}'
chkpt_path = f'checkpoints/{run_id}' + '-{epoch:02d}.hdf5'





chkpt_cback = ModelCheckpoint(chkpt_path, period=100)
log_dir = op.join('logs', run_id)
tboard_cback = TensorBoard(
    log_dir=log_dir,
    profile_batch=0,
    histogram_freq=0,
    write_graph=True,
    write_images=False,
)
tqdm_cb = TQDMProgressBar()




model = unet(input_size=(320, 320, 1), lr=1e-3, **run_params)
print(model.summary())





model.fit_generator(
    train_gen,
    steps_per_epoch=n_volumes_train,
    epochs=n_epochs,
    validation_data=val_gen,
    validation_steps=1,
    verbose=0,
    callbacks=[tqdm_cb, tboard_cback, chkpt_cback],
    # max_queue_size=100,
    use_multiprocessing=True,
    workers=35,
)
