#!/usr/bin/env python
# coding: utf-8

import argparse
# from sklearn.model_selection import train_test_split
from PIL import Image, ImageTk
import numpy as np
from numpy import asarray
import os
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askdirectory, askopenfilename

np.random.seed(0)
window = tk.Tk()
window.title('Perceptron')
window.geometry('600x600')
# window.configure(bg='grey')

class Perceptron(object):
	def __init__(self, arg):
		super(Perceptron, self).__init__()
		self.arg = arg
		self.weights = np.random.randn(self.arg.input_dim+1).reshape(-1,1) #(d+1,1)
		def square(x):
			return ((x**2) + (5*x))
		if self.arg.transform==1:
			self.transformation = square
		else:
			self.transformation = lambda x: x
		self.learning_rate = arg.learning_rate if self.arg.learning_rate is not None else 0.1
		# self.cutoff = args.cutoff if args.cutoff is not None else 0.5 

	def forward(self, x,y):
		# import pdb;pdb.set_trace()
		self.x = np.concatenate((self.transformation(x), np.ones((x.shape[0],1))), axis=-1) #(?,d+1)
		# print(self.x)
		out = self.x@self.weights #(?,1)
		self.t = (out >= 0) + 0 #(?,1)
		self.y = y.reshape(-1,1)
		return self.t

	def backward(self):
		self.weights += np.sum(self.learning_rate*(self.y-self.t)*self.x, axis=0).reshape(-1,1)

	def loss(self):
		"""no of incorrect samples"""
		# print(self.x[(self.y-self.t).reshape(-1)==0])
		# print(self.y.reshape(-1))
		# print(self.t.reshape(-1))
		return np.sum(self.y-self.t) 



def main(args):
	if args.data == 'image':
		image = Image.open(args.train_image)
		data = asarray(image)
		image2 = Image.fromarray(data)
		size = data.shape
		label = Image.open(args.train_label)
		ldata = asarray(label)
		label2 = Image.fromarray(ldata)
		X = []
		Y = []
		for i in range(size[0]):
			for j in range(size[1]):
				X.append(data[i][j]/255)
				Y.append(ldata[i][j]/255)
		X_train = np.array(X)
		Y = np.array(Y).astype('int')
		# assert (Y[:,0] == Y[:,1]).all() and (Y[:,0] == Y[:,2]).all()
		y_train = Y[:]

		image = Image.open(args.test_image)
		data = asarray(image)
		image2 = Image.fromarray(data)
		size = data.shape
		label = Image.open(args.test_label)
		ldata = asarray(label)
		label2 = Image.fromarray(ldata)
		X = []
		Y = []
		for i in range(size[0]):
			for j in range(size[1]):
				X.append(data[i][j]/255)
				Y.append(ldata[i][j]/255)
		X_test = np.array(X)
		Y = np.array(Y).astype('int')
		shp = ldata.shape
		# assert (Y[:,0] == Y[:,1]).all() and (Y[:,0] == Y[:,2]).all()
		y_test = Y[:]

		# X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2, random_state=42)
		args.input_dim = 3  # 3 channel input


	model = Perceptron(args)
	
	#Training the model
	print('='*20+'Training'+'='*20)
	for epoch in range(args.epoch):
		t = model.forward(X_train,y_train)
		print(f'Epoch {epoch+1}: No. of misclassifications = {abs(model.loss())}')
		model.backward()

	#Testing the model
	if args.data == 'image':
		print('='*20+'Testing'+'='*20)
		t = model.forward(X_test,y_test)
		out = t.reshape(shp)
		im = Image.fromarray(np.uint8(out*255))
		im.save(os.path.join(args.out_image, 'output.png'))
		print(f'Test accuracy: {100-100.00*abs(model.loss())/ len(y_test)}%')
		accuracy_label = tk.Label(text=f'Test accuracy: {100-100.00*abs(model.loss())/ len(y_test)}%')
		accuracy_label.place(x=200, y=5)




