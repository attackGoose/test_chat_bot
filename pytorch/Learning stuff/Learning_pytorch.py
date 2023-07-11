#this file is for learning pytorch by building a text generator
#https://pytorch.org/tutorials/
#https://youtu.be/V_xro1bcAuA


import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(torch.__version__)

### creating a tensor
scalar = torch.Tensor(7) #has no dimensions, one number

print(scalar.shape) #returns the number we gave it

vector = torch.Tensor([7, 7]) #has 1 dim since its a 1 dim array
print(vector.shape)

MAXTRIX = torch.Tensor([[7, 8],
                        [9, 10]])

TENSOR = torch.Tensor([[[1,2,3],
                        [3,6,9],
                        [2,4,5]]])
print(TENSOR.shape)


### random tensors: (creates more accurate training data)

rand_tensor = torch.rand(3, 4) #creates a tensor of size 3, 4 (matrix since there's 2 dimensions) 
print(rand_tensor, rand_tensor.ndim)


#creating a random image tensor:
rand_image_size_tensor = torch.rand(size=(224, 224, 3)) #hgiht, width, color (RGB), also the size parameter isn't neededsince its the first parameter
print(rand_image_size_tensor.shape, rand_image_size_tensor.ndim)

zero_tensor = torch.zeros(size=(3, 4))

ones_tensor = torch.ones(size=(3, 4))

#the default data type of these tensors are float32, although u can customize that

#creating a tensor that has a range:
one_to_ten = torch.arange(start=1, end=10, step=2) #goes up by 2
print(one_to_ten)

ten_zeros = torch.zeros_like(one_to_ten) #creates a tensor of the same size as one_to_ten of all zero values


#NOTE: Tensor Datatypes:

float_32_tensor = torch.tensor([3.0, 6.0, 9.0],
                               dtype = None, #type of the tensor: float_32, you can see a list of datatypes by googling "tensor datatypes pytorch"
                               device = None, #IMPORTANT: cuda uses gpu, operations on tensors need to be on the same device
                               requires_grad = False) #track gradiants with this tensor's operations?

float_16_tensor = float_32_tensor.type(torch.float16) #changing the type of a tensor
print(float_16_tensor)


print(float_16_tensor * float_32_tensor) #no error for some reason, dunno why, some operations will raise an error if they're not the same datatype

int_32_tensor = torch.tensor([3, 6, 9], dtype=torch.int64)

print(int_32_tensor*float_32_tensor) #also works

### 3 big errors: 
# Tensor Wrong Datatype, use tensor.dtype to see the datatype
# Tensor not in the right shape, use tensor.shape to get the shape
# tensor not on the right device, use tensor.device to get the device

some_tensor = torch.rand(3, 4)
print(some_tensor, some_tensor.shape, some_tensor.dtype, some_tensor.device)


###Tensor Operations:

tensor = torch.tensor([1, 3, 6])
print(torch.add(tensor, 10)) #adds 100 to all the elements 

#for multiplication, try to always use torch's implimentation other than the basic implimentations like + and -, there's 2 types, element wise multiplication and dot multiplication/matrix multiplication
print(tensor*tensor) 

print(torch.matmul(tensor, tensor)) #prints out the products of the elements in the matrix after multiplication

# Rules for matrix multiplications: 
# 1. Inner dimentions must match: (2, 3) times (3, 2) will work since the inner dimensions both = 3, but (3, 2) times (3, 2) won't work since the inner dimensions aren't the same
print(torch.matmul(torch.rand([3,2]), torch.rand([2, 3])))

# 2. the resulting matrix will have the dimensions of the outer dimensions
print(torch.matmul(torch.rand([4,2]), torch.rand([2, 3])).shape) #creates a matrix with dimensions [4, 3]


# (Shape Error, a very common error in deep learning)
TensorA = torch.tensor([[1, 2],
                        [3, 4],
                        [5, 6]])
TensorB = torch.tensor([[7, 8],
                        [9, 10],
                        [11, 12]])

#changing the shape of a tensor using transpose to switch the axis/dimensions of a tensor
TensorB = TensorB.T
print(TensorB, TensorB.shape)

print(torch.mm(TensorA, TensorB), torch.mm(TensorA, TensorB).shape) #mm = matmul, alias for writing less code, sideNote: @ is the sign fo matrix multiplication


##Tensor Aggrigation, finding the min, max, mean, sum, etc of a tensor

test_tensor = torch.arange(0, 100, 10)

#you could write this in 2 ways, both are shown below
print(test_tensor.min(), torch.min(test_tensor))
print(test_tensor.max(), torch.max(test_tensor))
print(test_tensor.type(torch.float32).mean(), torch.mean(test_tensor.type(torch.float32))) #gives us an error with datatype, so we have to change the datatype to what it wants
print(test_tensor.sum(), torch.sum(test_tensor))


#finding positional Datatypes, finds the position in the tensor that holds that value
print(f"index of the max position: {test_tensor.argmax()}\nindex of the min position: {test_tensor.argmin}")

#current time stamp: 2:59:28

"""
Solving Shape issues: reshaping, stacking, squeezing, and unsqueezing tensors:
reshaping - reshapes an input tensor to a defined shape
view - returns the view of an input tensor of a certain shape but keeps the same memory as the original tensor
stacking - combines multiple tensors on top of each other (vstack) or side by side (hstack)
squeeze - removes all '1' dimensions from a tensor
unsqueeze - adds a '1' dimension from a tensor
permute - returns the view of a tensor with the dimensions permuted (swapped) in a way

the purpose of these is to manipulate the dimensions of a tensor to resolve the shape issues
"""

another_tensor = torch.arange(1.0, 10.0)
print(another_tensor)
tensor_reshaped = another_tensor.reshape(3, 3) #changes the size/dimensions of a tensor into another one, the reshape has to be compatable with the original tensor
print(tensor_reshaped, another_tensor.reshape(9, 1))

another_tensorsView = another_tensor.view(1, 9)
print(another_tensorsView, another_tensorsView.shape)
#another_tensorView is a view of another_tensor, so by changing another_tensorsView, you will also change another_tensor

another_tensorsView[:, 0] = 5 #gets all rows of the tensor, and takes their value at the zeroth index and sets it equal to 5
print(another_tensor, another_tensorsView)


##Stacking Tensors
x = torch.arange(1.0, 10.0)

#there's also vstack and hstack, look into those later
x_stack = torch.stack([x, x, x, x], dim=0)
print(x_stack)

#squeezing tensors
x_squeeze = torch.squeeze(x)
print(f"original tensor: {x}\nsqueezed tensor: {x_squeeze}")

x_unsqueeze = x_squeeze.unsqueeze(dim=0) #it will add the extra dim into the dim given, which in this case is the 1st part of the dim, run the code and test to see more
print(f"previous target: {x_squeeze}\nprevious shape = {x_squeeze.shape}\nnew tensor: {x_unsqueeze}\nnew tensor shape: {x_unsqueeze.shape}")

#permuting tensors
x_original = torch.rand(size=(224, 224, 3)) #height, width, color_channels (RGB)
x_permuted = x_original.permute(2, 0, 1) #rearranges the color channel into the 0th index, and shifts the rest back by 1, shifts axis 0 -> 1, 1-> 2, 2-> 0
print(f"original shape: {x_original.shape}\npermuted shape: {x_permuted.shape}")

#time stamp = 3:23:27