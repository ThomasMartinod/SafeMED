import pandas as pd
import heapq
from collections import deque


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


def Dijkstra(G, Origin, Destination): # G: Graph, Origin: Starting Vertex, Destination: FInal Vertex

    # MinPV will store the minimum weight, and the predecesor thrown by Dijkstra's algorithm
    MinPV = {i: [float('inf'), ""] for i in G} 

    MinPV[Origin][0] = 0            # PathValue from A to A is 0
    MinPV[Origin][1] = None         # Predecesor of the origin is set as none

    H = [(0, Origin)]   # H is an ordered pair having the priority, or the possible ways
    

    while len(H) > 0:
        CurrentPathValue, CurrentVertex = heapq.heappop(H)
        # heappop returns the min element and  its position in the graph (current vertex)
      
        if CurrentVertex == Destination:      # If the current is the destination, we have finished
            PathTaken = []                      # This list will indicate the Path Given by the Dijkstras algorithm

            Returning = Destination             # This variable will return all the way from the destination to the origin to know the path taken  
            PathTaken.append(Destination)       # Last step is the destination

            while Returning is not Origin:      # We add the path taken
                Returning = MinPV[Returning][1]
                PathTaken.append(Returning)

            PathTaken = list(reversed(PathTaken)) # Finally we reverse the order to have the path in the right order
            PathTaken.append(CurrentPathValue)
            return PathTaken

        elif CurrentPathValue > MinPV[CurrentVertex][0]:    # We may avoid calculations if we reserve ourselves to shorter potencial pahts
            continue

        else:
            for Adjacent, Risk in G[CurrentVertex].items():
                PathValue = (1/2)*CurrentPathValue + (100)*(Risk[0] * Risk[1])          # Formula for finding the inverse satisfaction
                # The assigned value for the edge
                try:                                        # Dijkstra's algorithm
                    if PathValue < MinPV[Adyacent][0]:
                        MinPV[Adjacent][0] = PathValue
                        MinPV[Adjacent][1] = CurrentVertex
                        heapq.heappush(H, (PathValue, Adjacent))
                except KeyError:
                    continue



def main():
    # Conventions: G-> Graph; V-> Set of vertices of G; E-> Set of Edges of G

    df = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")       # df: dataframe of the .csv file
    df = df.fillna({"harassmentRisk": df["harassmentRisk"].mean()})     # We fill the NaNs in risk with the mean

    G = CreateGraph(df)

    print(Dijkstra(G, '(-75.5778046, 6.2029412)', '(-75.5762232, 6.266327)'))
    

main()

"""
The following coordinates were used for the test cases:
    - Eafit = "(-75.5778046, 6.2029412)"
    - U_Medellin = "(-75.6101004, 6.2312125)"
    - U_Antioquia = "(-75.5694416, 6.2650137)"
    - U_Nacional = "(-75.5762232, 6.266327)"
    - LuisAmigo = "(-75.5832559, 6.2601878)" """
