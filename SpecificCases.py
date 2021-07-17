
class Specific_Functions():
    """
    The functions in this class is not general at all, modify freely for your project
    """
    def folder_name_to_X_and_Y(self):
          """
          This function is a highly specific to my project. Modifying this function for your project might be efficient and useful.
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
