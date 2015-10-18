
# Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
# License: BSD 3 clause

# Standard scientific Python imports
#import matplotlib.pyplot as plt

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
import numpy
import os
from gif_reader import get_gif_num_frames
from PIL import Image

#class Images:

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

def read_images(file_names):
    images = []
    for file_name in file_names:
        images.append(read_image_file(file_name))
    return images

def read_targets(csv_file_name, gif_file_order, tag_index):
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
        for l in lines:
            vals = l.split(',')
            tags[vals[0]] = vals[1 + tag_index]
        return [tags[x] for x in gif_file_order]
    raise ValueError("Couldn't parse data correctly")

def nasa_dataset(gif_names):
    res = MyDataSet()
    
    res.images = numpy.array(read_images(gif_names))
    res.target = read_targets("results.csv", gif_names, 0)
    return res

gifs = find_gif_names("images")

# The digits dataset
#digits = datasets.load_digits()
digits = nasa_dataset(gifs)

# The data that we are interested in is made of 8x8 images of digits, let's
# have a look at the first 3 images, stored in the `images` attribute of the
# dataset.  If we were working from image files, we could load them using
# pylab.imread.  Note that each image must have the same size. For these
# images, we know which digit they represent: it is given in the 'target' of
# the dataset.
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
classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])

# Now predict the value of the digit on the second half:
expected = digits.target[n_samples / 2:]
predicted = classifier.predict(data[n_samples / 2:])

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
#for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    #plt.subplot(2, 4, index + 5)
    #plt.axis('off')
    #plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    #plt.title('Prediction: %i' % prediction)

#plt.show()
