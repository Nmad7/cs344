Cat Face GAN - A Calvin cs344 final project

The purpose of this project is to explore the implimentation of DCGAN architecture
 in the creation of AI generated cat images. The data for this GAN was taken from 
 https://www.kaggle.com/spandan2/cats-faces-64x64-for-generative-models.
 
 DCGAN.py trains a DCGAN and saves the generator as a model every 10 epochs
 
 upsamplingConvolution.py trains a GAN using upsampling and convolutional layers in the generator
 
 To use:
 replace the path variable in line 1 with the path to the folder of the dataset or the dataset in numpy array form. 
 Replace the convertFolder variable in line 2 with True if the path is a folder path, if the path is to a numpy array put False.
