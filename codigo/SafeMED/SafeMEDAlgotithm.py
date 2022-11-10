import heapq
import pandas as pd
from collections import deque
import time
import os
from PlotSafeRoute import Plot


def CreateGraph(df):
    V = df['origin'].unique()   # Set of vertices
    G = dict()                  # Graph

    for i in V:                 # We add smaller dictionaries for every vertex v into the graph
        subG = dict()
        G[i] = subG
        
    for j in range(len(df)):
        # We assemble the graph :)

        # For oneway routes
        if df.iloc[j]['oneway'] is False:
            G[df.iloc[j]['origin']][df.iloc[j]['destination']] = (df.iloc[j]['harassmentRisk'],df.iloc[j]['length'])
            G[df.iloc[j]['destination']][df.iloc[j]['origin']] = (df.iloc[j]['harassmentRisk'],df.iloc[j]['length'])
        else:
            G[df.iloc[j]['origin']][df.iloc[j]['destination']] = (df.iloc[j]['harassmentRisk'],df.iloc[j]['length'])

    return G


def Dijkstra(G, Origin, Destination, Op: int): # G: Graph, Origin: Starting Vertex, Destination: FInal Vertex

    # MinPV will store the minimum weight, and the predecesor thrown by Dijkstra's algorithm
    MinPV = {v: [float('inf'), ''] for v in G}

    MinPV[Origin][0] = 0
    MinPV[Origin][1] = None

    H = [(0, Origin, 0, 0)]
    
    while len(H) > 0:

        CurrentPathValue, CurrentVertex, ActualDistance, ActualRisk = heapq.heappop(H)
      
        if CurrentVertex == Destination:
            PathTaken = deque()

            Predecessor = Destination
            PathTaken.append(Predecessor)

            while Predecessor is not Origin:
                Predecessor = MinPV[Predecessor][1]
                PathTaken.append(Predecessor)
            
            print("For the equation number " + str(Op) + " the final values are:")
            print("Average risk: " + str(ActualRisk/(len(PathTaken)-1)) +"\nTotal Distance: "+ str(ActualDistance) + "\n")
            return PathTaken

        if CurrentPathValue > MinPV[CurrentVertex][0]:
            continue

        for Adyacente, Item in G[CurrentVertex].items():    

            # Item[0] = Risk = R
            # Item[1] = Distance = D

            if Op == 1:
                PathValue = CurrentPathValue + (1/2)*Item[1] + 100*Item[0]
            elif Op == 2:
                PathValue = CurrentPathValue + 100*Item[0] + 100*Item[1]
            elif Op == 3:
                PathValue = CurrentPathValue + Item[1]**Item[0]


            Distancia = ActualDistance + Item[1]
            Riesgo = ActualRisk + Item[0]
            try:
                if PathValue < MinPV[Adyacente][0]:
                    MinPV[Adyacente][0] = PathValue
                    MinPV[Adyacente][1] = CurrentVertex
                    heapq.heappush(H, (PathValue, Adyacente, Distancia, Riesgo))
            except KeyError:
                continue


def main():
    # Conventions: G-> Graph; V-> Set of vertices of G; E-> Set of Edges of G

    os.system('cls')

    print('Welcome to SafeMed; This program reduces harrasment risk and distance given an initial and final coordinate :)')

    print('\nInput the origin coordinates: ')
    Origin = str(input())

    print('\nInput the destination coordinates:')
    Destination = str(input())

    print('\nPlease stand by, this only will take a few seconds\n')


    start_time = time.time()

    df = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")       # df: dataframe of the .csv file
    df = df.fillna({"harassmentRisk": df["harassmentRisk"].mean()})     # We fill the NaNs in risk with the mean

    G = CreateGraph(df)

    AlgTime = time.time()

    Plot.CreatePlot(Dijkstra(G, Origin, Destination, 1), Dijkstra(G, Origin, Destination, 2), Dijkstra(G, Origin, Destination, 3))

    print("T_Programme: --- %s seconds ---" % (time.time() - start_time))
    print("T_Dijkstra: --- %s seconds ---\n" % (time.time() - AlgTime))

    print('Thanks! Be safe')

main()


"""
The following coordinates were used for the test cases:
    - Eafit = (-75.5778046, 6.2029412)
    - U_Medellin = (-75.6101004, 6.2312125)
    - U_Antioquia = (-75.5694416, 6.2650137)
    - U_Nacional = (-75.5762232, 6.266327)
    - Luis Amigó = (-75.5832559, 6.2601878) 
    - Pueblito Paisa = (-75.5808252, 6.2339338) 
    - Estación Alpujarra = (-75.5724095, 6.2421442)
    - Parque de los Pies Descalzos = "(-75.5757997, 6.2456824)
    - Jardin Infantil Heidelberg (La Estrella) = (-75.6456992, 6.1667406)
    - Hotel Dann Carlton = (-75.5703436, 6.2077406)
    - Loma de los Bernal = (-75.6064698, 6.2178043) 
    - Vía San Jerónimo = (-75.6909483, 6.338773)
    - Parque San Antonio De Prado = (-75.6560151, 6.1853283) 
    - Mall San Lucas = (-75.5660742, 6.1804998)

"""
