# Edit these to location of pictures, if already in numpy array then convert folder should be false
path = '/content/drive/My Drive/cs/cs344/cat_64x64.npy'
convertFolder = False

from os import listdir
import sys, subprocess
from matplotlib import pyplot
import math
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D, Conv2DTranspose
from keras.models import Sequential, Model
from keras.models import load_model
from keras.optimizers import Adam, SGD
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.backend import clear_session
from numpy import asarray
from numpy import save
from numpy import load
from numpy import ones
from numpy import zeros
from numpy import vstack
from numpy import expand_dims
from numpy.random import randn
from numpy.random import randint
import sys, subprocess

# install tensorflow gpu build if in colab
# taken from https://timsainburg.com/google%20colab.html
def run_subprocess_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode().strip())


IN_COLAB = "google.colab" in sys.modules
colab_requirements = ["pip install tf-nightly-gpu-2.0-preview"]
if IN_COLAB:
    for i in colab_requirements:
        run_subprocess_command(i)
    from google.colab import drive

    drive.mount('/content/drive')


# define a way to load data
def load_data(convert, path):
    if (convert == True):
        # Load in photos from google drive
        # define location of dataset
        folder = path
        photos = list()
        progress = 0
        # load each image in directory
        for file in listdir(folder):
            if (progress % 100) == 0:
                print(progress)
            # load image
            photo = load_img(folder + file, target_size=(image_width, image_height))
            # convert to numpy array
            photo = img_to_array(photo)
            # store
            photos.append(photo)
            progress = progress + 1
        # convert to a numpy array
        photos = asarray(photos)
        print(photos.shape)
        # save the reshaped photos
        save('saved_data.npy', photos)
        return photos
    else:
        # load photos from pre-made npy file
        photos = load(path)
        return photos


# Define variables
image_width = 64
image_height = 64
# Defining the Input shape
image_shape = (64, 64, 3)
latent_dim = 100
# load in cat data
X = load_data(convertFolder, path)

# display some images to test
for i in range(9):
    # define subplot
    pyplot.subplot(3, 3, 1 + i)
    # turn off axis labels
    pyplot.axis('off')
    # plot single image
    pyplot.imshow(X[randint(0, len(X))] / 255.0)
# show the figure
pyplot.show()
# convert from unsigned ints to floats
X = X.astype('float32')
# scale from [0,255] to [-1,1]
X = (X - 127.5) / 127.5


