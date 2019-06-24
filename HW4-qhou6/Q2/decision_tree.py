from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        # self.tree = []
        self.tree = {}
        self.colList = []
        pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        atree = {}
        max_gain = 0
        split_attribute = ''
        split_val = ''
        colX = self.reformX(X)
        colCheckMatrix = []
        for col in range(len(colX)):
            colCheckMatrix.append(self.findCheckPointOneColumn(colX[col]))

        if entropy(y) != 0:
            for col in range(len(X[0])):
                for row in range(len(colCheckMatrix[col])):
                    if col not in self.colList:
                        (X_left, X_right, y_left, y_right) = partition_classes(X, y, col, colCheckMatrix[col][row])

                        
                        new_y = [y_left]+[y_right]
                        if len(y_left) != 0 and len(y_right) != 0:
    
                            if information_gain(y, new_y) > max_gain:
                                max_gain = information_gain(y, new_y)
                                split_attribute = col
                                split_val = colCheckMatrix[col][row]
                                bestSet = (X_left, X_right, y_left, y_right)
    


        if (split_val != '' and split_attribute != ''):
            
            atree = {"attr": split_attribute, "val": split_val, "right": [], "left": []}
            self.colList.append(split_attribute)
            atree["left"] = self.learn(bestSet[0], bestSet[2])

            atree["right"] = self.learn(bestSet[1], bestSet[3])
            self.tree = atree
            return atree
        else:
            self.tree = {"result": y[0]}
            return {"result": y[0]}

    def reformX(self, X):
        newX = []
        for n in range(len(X[0])):
            newX.append([])
        for row in range(len(X)):
            for col in range(len(X[0])):
                newX[col] = newX[col] + [X[row][col],]
        return newX
    
    def findCheckPointOneColumn(self, col):
        # int

        if isinstance(col[0], float) or isinstance(col[0], int):
            maxC = max(col)
            minC = min(col)
            if (maxC != minC):
                return [minC, (maxC-minC)/4, (maxC-minC)/2, (maxC-minC)/4 * 3, maxC]
            else:
                return [minC]
        else:
            return list(set(col))


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
 
        tempTree = self.tree
        while ("result" not in tempTree.keys()):

            if isinstance(tempTree["val"], int) or isinstance(tempTree["val"], float):


                if record[tempTree["attr"]] <= tempTree["val"]:
                    tempTree = tempTree["left"]
                else:
                    tempTree = tempTree["right"]
            else:
                if record[tempTree["attr"]] == tempTree["val"]:
                    tempTree = tempTree["left"]
                else:
                    tempTree = tempTree["right"]

        return tempTree["result"]



