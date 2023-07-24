##timestamp: 14:13:33

"""
computer vision could be used for classification (both binary and multi-class), image recognition, object detection, spliting different sections of an image or segmenting an image
and many more, this model is going ot be using the convolutional neuro network model but the transformer model have also been shown to have good performance on this as well

About data:
the data is going to be of shape:
Shape = [batch_size, width, height, color_channels] color channel = RGB or etc, height and width of the image, and batch size is the the number of models processed before model 
parameters are updated
ex. Shape = [32, 224, 224, 3] #this is the most common sizes
or: Size = [None, 224, 224, 3] #also note that these parameters can vary

outputshape = [amount_of_possible_results]

About Convolutional Neuro Network (CNNs):

common architecture: (there are many more)
 - input image(s)
 - input layer
 - convolutional layer - extract/learns the most important features from the target imgaes, can be created with torch.nn.ConvXd() 
    (where X is a number/can be multiple values) like torch.nn.Conv2d(), which works with a bias vector and a weight matrix, which opperate over the input
 - hidden activation/non-linear activation - adds non-linearity to the learned features, usually torch.ReLU(), although can be many more
 - pooling layer - reduces dimensionality of the learned image features, uses torch.nn.MaxPool2d for max and torch.nn.AvgPool2d() for an average
 - output layer/linear layer - takes learned features and outputs them in the shapes of the target labels, uses torch.nn.Linear(out_features={number_of_classes}) 
    ex, it would be 3 for fitting into the classes of pizza, steak, or sushi since there are a total of 3 classes/categories
 - output activation - converts output logits into prediction values, usually torch.sigmoid() for binary classification or torch.softmax() for multi-class classification
"""

## other useful stuff that pytorch uses
"""
torchvision - main torch library for vision
torchaudio - audio
torchtext - text problems/stuff
TorchRec - recommendation systems
TorchData - data pipelines 
TorchServe - serving pytorch models

# for torchvision:
torchvision.datasets - getting datasets and data loading functions for computer vision
torchvision models - get pretrained computer vision models (already trained models)
torchvision.transforms - functions for manipulating for images/vision data to be suitable for use with an ML model
torch.utils.data.Datasets - base dataset class for pytorch, you can create your own custom datasets
torch.utils.data.DataLoader - creates a python iterable over a dataset
"""

#pytorch
import torch
from torch import nn

#torchvision stuff
import torchvision
from torchvision import transforms, datasets
from torchvision.transforms import ToTensor #this converts a PIL image or a numpy.ndarray to a tensor

#for visualizing 
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader

print(f"Torch Version: {torch.__version__}\nTorchvision version: {torchvision.__version__}")


### Creating/getting a dataset:

#using Built-in datasets: https://pytorch.org/vision/stable/datasets.html

#using Fashion MNIST:
train_data = datasets.FashionMNIST(
    root="data", #what to download data to
    train=True, #what do we want the training dataset
    download=True, #do we want to download it
    transform=torchvision.transforms.ToTensor(), #transforms the type to a tensor
    target_transform=None #keeping the label/target as it is
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=torchvision.transforms.ToTensor(),
    target_transform=None #keep the label/taget as it is
)  

##viewing data information

print(len(train_data), len(test_data))

image, label = train_data[0]
print(image, label)

class_names = train_data.classes
print(class_names)

class_to_idx = train_data.class_to_idx #shows the type to its corresponding index 
print(class_to_idx)

#checking the shape: (label doesn't have a shape since its only one number)
print(f"image shape: {image.shape} -> [color_channels, height, width]\n Image label shape: {label}, image label: {class_names[label]}")

#since this dataset is in all black and white, there's only 1 color channel, 1 for all white, 0 for all black, and inbetween for a mix of both

#shows all the possible labels
print(train_data.targets)


##Visualizing:

#the image shape is [color_channels, width, height] but matplotlib wants [width, height, color channel (optional)]
plt.imshow(image.permute(1, 2, 0), cmap="gray") 
plt.title(class_names[label])
plt.axis(False)
plt.show()