# define discriminator model
def define_discriminator(in_shape=(64, 64, 3)):
    model = Sequential()
    # perform convolution on initial size
    model.add(Conv2D(64, (3, 3), padding='same', input_shape=in_shape))
    model.add(LeakyReLU(alpha=0.2))
    # downsample to 32x32
    model.add(Conv2D(128, (3, 3), strides=(2, 2), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    # downsample to 16x16
    model.add(Conv2D(128, (3, 3), strides=(2, 2), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    # downsample to 8x8
    model.add(Conv2D(256, (3, 3), strides=(2, 2), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    # downsample to 4x4
    model.add(Conv2D(256, (3, 3), strides=(2, 2), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    # classifier
    model.add(Flatten())
    model.add(Dropout(0.4))
    model.add(Dense(1, activation='sigmoid'))
    # compile model
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model


# create the discriminator
d_model = define_discriminator()
d_model.summary()


# define generator model
def define_generator(latent_dim):
    model = Sequential()
    # foundation for 4x4 image
    n_nodes = 256 * 4 * 4
    model.add(Dense(n_nodes, input_dim=latent_dim))
    model.add(Reshape((4, 4, 256)))
    # upsample to 8x8
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=4, padding="same"))
    model.add(Activation("relu"))
    # upsample to 16x16
    model.add(UpSampling2D())
    model.add(Conv2D(64, kernel_size=4, padding="same"))
    model.add(Activation("relu"))
    # upsample to 32x32
    model.add(UpSampling2D())
    model.add(Conv2D(32, kernel_size=4, padding="same"))
    model.add(Activation("relu"))
    # upsample to 64x64
    model.add(UpSampling2D())
    model.add(Conv2D(32, kernel_size=4, padding="same"))
    model.add(Activation("relu"))
    # output layer
    model.add(Conv2D(3, (3, 3), activation='tanh', padding='same'))
    return model


# create the generator
g_model = define_generator(latent_dim)
g_model.summary()


# define the combined generator and discriminator model, for updating the generator
def define_gan(g_model, d_model):
    # make weights in the discriminator not trainable
    d_model.trainable = False
    # connect them
    model = Sequential()
    # add generator
    model.add(g_model)
    # add the discriminator
    model.add(d_model)
    # compile model
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt)
    return model


# create the gan
gan_model = define_gan(g_model, d_model)
gan_model.summary()


# @title Add auxiliary helping functions
# get real samples
def get_real_samples(dataset, n_samples):
    # choose random instances
    ix = randint(0, dataset.shape[0], n_samples)
    # retrieve selected images
    X = dataset[ix]
    # generate 'real' class labels (1)
    y = ones((n_samples, 1))
    return X, y


# generate points in latent space as input for the generator
def generate_latent_points(latent_dim, n_samples):
    # generate points in the latent space
    x_input = randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    x_input = x_input.reshape(n_samples, latent_dim)
    return x_input


# use the generator to generate fake samples
# also add labels indicating their fakeness
def generate_fake_samples(g_model, latent_dim, n_samples):
    # generate points in latent space
    x_input = generate_latent_points(latent_dim, n_samples)
    # predict outputs
    X = g_model.predict(x_input)
    # create 'fake' class labels (0)
    y = zeros((n_samples, 1))
    return X, y


# plot generated images
def display_images(examples, n=3):
    # scale from [-1,1] to [0,1]
    examples = (examples + 1) / 2.0
    # plot images
    for i in range(n * n):
        # define subplot
        pyplot.subplot(n, n, 1 + i)
        # turn off axis
        pyplot.axis('off')
        # plot raw pixel data
        pyplot.imshow(examples[i])
    pyplot.show()
    pyplot.close()


# evaluate the discriminator, plot generated images, save generator model
def summarize_performance(epoch, g_model, d_model, dataset, latent_dim, n_samples=150):
    # prepare real samples
    X_real, y_real = get_real_samples(dataset, n_samples)
    # evaluate discriminator on real examples
    _, acc_real = d_model.evaluate(X_real, y_real, verbose=0)
    # prepare fake examples
    x_fake, y_fake = generate_fake_samples(g_model, latent_dim, n_samples)
    # evaluate discriminator on fake examples
    _, acc_fake = d_model.evaluate(x_fake, y_fake, verbose=0)
    # summarize discriminator performance
    print('>Accuracy real: %.0f%%, fake: %.0f%%' % (acc_real * 100, acc_fake * 100))
    # save plot
    display_images(x_fake)
    # save the generator model tile file
    filename = 'upsample_generator_model_%03d.h5' % (epoch + 1)
    g_model.save(filename)


# train the generator and discriminator
def train(g_model, d_model, gan_model, dataset, latent_dim, n_epochs=150, n_batch=128):
    bat_per_epo = int(dataset.shape[0] / n_batch)
    half_batch = int(n_batch / 2)
    # manually enumerate epochs
    for i in range(n_epochs):
        # enumerate batches over the training set
        for j in range(bat_per_epo):
            # get randomly selected 'real' samples
            X_real, y_real = get_real_samples(dataset, half_batch)
            # update discriminator model weights
            d_loss1, _ = d_model.train_on_batch(X_real, y_real)
            # generate 'fake' examples
            X_fake, y_fake = generate_fake_samples(g_model, latent_dim, half_batch)
            # update discriminator model weights
            d_loss2, _ = d_model.train_on_batch(X_fake, y_fake)
            # prepare points in latent space as input for the generator
            X_gan = generate_latent_points(latent_dim, n_batch)
            # create a goal of discriminater not detecting any fakes
            y_gan = ones((n_batch, 1))
            # update the generator via the discriminator's error
            g_loss = gan_model.train_on_batch(X_gan, y_gan)
            # summarize loss on this batch
            print('>%d, %d/%d, d1=%.3f, d2=%.3f g=%.3f' %
                  (i + 1, j + 1, bat_per_epo, d_loss1, d_loss2, g_loss))
        # evaluate the model performance, sometimes
        if (i + 1) % 10 == 0:
            summarize_performance(i, g_model, d_model, dataset, latent_dim)


# train model
train(g_model, d_model, gan_model, X, latent_dim)

X, _ = generate_fake_samples(g_model, 100, 9)
display_images(X)