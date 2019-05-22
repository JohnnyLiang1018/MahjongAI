class MahjongAgent:
    wan = [0,1,0,1,0,1,1,0,3]
    so = [0,0,0,1,2,0,1,1,1]
    pin = [0,0,0,1,1,1,0,0,4]
    honor = [0,0,0,0,0,0,0]
    hands = [wan,so,pin]
    partition = {"sequence_middle, 2, wan", "sequence_middle,7, wan", "sequence_complete", "single"}
    
    # sequence_two-way * 0.7 * 0.24
    # sequence_middle * 0.01

    def handPartition(self):
        for t in self.hands:
            for x in range(len(t)):
                if(t[x] == 4):
                    #1 KAN or 1 triplet + possible sequence
                    self.partition["KAN-triplet"] = x
                elif(t[x] == 3):
                    # 1 triplet or 1 pair + possible sequence
                    self.partition["triplet"] = x
                elif(t[x] == 2):
                    # 1 pair
                    self.partition["pair"] = x
                if(x < len(t)-2 and t[x] == 1):
                    if(t[x+1]==0 and t[x+2]):
                        # sequence middle
                        self.partition["sequence_middle"] = x
                    if(t[x+1]==1 and t[x+2]==0):
                        #sequence two-way
                        self.partition["sequence_two-way"] = x 
                    if(t[x+1]==1 and t[x+2]==1):
                        #sequence complete
                        self.partition["sequence_complete"] = x

dummy = MahjongAgent()
dummy.handPartition()
print(len(dummy.partition))
print(dummy.partition)