#showing the image without the color channel (gets rid of all dims with only 1 or 0 as a size) (its the same as above)
#plt.imshow(image.squeeze()) 
#plt.show()

# plotting more images:

fig = plt.figure(figsize=(9, 9))
rows, cols = 4, 4

for i in range(1, rows*cols+1):
   random_index = torch.randint(low=0, high=len(train_data), size=[1]).item()
   print(random_index)
   img, label = train_data[random_index]
   fig.add_subplot(rows, cols, i) #at the ith index, add a subplot
   plt.imshow(img.squeeze(), cmap="gray")
   plt.title(class_names[label])
   plt.axis(False)

plt.show()

## these images might not be able to be modeled with linear lines so we might need non-linearity

## preparing DataLoader to transform the datasets to a python iterable/batches/mini_batches since it is more computationally efficient 
# (spliting a dataset of 60000 images into 32 images to look at at a time rather than 60000) (batch_size of 32 is common)
# it also gives our neuro network more chances to update its gradients per epoch (we get one update per batch, so having more batches is better, but we also need enough data
# in each batch to make an accurate adjustment on)


#using DataLoader to batch and shuffle the data into smaller pieces to train:

#hyperparameters:
BATCH_SIZE = 32

train_dataloader = DataLoader(dataset=train_data,
                              batch_size=BATCH_SIZE,
                              shuffle=True #incase our dataset has order, we mix up the dataset
                              )

test_dataloader = DataLoader(dataset=test_data,
                             batch_size=BATCH_SIZE,
                             shuffle=True)

print(f"DataLoaders: {train_dataloader, test_dataloader}")
print(f"Length of train_dataloader: {len(train_dataloader)} batches of {BATCH_SIZE}...")
print(f"Length of train_dataloader: {len(test_dataloader)} batches of {BATCH_SIZE}...")

train_features_batch, train_labels_batch = next(iter(train_dataloader)) #gets the next batch of the iterable train_dataloader, 
print(train_features_batch.shape, train_labels_batch.shape)

#interacting with a dataloader:
torch.manual_seed(42)
random_index = torch.randint(low=0, high=len(train_features_batch), size=[1]).item()

img, label = train_features_batch[random_index], train_labels_batch[random_index]

plt.imshow(img.squeeze(), cmap="gray")
plt.title(class_names[label])
plt.axis(False)
print(f"image size: {img.shape}")
print(f"Label: {label}, label size: label.shape")

plt.show()


# building a baseline model: (a baseline model is a simple model that will improve with subsequent models/experiments)
# In other words, start simple, add complexity when necessary

#creating a flatten layer: 
flatten_model = nn.Flatten()

#get a single sample
x = train_features_batch[0]

#flatten the sample:
output = flatten_model(x)

print(f"Shape before flattening: {x.shape}\nShape after Flattening: {output.shape}")

## shows that nn.Flatten layer combines the dimensions into a single vector space

#has no non-linearities
class FashioMNISTModelV0(nn.Module):
   def __init__(self, input_shape: int, hidden_units: int, output_shape: int):
      super().__init__()
      self.layer_stack = nn.Sequential(
         nn.Flatten(),
         nn.Linear(in_features=input_shape, out_features=hidden_units),
         nn.Linear(in_features=hidden_units, out_features=output_shape),
         # sizenote: you need to make sure that your input and output shapes line up with where they need to be in the model
      )

   def forward(self, x: torch.Tensor) -> torch.Tensor:
      return self.layer_stack(x)

model_0 = FashioMNISTModelV0(
   input_shape=28*28, #this is the size of the model after it gets flattened
   hidden_units=10, #amount of units in the hidden layer
   output_shape=len(class_names) #one for every class
).to("cpu")

dummy_x = torch.rand(1, 1, 28, 28) #batch of 1, color channel of 1, size of 28x28
print(model_0(dummy_x)) #the flatten combines all the dimensions into a singular vector 

#now we get one logit per class (we can use softmax to get the prediction labels and etc)

#how the flatten layer works example: timestamp: 15:34:12


#current timestamp: 15:35:55
