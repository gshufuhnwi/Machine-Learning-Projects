import operator
import pandas as pd
import Metrics

class Cnn:
        def getClosestPoint(data, point):
        	distances = []
        	length = len(point)-1
        	for x in range(len(data)):
        		dist = Metrics.Metrics().euclideanDistance(point, data.iloc[x], length)
        		distances.append((data.iloc[x], dist))
        	distances.sort(key=operator.itemgetter(1)) #sort dict based on distance between points
        	return distances[0][0]
    
        def getReducedDataset(self, data):
                Z = pd.DataFrame(columns= data.columns.values)
                count = 0
                while(True):
                        count += 1
                        #marked is going to mark the points which will be removed after each iteration
                        marked = pd.DataFrame(columns= data.columns.values)
                        for index, row in data.iterrows():
                            x = data.loc[index]
                            train = data.drop(index)
                            #get the colsest point
                            NB = Cnn.getClosestPoint(train, x)
                            #if class not equal to add to Z and marked for removal
                            if x[-1] != NB[-1]:
                                Z = Z.append(NB)
                                marked = marked.append(NB)
                        print('count :: ', count)
                        #if no point is marked, the previous and new Z is same terminate
                        #for tackling infinity check count
                        if len(marked) == 0 or count == 5:
                                return Z    
                        #check wether there is are points in the data.
                        if (len(data) - len(marked)) <= 2:
                                return Z
                        data = data.drop(marked.index.values.tolist())
                

 



