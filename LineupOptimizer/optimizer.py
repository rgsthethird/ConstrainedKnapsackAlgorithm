# Optimizes a multiple-dimension 0-1 knapsack problem given weight
# and quantity constraints. Developed to optimize Draftkings soccer lineups
# Algorithm runs in O(n^2*W*Q) time, where n = number of players,
# W = maximum weight (price), and Q = maximum quantity (number of players)
# By Rob Schwartz
class Optimizer:

    def __init__(self):
        # Maximum "weight". Keep as small as possible. For instance, because
        # DK lineups have a maximum of $50,000 with player prices always
        # being a multiple of 100, I divided all of them by 500.
        self.W = 500
        # Maximum number of players
        self.Q = 6
        # Example players. Need to prepare import option via text file.
        self.players = {1:[20.6011924202255,74,'Habib Diallo'],
                        2:[6.21613679055888,96,'Callum Wilson'],
                        3:[23.4303910706968,80,'Ludovic Ajorque'],
                        4:[10.0843816462449,56,'Flavien Tait'],
                        5:[7.87882240308121,58,'Sean Longstaff'],
                        6:[5.29716152416648,70,'Kenny Lala'],
                        7:[5.55726120793809,70,'Joelinton'],
                        8:[11.0372519954224,28,'Stefan Mitrović'],
                        9:[7.23640011386239,54,'Nathaniel Clyne'],
                        10:[9.67861468032334,48,'Anthony Caci'],
                        11:[10.8619083965267,74,'Jonjo Shelvey'],
                        12:[7.01658970082632,52,'Jamal Lewis'],
                        13:[11.3510559614062,130,'Andros Townsend'],
                        14:[6.65530397215877,48,'Damien Da Silva'],
                        15:[5.38762148897945,46,'Scott Dann'],
                        16:[6.72054984634418,74,'Jeremy Doku'],
                        17:[8.05941943223172,80,'Hamari Traoré'],
                        18:[13.225729262209,78,'Faitout Maouassa'],
                        19:[5.09471889244654,32,'Jean-Eudes Aholou'],
                        20:[6.9178852453127,34,'Cheikhou Kouyaté'],
                        21:[11.3698669766008,60,'Mohamed Simakan'],
                        22:[4.07032916928809,38,'James McArthur'],
                        23:[6.58819494354805,38,'Javier Manquillo'],
                        24:[10.7079914723422,62,'Miguel Almirón'],
                        25:[3.31144520116847,42,'Federico Fernández'],
                        26:[8.32665209016247,86,'Sehrou Guirassy'],
                        27:[9.38040527496683,54,'Jean-Ricner Bellegarde'],
                        28:[9.95369954822981,88,'Benjamin Bourigeaud'],
                        29:[7.95980768611809,52,'Eduardo Camavinga'],
                        30:[3.80775843812509,64,'Patrick van Aanholt'],
                        31:[6.01422114388434,88,'Jordan Ayew']}
        # Eventual final matrix that shows path to optimal score/lineup
        self.knapsackMatrix = None
        self.captain = []
        self.topScore = 0

    # Optimizes lineup given players, max weight, and max quantity
    # Essentially tracks the best possible score you can get for each
    # Maximum weight (increasing from 0...W), each number of players
    # considered (0...n), and each quantity (0...Q). It then determines
    # the best value for each new variable by using the pre-calculated
    # values stored in prior matrices. In other words - dynamic programming
    # with multiple dimensions.
    def optimize(self):
        n = len(self.players)
        # Tracks top score for each captain
        topScore = 0

        # Tests each player as captain
        for playerKey in self.players.keys():
            # Captains earn 1.5x value at 1.5x weight
            player = self.players[playerKey]
            captain = player[2]
            playerValue = player[0]
            playerPrice = player[1]
            player[0] = playerValue*1.5
            player[1] = int(playerPrice*1.5)

            # Creates new set of matrices for each captain
            knapSack = self.initKnapsack(self.W)
            # m represents the index of a matrix (typical 0-1 knapsack DP matrix) in the knapsack
            # Also acts as the upper quantity limit for that matrix
            for m in range(self.Q):
                # i and w are the matrix dimensions
                for i in range(1,n+1):
                    for w in range(0,self.W+1):
                        # Because I'm using numbers 0...n-1 as keys in self.players, bi and wi
                        # can be called using matrix row iterator i
                        bi = self.players[i][0]
                        wi = self.players[i][1]
                        # If the player weight < current acceptable weight
                        if wi <= w:
                            # Conditions that determine current cell value based on prior values
                            if bi + knapSack[m][i-1][w-wi][0] > knapSack[m][i-1][w][0] and knapSack[m][i-1][w-wi][1] <= m:
                                if knapSack[m-1][i-1][w-wi][0] <= m and knapSack[m][i-1][w-wi][0] < knapSack[m-1][i-1][w-wi][0]:
                                    knapSack[m][i][w][0] = bi + knapSack[m-1][i-1][w-wi][0]
                                    knapSack[m][i][w][1] = knapSack[m-1][i-1][w-wi][1]+1
                                else:
                                    knapSack[m][i][w][0] = bi + knapSack[m][i-1][w-wi][0]
                                    knapSack[m][i][w][1] = knapSack[m][i-1][w-wi][1]+1

                            elif bi + knapSack[m-1][i-1][w-wi][0] > knapSack[m][i-1][w][0] and knapSack[m-1][i-1][w-wi][1] <= m:
                                knapSack[m][i][w][0] = bi + knapSack[m-1][i-1][w-wi][0]
                                knapSack[m][i][w][1] = knapSack[m-1][i-1][w-wi][1]+1

                            elif m > 0 and knapSack[m-1][i-1][w-wi][1] < m and bi + knapSack[m-1][i-1][w-wi][0] > knapSack[m][i-1][w][0]:
                                knapSack[m][i][w][0] = bi + knapSack[m-1][i-1][w-wi][0]
                                knapSack[m][i][w][1] = knapSack[m-1][i-1][w-wi][1]

                            else:
                                knapSack[m][i][w] = knapSack[m][i-1][w]
                        else:
                            knapSack[m][i][w] = knapSack[m][i-1][w]

            # If top score from this captain is the best yet encountered, save score, captain, and matrix.
            if knapSack[self.Q-1][n][self.W][0] > self.topScore:
                self.topScore = knapSack[self.Q-1][n][self.W][0]
                self.captain = player
                self.knapsackMatrix = knapSack
            # Return captain to normal value and weight
            player[0] = playerValue
            player[1] = playerPrice

    # Using final matrix, backtracks to determine which players comprise final score
    def findPlayers(self, knapSack):
        i = len(self.players)
        k = self.W
        m = self.Q
        players = []
        price = 0
        # Backtracking and adding players as they're found
        while i > 0 and k > 0 and m > 0:
            if knapSack[m-1][i][k] != knapSack[m-1][i-1][k]:
                players.append(self.players[i][2])
                price += self.players[i][1]
                k = k-self.players[i][1]
                i = i-1
                if knapSack[m-1][i][k][1] == m or knapSack[m-2][i][k][0] > knapSack[m-1][i][k][0]:
                    m = m-1
            else:
                i = i-1
        return [players, price]

    # Creates knapsack with max matrix width of W
    def initKnapsack(self, W):
        knapSack = [ [ [ [-1,0] for i in range(W+1) ] for j in range(len(self.players)+1) ] for k in range(self.Q)]
        for quantity in knapSack:
            for player in quantity:
                player[0] = [0,0]
            quantity[0] = [ [0,0] for i in range(W+1) ]
        return knapSack

    def getKnapsack(self):
        return self.knapsackMatrix

    def getCapStats(self):
        return [self.captain[2],self.captain[0],self.captain[1]]

    # Cements captain's data (changes captain's value/weight in self.players)
    def cementCaptain(self):
        for playerKey in self.players.keys():
            if self.players[playerKey][2] == self.captain[2]:
                self.players[playerKey][0] = self.players[playerKey][0]*1.5
                self.players[playerKey][1] = int(self.players[playerKey][1]*1.5)
                break

    def getTopScore(self):
        return self.topScore
