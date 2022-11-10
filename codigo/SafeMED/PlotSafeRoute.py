import gmplot

class Plot:

    def CreatePlot(R1, R2, R3):
        
        Path1 = []
        for i in range(len(R1)):
            el = str(R1.pop())
            CommaPosition = el.find(",")

            yCoordinate = float(el[1:CommaPosition])
            xCoordinate = float(el[CommaPosition+1:-1])

            Path1.append((xCoordinate, yCoordinate))
        

        Path2 = []
        for i in range(len(R2)):
            el = str(R2.pop())
            CommaPosition = el.find(",")

            yCoordinate = float(el[1:CommaPosition])
            xCoordinate = float(el[CommaPosition+1:-1])
            
            Path2.append((xCoordinate, yCoordinate))
        

        Path3 = []
        for i in range(len(R3)):
            el = str(R3.pop())
            CommaPosition = el.find(",")

            yCoordinate = float(el[1:CommaPosition])
            xCoordinate = float(el[CommaPosition+1:-1])

            Path3.append((xCoordinate, yCoordinate))

    
        U1, T1 = zip(*Path1)
        U2, T2 = zip(*Path2)
        U3, T3 = zip(*Path3)
        
        myGmap = gmplot.GoogleMapPlotter(6.22, -75.6, 14)  
        
        myGmap.plot(U1, T1, 'aquamarine', edge_width = 10.0)             # First equation
        myGmap.plot(U2, T2, 'mediumslateblue', edge_width = 7.0)        # Second equation
        myGmap.plot(U3, T3, 'violet', edge_width = 4.0)                 # Third equation
        
        myGmap.marker(U1[-1],T1[-1] , "red", title="Destination")
        myGmap.marker(U1[0],T1[0] , "red", title="Origin")
        
        myGmap.draw('C:\\Users\\thomm\\Desktop\\SafeMED\\Map.html')
