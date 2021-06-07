import glob
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import pickle
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import keras
from keras.layers import Activation, Conv2D, Flatten, Dense, Dropout, Conv3D
from keras.optimizers import SGD, Adadelta, Adagrad, Adam, Adamax, RMSprop, Nadam
from keras.layers.noise import AlphaDropout, GaussianDropout, GaussianNoise
from keras.layers.convolutional import MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
import datetime

class PictureProcessing():
    def __init__(self):
        """You can modify the _init_ process that can be set through config.ini"""
        self.picture_data_folder_name = "data2"
        self.folder_name_for_models = "models"
        self.folder_name_for_backups = "backup"
        self.image_size = 256 #it could be 200, 50 or anything as you like.
    def main(self):
        X,Y = self.folder_name_to_X_and_Y()
        self.XYpickler(X,Y)

    def path2vector(self,path):
        img = self.pic2data(path)
        return img
    def pic2data(self, picjpg, image_size = 256):
        image_size = self.image_size
        image=Image.open(picjpg)
        image=image.convert('RGB')
        #image = image.quantize(4)
        #image = image.point(lambda x: 0 if x < 230 else x)
        image=image.resize((image_size,image_size))
        data=np.asarray(image)
        X = np.array(data)
        return X


    def folder_name_to_X_and_Y(self):
        """
        This is a highly specified function. Modifying this function for your project might be efficient and useful.
        """
        folders = glob.glob(os.path.join(self.picture_data_folder_name,"*"))
        X = []
        Y = []
        ct = 0
        for folder in folders:
            if "drone" in folder:
                specific_picture_pathjpg = glob.glob(os.path.join(folder,"*.jpg"))
                specific_picture_pathJPEG = glob.glob(os.path.join(folder,"*.JPEG"))
                specific_picture_pathjpg.extend(specific_picture_pathJPEG)
                for picpath in specific_picture_pathjpg:
                    X.append(self.path2vector(picpath))
                    Y.append(0)
                    ct += 1
            else:
                print(folder)
                elsefolders = glob.glob(os.path.join(folder,"*"))
                for elsefolder in elsefolders:
                    specific_picture_path = glob.glob(os.path.join(elsefolder,"*.jpg"))
                    for picpath in specific_picture_path:
                        X.append(self.path2vector(picpath))
                        Y.append(1)
                        ct += 1
        print(len(X),len(Y),ct)
        return X, Y

    def create_folder_if_None_exists(self,name):
        if not os.path.exists(name):
            os.makedirs(name)
            print("The folder named '{}' had not existed so I created it.".format(name))
        else:
            print("The folder named '{}' already exists so nothing was executed.".format(name))

    def get_currenttime_numeral(self):
        d = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return d

    def XYpickler(self,X,Y):
        """
        1.Pickle X and Y as forms of X.sav and Y.sav. 2.Also create a new folder called backup if there is None.
        3.Then, save 'X_{}.sav'.format(datetimenoworsomething) and 'Y_{}.sav'.format(datetimenoworsomething) , as backups.
        """
        #procedure 1.
        #folder_name_for_models = "models"
        self.create_folder_if_None_exists(self.folder_name_for_models)
        filenameX = (os.path.join(self.folder_name_for_models,"X.sav"))
        pickle.dump(X, open(filenameX, "wb"))
        filenameY = (os.path.join(self.folder_name_for_models,"Y.sav"))
        pickle.dump(Y, open(filenameY, "wb"))
        #procedure 2.
        #folder_name_for_backups = "backup"
        self.create_folder_if_None_exists(self.folder_name_for_backups)
        d = self.get_currenttime_numeral()
        filenameX = (os.path.join(self.folder_name_for_backups,"X_{}.sav".format(d)))
        pickle.dump(X, open(filenameX, "wb"))
        filenameY = (os.path.join(self.folder_name_for_backups,"Y_{}.sav".format(d)))
        pickle.dump(Y, open(filenameY, "wb"))

    #Utilities below.
    def XYloader(self):
        """
        This one is not used amongst this sector or file. Use it by importing it from somewhere else.
        """
        filenameX = (os.path.join(self.folder_name_for_models,"X.sav"))
        with open(filenameX, mode="rb") as f:
            X = pickle.load(f)
        filenameY = (os.path.join(self.folder_name_for_models,"Y.sav"))
        with open(filenameY, mode="rb") as f:
            Y = pickle.load(f)
        return X,Y
    def file2data(self, filepath, image_size = 256): #not recommended when you would need a labeled dataset. Use pic2data instead in that case.
        image_size = self.image_size
        X = []
        files=glob.glob(filepath+"/*.png")
        print(len(files))
        files.extend(glob.glob(filepath+"/*.jpg"))
        print(len(files))
        for pic in files:
            image=Image.open(pic)
            image=image.convert('RGB')
            #image = image.convert("L")
            image=image.resize((image_size,image_size))
            data=np.asarray(image)
            #up = 0
            #1 = down
            X.append(data)
        X = np.array(X)
        return X
    def XnY2train(self,X, Y, test_size =0.2, Shuffle = True):
        if shuffle == True:
            X,Y = shuffle(X, Y)
        else:
            pass
        x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=test_size)
        #map the files to a file
        xy = (x_train, x_test, y_train, y_test)
        return x_train, x_test, y_train, y_test


#cwd = r"C:\Users\Andre\Pictureprocess\model"
#os.chdir(cwd)
if __name__ == "__main__":
    Picture_processing_ = PictureProcessing()
    Picture_processing_.main()
