# Adapted from the ML examples in scikit learn.
# Original Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
# License: BSD 3 clause

# Standard scientific Python imports
#import matplotlib.pyplot as plt

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
import numpy
from PIL import Image

import os
import time
from datetime import datetime

#class Images:

NUM_FILES=30

class MyDataSet:
    images = numpy.ndarray(shape=(3,3))
    target = []

def find_gif_names(images_dir):
    dirs = os.listdir(images_dir)
    files = []
    for d in dirs:
        for f in os.listdir(os.path.join(images_dir, d)):
            file_name = os.path.join(images_dir, d, f)
            files.append(file_name)
    return files
    

def read_image_file(file_name):
    """
    Reads an image file from a file name.
    Requires that it's a gif. Returns the grayscale of that gif
    as a 2d array of pixels.
    """
    im = Image.open(file_name)
    ints = [ord(b) for b in im.tobytes()]
    return ints

def read_images(file_names, n_samples):
    images = []
    for file_name in file_names[0:n_samples]:
        #yield read_image_file(file_name)
        images.append(read_image_file(file_name))
    return images
    

def read_gif_names(csv_file_name, tag_index, n_samples):
    gif_files = []
    with open(csv_file_name) as f:
        csv_data = f.read()
        lines = csv_data.split('\n')
        tags = {}
        num_lines = 0
        for l in lines:
            if num_lines == 0:
                num_lines += 1
                continue
            num_lines += 1
            vals = l.split(',')
            filename = vals[0]
            gif_files.append(filename)
    return gif_files[0:n_samples]

def read_targets(csv_file_name, tag_index, gif_files, n_samples):
    """
    csv file holds data like
      f1 t1 t2 t3
      f2 t1 t2 t3
    where f1 and f2 are the file names, and ti holds the whether
    the ith tag is 0 or 1 for the file f1, f2
    
    gif_file_order gives the order that the files are given in the array of
    data inputs to the ML algo. 
    
    tag index is the column of the tag we're interested in.
    """
    with open(csv_file_name) as f:
        csv_data = f.read()
        lines = csv_data.split('\n')
        tags = {}
        num_lines = 0
        for l in lines:
            if num_lines == 0:
                num_lines += 1
                continue
            num_lines += 1
            vals = l.split(',')
            filename = vals[0]
            classification=vals[1+tag_index]
            if classification == "true":
                classification = 1
            else:
                classification = 0
            tags[filename] = classification

        result = [tags[x] for x in gif_files if x in tags]
        result = result[0:n_samples]
        return result
    raise ValueError("Couldn't parse data correctly")

def nasa_dataset(n_samples):
    res = MyDataSet()    
    gif_names = read_gif_names("results.csv", 0, n_samples)
    res.target = read_targets("results.csv", 0, gif_names, n_samples) 
    res.images = numpy.array(read_images(gif_names, n_samples))
    return res



####################################################
# Begin.
#

curr_time = datetime.now()

#gifs = find_gif_names("images")

# The digits dataset
digits = nasa_dataset(NUM_FILES)

# The data that we are interested in is made of 8x8 images of digits, let's
# have a look at the first 3 images, stored in the `images` attribute of the
# dataset.  If we were working from image files, we could load them using
# pylab.imread.  Note that each image must have the same size. For these
# images, we know which digit they represent: it is given in the 'target' of
# the dataset.
#for image in digits.images:
#    print(image)

images_and_labels = list(zip(digits.images, digits.target))
#for index, (image, label) in enumerate(images_and_labels[:4]):
    #plt.subplot(2, 4, index + 1)
    #plt.axis('off')
    #plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    #plt.title('Training: %i' % label)

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# We learn the digits on the first half of the digits
try:
    print(digits.images[:n_samples / 2])
    print(digits.target[:n_samples / 2])
    classifier.fit(digits.images[:n_samples / 2], digits.target[:n_samples / 2])
    classifier.fit(digits.images[:n_samples / 2], digits.target[:n_samples / 2])
    
    # Now predict the value of the digit on the second half:
    expected = digits.target[n_samples / 2:]
    predicted = classifier.predict(data[n_samples / 2:])

    print(expected)
    print(predicted)

    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

    images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
except:
    print("finished with errors.")
    time_finished = datetime.now()
    print(curr_time)
    print(time_finished)
    raise

time_finished = datetime.now()
print(curr_time)
print(time_finished)

    #for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    #plt.subplot(2, 4, index + 5)
    #plt.axis('off')
    #plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    #plt.title('Prediction: %i' % prediction)
    
    #plt.show()
