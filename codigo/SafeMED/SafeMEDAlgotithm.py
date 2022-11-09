import heapq
import pandas as pd
from collections import deque
from PlotSafeRoute import Plot
import math as mt


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
            
            print("Riesgo promedio: " + str(ActualRisk/(len(PathTaken)-1)) +"\nDistancia acumulada de: "+ str(ActualDistance))
            return PathTaken

        if CurrentPathValue > MinPV[CurrentVertex][0]:
            continue

        for Adyacente, Risk in G[CurrentVertex].items():
            if Op == 1:
                Comb = CurrentPathValue
            elif Op == 2:
                Comb = 100*Risk[0] + 100*Risk[1] + CurrentPathValue
            elif Op == 3:
                Comb = CurrentPathValue + Risk[0]**Risk[1]


            Distancia = ActualDistance + Risk[1]
            Riesgo = ActualRisk + Risk[0]
            try:
                if Comb < MinPV[Adyacente][0]:
                    MinPV[Adyacente][0] = Comb
                    MinPV[Adyacente][1] = CurrentVertex
                    heapq.heappush(H, (Comb, Adyacente, Distancia, Riesgo))
            except KeyError:
                continue


def main():
    # Conventions: G-> Graph; V-> Set of vertices of G; E-> Set of Edges of G

    print('Welcome to SafeMed; This program does something')

    print('Input the origin coordinates: ')
    Origin = str(input())

    print('Input the destination coordinates')
    Destination = str(input())

    df = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")       # df: dataframe of the .csv file
    df = df.fillna({"harassmentRisk": df["harassmentRisk"].mean()})     # We fill the NaNs in risk with the mean

    G = CreateGraph(df)

    Plot.CreatePlot( Dijkstra(G, Origin, Destination, 1), Dijkstra(G, Origin, Destination, 2), Dijkstra(G, Origin, Destination, 3))



main()


"""
The following coordinates were used for the test cases:
    - Eafit = "(-75.5778046, 6.2029412)"
    - U_Medellin = "(-75.6101004, 6.2312125)"
    - U_Antioquia = "(-75.5694416, 6.2650137)"
    - U_Nacional = "(-75.5762232, 6.266327)"
    - LuisAmigo = "(-75.5832559, 6.2601878)" """
