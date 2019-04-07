'''
RVGraph
(1) which requests can be pairwise combined: if share > single route then don't pairwise else pair wise
(2) which vehicles can serve which requests individually, given their current passengers
'''
from time import sleep, gmtime, strftime, time
import requests
from googleMapApiAdapter import getDistance, getDistanceMatrix

# redis key name, refer to README for the data struture
RIDE_REQUEST = 'realTimeRideRequest'
DRIVER_LOCATION = 'driverLocation'
DRIVER_ON_GOING_RIDE = 'driverOngoingRide'

'''
{
    ('request1', 'request2'): distance,
    ('request1', 'request3'): distance,
}
'''

class RTVGraph:
    def __init__(self,constraints_param,useGridWorld=False):
        self.rtvGraph = []
        self.maxMatchDistance = constraints_param['maxMatchDistance']
        self.useGridWorld = useGridWorld       

    def _getDistanceMatrix(self, origins, destinations):
        if self.useGridWorld:
            # TODO
            return None
        else:
            return getDistanceMatrix(origins, destinations)                

    def RTVGraphFindFeasibleTrips(self,rvGraph,driverList):
       
        for (request, request2) in rvGraph.requestsGraph:
            for driver in driverList:
                if len(driver["ongoingRide"]) == 0:

                    locationList = []
                    locationList.append( driver['location'] )
                    locationList.append( request['startLocation'])
                    locationList.append( request2['startLocation'] )
                    locationList.append( request['endLocation'])
                    locationList.append( request2['endLocation'] )
                    distanceMatrix = self._getDistanceMatrix(locationList, locationList)

                    delaylist = []
                    delaylist.append((distanceMatrix[0][1] + distanceMatrix[1][2]-distanceMatrix[0][2])+(distanceMatrix[1][2]+distanceMatrix[2][3]-distanceMatrix[1][3]))
                    delaylist.append(distanceMatrix[0][1] + distanceMatrix[1][3]+ distanceMatrix[3][2]- distanceMatrix[0][2])
                    delaylist.append(distanceMatrix[1][0] + distanceMatrix[0][2]+distanceMatrix[2][3]- distanceMatrix[1][3])
                    delaylist.append((distanceMatrix[1][0] + distanceMatrix[0][3]-distanceMatrix[1][3])+(distanceMatrix[0][3] + distanceMatrix[3][2]-distanceMatrix[0][2]))
                    
                    delayMin=min(delaylist)
                    index=delaylist.index(min(delaylist))

                if delayMin<self.maxMatchDistance:  
                    if index<2:
                        if distanceMatrix[0][1] + distanceMatrix[1][2]<5000:
                            self.rtvGraph.append((driver,request,request2,delayMin,index))
                    else:
                        if distanceMatrix[0][2] + distanceMatrix[2][1]<5000:
                            self.rtvGraph.append((driver,request,request2,delayMin,index))
                   
                   
    
        #self.rtvGraph.extend(rvGraph.rvGraph)

            
                
                                


    '''
    return data structure example
    {
    'driver1':[('request1'),('request2'),delayMin],
    'driver1':[('request2'),('request3'),delayMin]
              
    }
    '''

    

    