parser = argparse.ArgumentParser(description='Inputs to model run script')
parser.add_argument('-f')  # add this dummy argument to overcome system exit error
parser.add_argument('--input_dim', default=2, type=int, help='input dimension of features')
parser.add_argument('--epoch', default=None, type=int, help='number of epochs')
parser.add_argument('--transform', default=None, type=int, help='do non linear transformation on input or not')
parser.add_argument('--learning_rate', default=None, type=float, help='learning rate')
parser.add_argument('--data', default=None, type=str, help='training and eval data')
parser.add_argument('--train_image', default=None, type=str, help='Training image path')
parser.add_argument('--train_label', default=None, type=str, help='Label image path')
parser.add_argument('--test_image', default=None, type=str, help='Test image path')
parser.add_argument('--test_label', default=None, type=str, help='Test label path')
parser.add_argument('--out_image', default=None, type=str, help='Predicted image store path')
args = parser.parse_args()


# tkinter windgets

def linearTransformation():
	args.transform = 0
	text = 'linear transformation'
	tk.Label(window, text=text).place(x=5, y=300)
	return
def nonLinearTransformation():
	args.transform = 1
	text = 'non linear transformation'
	tk.Label(window, text=text).place(x=5, y=300)
	return
Rb1 = tk.Radiobutton(window, text='Linear Transformation',value=1, command=linearTransformation).place(x=5, y=3)
Rb2 = tk.Radiobutton(window, text='Non Linear Transformation', value=2, command=nonLinearTransformation).place(x=5, y=30)

args.data = 'image'
currdir = os.getcwd()

def loadTrainImage():
	args.train_image = askopenfilename(parent=window, initialdir=currdir, title='Please select train image')
	text = 'Training image loaded'
	tk.Label(window, text=text).place(x=5, y=320)
	return

train = tk.Button(window, text='Train image',width=20,bg='grey',fg='white', command=loadTrainImage).place(x=5, y=60)

def loadTrainLable():
	args.train_label = askopenfilename(parent=window, initialdir=currdir, title='Please select train label')
	text = 'Training image label loaded'
	tk.Label(window, text=text).place(x=5, y=340)
	return

trainL = tk.Button(window, text='train image lable',width=20,bg='grey',fg='white', command=loadTrainLable).place(x=5, y=90)

def loadTestImage():		
	args.test_image = askopenfilename(parent=window, initialdir=currdir, title='Please select test image')
	text = 'Testing image loaded'
	tk.Label(window, text=text).place(x=5, y=360)
	return

test = tk.Button(window, text='Test image',width=20,bg='grey',fg='white', command=loadTestImage).place(x=5, y=120)

def loadTestLable():
	args.test_label = askopenfilename(parent=window, initialdir=currdir, title='Please select test label')
	text = 'Testing image label loaded'
	tk.Label(window, text=text).place(x=5, y=380)
	return

testL = tk.Button(window, text='test image lable',width=20,bg='grey',fg='white', command=loadTestLable).place(x=5, y=150)

def output():
	args.out_image = askdirectory(parent=window, initialdir=currdir, title='Please select a directory to store test output')
	text = 'output directory is provided'
	tk.Label(window, text=text).place(x=5, y=400)
	return

outputbutton = tk.Button(window, text='output directiony',width=20,bg='grey',fg='white', command=output).place(x=5, y=180)

# print(args)
def learningRate():
	args.learning_rate = float(simpledialog.askstring(title="Learning rate",
 								  prompt="Set the learning rate for this run \n Press OK for default value"))
	text = f'Learning rate is set to {args.learning_rate}'
	tk.Label(window, text=text).place(x=5, y=420)
	return

learning_rate_b = tk.Button(window, text='set learning rate',width=20,bg='grey',fg='white', command=learningRate).place(x=5, y=210)

def Epoches():
	args.epoch = int(simpledialog.askstring(title="Epochs",
 								  prompt="Set the number of epochs for this run \n Press OK for default value"))
	text = f'No. of Epoches is set to {args.epoch}'
	tk.Label(window, text=text).place(x=5, y=420)
	return

epoch_b = tk.Button(window, text='set epoch value',width=20,bg='grey',fg='white', command=Epoches).place(x=5, y=240)

def run():
	main(args)
	image = Image.open(args.out_image + '/' + 'output.png')
	newsize = (400,400)
	image_out = image.resize(newsize)
	imagetest = ImageTk.PhotoImage(image=image_out)
	labelimg = tk.Label(image=imagetest)
	labelimg.image = imagetest
	labelimg.place(x=200, y=30)

mainButton = tk.Button(window, text='run Perceptron',width=20,bg='grey',fg='white', command=run).place(x=5, y=270)

window.mainloop()