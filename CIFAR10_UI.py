# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI1_5.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog
# from tensorflow.keras.datasets import cifar10
from torchvision import models
from torchsummary import summary
# import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import PIL.Image as Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import os

NUM_EPOCH = 30

d = {
    0 : 'airplane',
    1 : 'automobile',
    2 : 'bird' ,
    3:'cat' ,
    4:'deer',
    5:'dog',
    6:'frog',
    7:'horse',
    8:'ship',
    9:'truck' 
}
# Model structure
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn.setGeometry(QtCore.QRect(40, 60, 151, 41))
        self.loadBtn.setObjectName("loadBtn")
        self.loadBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn_2.setGeometry(QtCore.QRect(40, 120, 151, 41))
        self.loadBtn_2.setObjectName("loadBtn_2")
        self.loadBtn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn_3.setGeometry(QtCore.QRect(40, 180, 151, 41))
        self.loadBtn_3.setObjectName("loadBtn_3")
        self.loadBtn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn_4.setGeometry(QtCore.QRect(40, 240, 151, 41))
        self.loadBtn_4.setObjectName("loadBtn_4")
        self.loadBtn_5 = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn_5.setGeometry(QtCore.QRect(40, 300, 151, 41))
        self.loadBtn_5.setObjectName("loadBtn_5")
        self.loadBtn_6 = QtWidgets.QPushButton(self.centralwidget)
        self.loadBtn_6.setGeometry(QtCore.QRect(40, 360, 151, 41))
        self.loadBtn_6.setObjectName("loadBtn_6")
        self.ImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.ImageLabel.setGeometry(QtCore.QRect(210, 60, 500, 500))
        self.ImageLabel.setText("")
        # self.ImageLabel.setScaledContents(True)
        self.ImageLabel.setObjectName("ImageLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # loadbutton
        self.loadBtn.clicked.connect(self.loadImg)
        self.loadBtn_2.clicked.connect(self.Show9Image)
        self.loadBtn_3.clicked.connect(self.ShowVGGStructure)
        self.loadBtn_4.clicked.connect(self.ShowAugmentation)
        self.loadBtn_5.clicked.connect(self.LoadTrainingImg)
        self.loadBtn_6.clicked.connect(self.Inference)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadBtn.setText(_translate("MainWindow", "Load Image"))
        self.loadBtn_2.setText(_translate("MainWindow", "1. Show Train Image"))
        self.loadBtn_3.setText(_translate("MainWindow", "2. Show Model Structure"))
        self.loadBtn_4.setText(_translate("MainWindow", "3. Show Data Augmentation"))
        self.loadBtn_5.setText(_translate("MainWindow", "4. Show Accuracy and Loss"))
        self.loadBtn_6.setText(_translate("MainWindow", "5. Inference"))

    def loadImg(self):
        fname = QFileDialog.getOpenFileName(caption='Open File', directory='./')
        ImgPath = fname[0]
        txt = fname[0].split("/")
        # self.fileNameLbl.setText(txt[-1])
        self.image = cv2.imread(ImgPath)
        if(self.image is None):
            print('load image failed\n')
            return
        # print(self.image.shape)
        height, width, channel = self.image.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.image.data.tobytes(), width, height, bytesPerLine, QImage.Format_BGR888)
        self.ImageLabel.setPixmap(QPixmap.fromImage(qImg).scaled(self.ImageLabel.width(),
                                                        self.ImageLabel.height(), 
                                                        QtCore.Qt.KeepAspectRatio))
        self.ImageLabel.show()

    def Show9Image(self):
        # Cifar-10 data
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        # Data
        trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
        testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
        trainLoader = torch.utils.data.DataLoader(trainset, batch_size=9, shuffle=True, num_workers=2)
        testLoader = torch.utils.data.DataLoader(testset, batch_size=9, shuffle=False, num_workers=2)

        dataiter = iter(trainLoader)
        images, labels = next(dataiter)
        images = images/2 + 0.5 # unnormalize
        images = images.numpy()
        images = np.transpose(images, (0,2,3,1))
        # (x_img_train,y_label_train), (x_img_test,y_label_test)=cifar10.load_data()
        # print('train:',x_img_train.shape)
        # print('test:',len(x_img_test))
        # print('label shape', y_label_train.shape)
        # print('label type', type(y_label_train))

        # Random choose
        # random_index = np.random.choice(x_img_train.shape[0], 9, False)
        # loadImages = x_img_train[random_index]
        # labels = y_label_train[random_index]

        classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

        # Plot image
        fig = plt.figure()
        for i in range(images.shape[0]):
            ax = fig.add_subplot(3, 3, i+1)
            ax.imshow(images[i])
            ax.set_title(classes[labels[i]])
        plt.subplots_adjust(top=0.919,
                            bottom=0.089,
                            left=0.027,
                            right=0.973,
                            hspace=0.727,
                            wspace=0.0)
        plt.show()
        # self.CreateLabel()

        # for i in range(loadImages.shape[0]):
        #     height, width, channel = loadImages[i].shape
        #     bytesPerLine = 3 * width
        #     qImg = QImage(loadImages[i].data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        #     self.ImageLabel[i].setScaledContents(True)    # Fixed to label size
        #     self.ImageLabel[i].setPixmap(QPixmap.fromImage(qImg))
        #     _translate = QtCore.QCoreApplication.translate
        #     self.TextLabel[i].setText(_translate("MainWindow", d[labels[i][0]]))

        #     self.ImageLabel[i].show()
        #     self.TextLabel[i].show()

    def CreateLabel(self):
        """
        self.ImageLabel = []
        self.TextLabel = []
        width = 160
        height = 160
        top = 60
        left = 210
        margin_left = 50
        margin_top = 50
        for i in range(3):
            for j in range(3):
                index = i*3+j
                imageLabel = QtWidgets.QLabel(self.centralwidget)
                self.ImageLabel.append(imageLabel) 
                self.ImageLabel[index].setGeometry(QtCore.QRect(left+width*j+margin_left*j, top+height*i+margin_top*i, width, height))
                self.ImageLabel[index].setScaledContents(True)
                self.ImageLabel[index].setObjectName("ImageLabel"+str(index))
                # self.ImageLabel[index].show()
                textLabel = QtWidgets.QLabel(self.centralwidget)
                self.TextLabel.append(textLabel) 
                self.TextLabel[index].setGeometry(QtCore.QRect(left+width*j+margin_left*j, top+height*i+margin_top*i-30, width, 30))
                self.TextLabel[index].setObjectName("TextLabel"+str(index))
                # self.TextLabel[index].show()
                # _translate = QtCore.QCoreApplication.translate
                # self.TextLabel[index].setText(_translate("MainWindow", "TextLabel"+str(index)))
        """

    def ShowVGGStructure(self):
        # vggmodel = tf.keras.applications.vgg19.VGG19(weights='imagenet')
        # vggmodel.summary()

        vggmodel = models.vgg19()
        summary(vggmodel.cuda(), (3,224,224))
        print(vggmodel)

    def ShowAugmentation(self):
        # Convert BGR to RGB
        img_pil = Image.fromarray(np.uint8(self.image[:,:,::-1]))
        transform = transforms.Compose([
            transforms.RandomRotation(180,expand=False),
            transforms.RandomResizedCrop(img_pil.size),
            transforms.RandomHorizontalFlip()
        ])
        augImages = []
        for i in range(3):
            img = transform(img_pil)
            augImages.append(img)
        
        fig = plt.figure()
        for i in range(3):
            ax = fig.add_subplot(1,3,i+1)
            ax.imshow(augImages[i])
        plt.subplots_adjust(
            top=0.969,
            bottom=0.031,
            left=0.031,
            right=0.971,
            hspace=0.2,
            wspace=0.356
        )
        plt.show()

    def LoadTrainingImg(self):
        self.ImageLabel.setPixmap(QPixmap('accuracy.png').scaled(self.ImageLabel.width(),
                                                            self.ImageLabel.height(),
                                                            QtCore.Qt.KeepAspectRatio))
        self.ImageLabel.show()
         
    def Inference(self):
        height, width, channel = self.image.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.image.data.tobytes(), width, height, bytesPerLine, QImage.Format_BGR888)
        self.ImageLabel.setPixmap(QPixmap.fromImage(qImg).scaled(self.ImageLabel.width(),
                                                        self.ImageLabel.height(), 
                                                        QtCore.Qt.KeepAspectRatio))
        self.ImageLabel.show()

        # Load Model
        filepath = 'models/vgg19_kaggle_cifar10_224x224_best.pth'
        if os.path.exists(filepath):
            model = torch.load(filepath)
        else:
            print(f'File {filepath} does not exist')
            return
        
        model.eval()
        # GPU
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        # device = 'cpu'
        model.to(device)
        
        image_size = (224, 224)
        convert_tensor = transforms.Compose([transforms.ToTensor(), transforms.Resize(image_size, antialias=True)])
        predictImg = convert_tensor(self.image)
        predictImg = predictImg.unsqueeze(0)
        predictImg = predictImg.to(device)

        with torch.no_grad():
            prediction = model(predictImg)
            prediction = torch.nn.functional.softmax(prediction, dim=1)
            confidence, predicted = torch.max(prediction.data, 1)
        # print(confidence.shape)
        # print(predicted.shape)

        classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        # Show result
        self.ResultLabel = QtWidgets.QLabel(self.centralwidget)
        self.ResultLabel.setGeometry(QtCore.QRect(210, 30, 500, 30))
        self.ResultLabel.setText("Confidence = %.2f\nPrediction Label: %s" %(confidence, classes[predicted]))
        self.ResultLabel.setObjectName("ResultLabel")
        self.ResultLabel.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())