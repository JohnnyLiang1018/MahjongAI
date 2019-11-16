from collections import defaultdict
from GameBoard import GameBoard
import Mahjong_AI
import numpy as np
import pickle

class MahjongAgent:
    wan = [1,1,3,1,2,3,0,0,1]  #0-8
    so = [0,0,0,1,0,0,0,2,1]   #9-17
    pin = [1,1,0,1,0,0,0,0,0]  #18-26
    honor = [0,0,0,0,0,0,0]
    hands = [wan,so,pin]

    hand = []
    open_meld = []
    partition = {}
    efficiency_map = {}
    num_remain_tile = 70
    tile_count = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

    han = 0
    fu = 20
    
    # def __init__(self,gameboard):
        # self.hand = []
        # self.open_meld = []
        # self.gameboard = gameboard
        # self.tile_count = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
        # self.num_remain_tile = 83
        # self.fu = 20
        # self.han = 0

    
    # sequence_two-way * 0.7 * 0.24
    # sequence_middle * 0.01
    # def new_partition(self):
    #     pair = []
    #     for t in self.hands:
    #         sequence = {}
    #         triplet = {}
    #         kang_triplet = []
    #         for x in range(len(t)):
    #             if(t[x] == 4):
    #                 # mark index as kang_triplet
    #                 kang_triplet.append(x)
    #             if(t[x] == 3):
    #                 # mark index as triplet
    #                 print("triplet at:" + str(x))
    #                 triplet.update(str(x),x)
    #             elif(t[x] == 2):
    #                 # mark index as pair
    #                 print("pair at:" + str(x))
    #                 pair.append(x) 
    #             elif(x<=6):
    #                 if(t[x] >= 1 and t[x+1]>=1 and t[x+2]>=1):
    #                     true_count = 0
    #                     if(t[x] >= 3):
    #                         true_count += 1
    #                     if(t[x] >= 3):
    #                         continue
    #                     else:
    #                         # mark index as sequence-complete
    #                         print("sequence complete at:" + str(x))
    #                         sequence.update(str(x),x)
                
    #         for num in sequence:
    #             if (sequence.get(num) in triplet or sequence.get(num+1) in triplet or sequence(num+2) in triplet):
    #                 # mark sequence index with triplet overlap
                    
    #                 print("sequence complete plus pair")
            
    def tenpai_status_check(self,hand):
        return_list = {}
        single_tile = []
        value_list = []
        if(len(hand)%3 == 1):
            return return_list

        if(len(hand) == 14):
            # check seven-pairs
            pair_count = 0
            x = 0
            while x < 13:
                if(hand[x] == hand[x+1]):
                    pair_count += 1
                    x += 2
                else:
                    single_tile.append(hand[x])
                    x += 1
            if(x == 13):
                single_tile.append(hand[x])

            if(pair_count == 7):
                for tile in hand:
                    return_list.setdefault(tile,tile)
                return return_list
            
            if(pair_count == 6):
                return_list.setdefault(single_tile[0],[single_tile[1]])
                return_list.setdefault(single_tile[1],[single_tile[0]])
                return return_list

        if(len(hand) == 2):
            return_list.setdefault(hand[0],[hand[1]])
            return_list.setdefault(hand[1],[hand[0]])
            #print(return_list)
            return return_list
        
        if(len(hand) == 3):

            left_dis = hand[1] - hand[0]
            right_dis = hand[2] - hand[1]

            if(hand[0]//9 == hand[1]//9 and left_dis <= 2):
                if(hand[1] - hand[0] == 2):
                    # sequence-middle
                    return_list.setdefault(hand[2],[hand[1]-1])
                else:
                    # two-way or one-way
                    left = hand[0] - 1
                    right = hand[1] + 1
                    if(left//9 == right//9):
                        # two-way
                        return_list.setdefault(hand[2],[left,right])
                    else:
                        # one-way
                        if(left < 0):
                            return_list.setdefault(hand[2],[right])

                        elif((right-1) % 9 >= 5):
                            return_list.setdefault(hand[2],[left])
                        else:
                            return_list.setdefault(hand[2],[right])

            if(hand[1]//9 == hand[2]//9 and right_dis <= 2):
                if(hand[2] - hand[1] == 2):
                    # sequence-middle
                    return_list.setdefault(hand[0],[hand[2]-1])
                else:
                    # two-way or one-way
                    left = hand[1] - 1
                    right = hand[2] + 1
                    if(left // 9  == right // 9):
                        # two-way
                        return_list.setdefault(hand[0],[left,right])
                    else:
                        if (left < 0):
                            return_list.setdefault(hand[0],[right])
                        # one-way
                        elif((right-1) % 9 >= 5):
                            return_list.setdefault(hand[0],[left])
                        else:
                            return_list.setdefault(hand[0],[right])

        if(len(hand) == 5):
            remain = []
            for x in range(len(hand)-2):
                remain = self.seq_extract(hand,x)
                remain = self.pair_extract(remain)
                remain = self.tri_extract(remain)
                if(len(remain) != 5):
                    # double pair waiting
                    if(len(remain) == 1):
                        y = 0
                        while y < len(hand):
                            if(hand[y] != remain[0]):
                                value_list.append(hand[y])
                                y+=2
                            else:
                                y+=1
                        return_list.setdefault(remain[0],value_list)
                    # print("check point 1")
                    extend_dict = self.tenpai_status_check(remain)
                    for key in extend_dict:
                        if(key in return_list):
                            for item in extend_dict[key]:
                                if (item not in return_list[key]):
                                    return_list[key].append(item)
                        else:
                            return_list.setdefault(key,extend_dict[key])

                    


        if(len(hand) > 5):
            # print("greater 5")
            remain = []
            for x in range(len(hand)-2):
                remain = self.seq_extract(hand,x)
                remain = self.tri_extract(remain)
                if(len(remain) < len(hand)):
                    # print("check point 2")
                    extend_dict = self.tenpai_status_check(remain)
                    for key in extend_dict:
                        if(key in return_list):
                            for item in extend_dict[key]:
                                if (item not in return_list[key]):
                                    return_list[key].append(item)
                        else:
                            return_list.setdefault(key,extend_dict[key])
        
        # print("final:")
        # print(return_list)
        return return_list
          
    
    def pair_extract(self,hand):
        remain = []
        x = 0
        while x < (len(hand)-1):
            if (hand[x] == hand[x+1]):
                x+=2
                continue
            remain.append(hand[x])
            x+=1
        if(x<len(hand)):
            remain.append(hand[x])
        # print("extract pair:")
        # print(remain)
        return remain 
    


    def tri_extract(self,hand):  
        remain = []
        x = 0
        while x < (len(hand)-2):
            if(hand[x] == hand[x+1] == hand[x+2]):
                x+=3
                continue
            remain.append(hand[x])
            x+=1

        if(x<len(hand)):
            remain.append(hand[x])
        if(x<len(hand)-1):
            remain.append(hand[x+1])

        # print("extract tri:")
        # print(remain)
        return remain

    def seq_extract(self,hand,index):
        
        remain = []
        remain.extend(hand[0:index])
        partial_hand = hand[index:]
        index_1_count = 0
        index_2_count = 0
        index_3_count = 0
        index_1_move = 0
        index_2_move = 0
        index_3_move = 0 
        x = 0
        value = partial_hand[0]
        while x < (len(partial_hand)-2):
            
            # print(partial_hand)
            if(index_1_move == 0):
                value = partial_hand[x]
                index_1_count = partial_hand.count(value)
                #print(value)
            
            # no more possible sequences beyong tile 25
            if(value >= 25):
                # print("greater than 15")
                remain.extend(partial_hand[x:])
                return remain
            
            # if three values are within the same type
            if (value // 9 == (value+2) // 9):

                if(index_2_move == 0):
                    index_2_count = partial_hand.count(value+1)
                    #print(value+1)
                if(index_3_move == 0):
                    index_3_count = partial_hand.count(value+2)
                    #print(value+2)

                # print(str(index_1_count) + "," + str(index_2_count) + "," + str(index_3_count))

                # if there are at least one instance of each value
                if (index_1_count >0 and index_2_count >0 and index_3_count>0):

                    # if the numbers of each value are the same
                    if(index_1_count == index_2_count == index_3_count):
                        
                        # loop index advance move sum * 3
                        x += ((index_1_count)*3 + index_1_move + index_2_move + index_3_move)

                        # full reset
                        index_1_count = 0
                        index_2_count = 0
                        index_3_count = 0
                        index_1_move = 0
                        index_2_move= 0
                        index_3_move = 0
                        continue
                    # if the first value is the smallest
                    if (index_1_count <= index_2_count and index_1_count <= index_3_count):
                        
                        
                        
                        # index_2 and index_3 -= index_1, index_2_move and 3_move += index_1
                        index_2_count -= index_1_count
                        index_3_count -= index_1_count
                        index_2_move += index_1_count
                        index_3_move += index_1_count


                        # loop index advance index_1_move + index_1_count
                        if(index_2_count == 0 ):
                            x += (index_1_move+index_1_count+index_2_move)
                            index_1_count = index_3_count
                            index_1_move = index_3_move

                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0

                            value += 2
                            continue
                        
                        elif(index_3_count == 0 ):
                            
                            remain.extend([(value+1) for i in range(index_2_count)])

                            x += (index_1_move+index_1_count+index_2_move+index_2_count+index_3_move)

                            # full reset
                            index_1_count = 0
                            index_1_move = 0
                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0

                            continue

                        else:
                            x += (index_1_move+index_1_count)
                            # index_1 = index_2, index_2 = index_3, index_3 = 0
                            index_1_count = index_2_count
                            index_1_move = index_2_move
                            index_2_count = index_3_count
                            index_2_move = index_3_move
                            index_3_count = 0
                            index_3_move = 0
                            value += 1
                            continue
                    
                    elif (index_2_count <= index_1_count and index_2_count <= index_3_count):

                        index_1_count -= index_2_count
                        index_3_count -= index_2_count
                        index_1_move += index_2_count
                        index_3_move += index_2_count
                        
                        remain.extend([value for i in range(index_1_count)])
                        if(index_3_count == 0):
                            x += (index_1_move + index_1_count + index_2_move + index_2_count + index_3_move)

                            # full reset
                            index_1_count = 0
                            index_2_count = 0
                            index_3_count = 0
                            index_1_move = 0 
                            index_2_move = 0
                            index_3_move = 0
                            continue

                        else:
                            x += (index_1_move + index_1_count + index_2_count + index_2_move)
                            index_1_count = index_3_count
                            index_1_move = index_3_move
                            index_2_count = 0
                            index_2_move = 0
                            index_3_count = 0
                            index_3_move = 0
                            value += 2
                            continue
                        
                        
                        
                    elif (index_3_count <= index_1_count and index_3_count <= index_2_count):
                        

                        # remaining 
                        index_1_count -= index_3_count
                        index_2_count -= index_3_count

                        index_1_move += index_3_count
                        index_2_move += index_3_count

                        remain.extend([value for i in range(index_1_count)])
                        remain.extend([(value+1) for i in range(index_2_count)])
                        # move index by the tile 
                        x += (index_1_move+ index_1_count + index_2_move + index_2_count + index_3_count + index_3_move)
                        
                        # full reset
                        index_1_count = 0
                        index_2_count = 0
                        index_3_count = 0
                        index_1_move = 0
                        index_2_move = 0
                        index_3_move = 0 
                        continue
                                  


            x += (index_1_move + index_2_move + index_3_move + 1)
            remain.append(value)
            #print("# of index 1 added to remain "+ str(index_1_count))
            index_1_count = 0
            index_1_move = 0
            index_2_count = 0
            index_2_move = 0
            index_3_count = 0
            index_3_move = 0 

        # seq_extract v1.0
        # remain = []
        # remain.extend(hand[0:index])
        # duplicate = []
        # x = index
        # while x < (len(hand)-2):
        #     if(hand[x]//9 == hand[x+2]//9):
        #         while(hand[x] == hand[x+1] or hand[x+1] == hand[x+2]):
        #             if(hand[x] == hand[x+1]):
        #                 hand.count

        #         if(hand[x]+2 == hand[x+1]+1 == hand[x+2]):
        #             x+=3
        #             continue
                    
                    
        #     remain.append(hand[x])
        #     x+=1   
        x += (index_1_move + index_2_move + index_3_move)

        if(x<len(partial_hand)-1):
            remain.append(partial_hand[x+1])
        if(x <= len(partial_hand)-1):
            remain.append(partial_hand[x])
        # print("extract seq:")
        # print(remain)
        return sorted(remain)




    def single_handParti(self,attr):
        current_list = self.hands[attr]

        for x in range(len(current_list)):

            self.efficiency_map.setdefault(str(attr*9+x),0)
            if(current_list[x] == 4):
                    #1 KAN or 1 triplet + possible sequence
                self.partition.setdefault("KAN-triplet",[])
                self.partition["KAN-triplet"].append(attr*9+x)

            if(current_list[x] == 3):
                    # 1 triplet or 1 pair + possible sequence
                self.partition.setdefault("triplet",[])
                self.partition["triplet"].append(attr*9+x)
            if(current_list[x] == 2):
                    # 1 pair
                self.partition.setdefault("pair",[])
                self.partition["pair"].append(attr*9+x)

            if(x == 7 and current_list[x] >= 1):
                if(current_list[x-1] == 0 and current_list[x+1]>=1):
                    self.partition.setdefault("sequence_one-way",[])
                    self.partition["sequence_one-way"].append(attr*9+x-1)
                
            if(x < len(current_list)-2 and current_list[x] >= 1):
                if(current_list[x+1]==0 and current_list[x+2]):
                        # sequence middle
                    self.partition.setdefault("sequence_middle",[])
                    self.partition["sequence_middle"].append(attr*9+x)
                if(current_list[x+1]>=1 and current_list[x+2]==0):
                        #sequence two-way
                    if(x==0):
                        self.partition.setdefault("sequence_one-way",[])
                        self.partition["sequence_one-way"].append(attr*9+x)
                    else:
                        self.partition.setdefault("sequence_two-way",[])
                        self.partition["sequence_two-way"].append(attr*9+x) 
                if(current_list[x+1]>=1 and current_list[x+2]>=1):
                        #sequence complete
                    self.partition.setdefault("sequence_complete",[])
                    self.partition["sequence_complete"].append(attr*9+x)

                else:
                    self.partition.setdefault("single",[])
                    self.partition["single"].append(attr*9+x)
            elif(current_list[x] == 1):
                self.partition.setdefault("single",[])
                self.partition["single"].append(attr*9+x)
        

    # print tiles that are used in all the possible partitions
    def used_tile(self):
        used_tile_list = {}
        self.efficiency_map = defaultdict(int)
        for key in self.partition:
            for index in self.partition[key]:
                if("middle" in key): 
                    self.efficiency_map[index] +=1
                    self.efficiency_map[index+2] +=1
                elif("two-way" in key):
                    self.efficiency_map[index] +=1
                    self.efficiency_map[index+1] +=1
                else:
                    self.efficiency_map[index] +=1
        print(self.efficiency_map)
        return used_tile_list

    # print tiles that are needed for incomplete sequences 
    def tile_needed(self,input):
        waiting_tile_list = []
        for index in self.partition[input]:
            if("pair" in input or "single" in input):
                # get remaining tile at certain location
                # modify efficiency map value based on remaining tile
                value = self.remaining_tile(index) * 0.1
                self.efficiency_map[str(index)] += value


                waiting_tile_list.append(index)
            if("middle" in input):
                waiting_tile_list.append(index+1)
            if("two-way" in input):
                # can add a condition check to eliminate negative index
                waiting_tile_list.append(index-1)
                waiting_tile_list.append(index+2)
            if("one-way" in input):
                if(index%9==0):
                    waiting_tile_list.append(index+2)
                else:
                    waiting_tile_list.append(index)
        waiting_tile_list.sort()
        return waiting_tile_list

    def tile_use_count(self):
        for t in self.partition:
            for index in self.partition[t]:
                if("two-way" in t):
                    self.efficiency_map[str(index-1)] += 1
                    self.efficiency_map[str(index)] += 1
                    self.efficiency_map[str(index+1)] += 1
                elif("sequence" in t):
                    self.efficiency_map[str(index)] += 1
                    self.efficiency_map[str(index+1)] += 1
                    self.efficiency_map[str(index+2)] += 1
                else:
                    self.efficiency_map[str(index)] += 1
 


    def tile_efficiency(self): 
        # get the lowest value(s) from the efficiency map
        # if multiple 
        return None

    def partition_dict(self,hand,parti_type):
        return_dict = {}
        if("seq" in parti_type):
            # sequence
            hand_1 = self.seq_extract(hand,0)
            temp_list = self.locate_index(hand,hand_1,True)
            seq_dict = self.inc_seq_extract(hand_1)

            return_dict.setdefault("seq-complete",temp_list)
            return_dict.setdefault("seq-two-way",seq_dict["seq-two-way"])
            return_dict.setdefault("seq-one-way",seq_dict["seq-one-way"])
            return_dict.setdefault("seq-middle",seq_dict["seq-middle"])

            # triplet
            hand_2 = self.tri_extract(hand_1)
            temp_list_2 = self.locate_index(hand_1,hand_2,False)
            return_dict.setdefault("triplet",temp_list_2)

            # pair
            hand_3 = self.pair_extract(hand_2)
            temp_list_3 = self.locate_index(hand_2,hand_3,False)
            return_dict.setdefault("pair",temp_list_3)
            return_dict.setdefault("single",hand_3)

        elif("tri" in parti_type):
            # triplet 
            hand_1 = self.tri_extract(hand)
            temp_list = self.locate_index(hand,hand_1,False)
            return_dict.setdefault("triplet",temp_list)

            # sequence
            hand_2 = self.seq_extract(hand_1,0)
            temp_list_2 = self.locate_index(hand_1,hand_2,True)
            return_dict.setdefault("seq-complete",temp_list_2)

            seq_dict = self.inc_seq_extract(hand_2)
            return_dict.setdefault("seq-two-way",seq_dict["seq-two-way"])
            return_dict.setdefault("seq-one-way",seq_dict["seq-one-way"])
            return_dict.setdefault("seq-middle",seq_dict["seq-middle"])

            # pair
            hand_3 = self.pair_extract(hand_2)
            temp_list_3 = self.locate_index(hand_2,hand_3,False)
            return_dict.setdefault("pair",temp_list_3)
            return_dict.setdefault("single",hand_3)

        else:
            # seven pairs
            hand_1 = self.pair_extract(hand)
            temp_list = self.locate_index(hand,hand_1,False)
            return_dict.setdefault("pair",temp_list)
            return_dict.setdefault("single",hand_1)

        # print(return_dict)
        return return_dict

    def locate_index(self,hand_bef,hand_aft,isSeq):
        return_list = []
        index = 0
        diff = []
        # find the difference
        while index < len(hand_bef):
            value = hand_bef[index]
            count_after = hand_aft.count(value)
            count_before = hand_bef.count(value)
            if(count_after < count_before):
                diff.extend([value]*(count_before - count_after))

            index += 1
        
        if(isSeq == False):
            return_list = list(dict.fromkeys(diff))
            return return_list

        # the tile value
        tile = 0
        while tile < 25:
            if (len(diff) == 0):
                break

            num_tile_1 = diff.count(tile)
            if(num_tile_1 == 0):
                tile += 1
                continue
            
            elif(diff.count(tile+1) > 0 and diff.count(tile+2) > 0):
                return_list.append(tile)
                diff.remove(tile)
                diff.remove(tile+1)
                diff.remove(tile+2)

            else:
                tile += 1
        
        return return_list
            

        

            

        
    def inc_seq_extract(self,hand):
        return_dict = {}
        return_dict.setdefault("seq-two-way",[])
        return_dict.setdefault("seq-one-way",[])
        return_dict.setdefault("seq-middle",[])
        x = 0
        while x < 25:
            first_tile = hand.count(x)
            if(first_tile > 0):
                second_tile = 0
                third_tile = 0

                # only valid if the tiles are the same types
                if(x // 9 == (x+1) // 9):
                    second_tile = hand.count(x+1)
                if(x // 9 == (x+2) // 9):
                    third_tile = hand.count(x+2)

                # if there are two consecutive tiles
                if(second_tile > 0):
                    if(x % 9 == 0 or x % 9 == 8):
                        return_dict["seq-one-way"].append(x)
                    else:
                        return_dict["seq-two-way"].append(x)
                    
                    x += 2

                elif(third_tile > 0):
                    if((x+2) // 9 == (x+3) // 9 and hand.count(x+3) == 0):
                        return_dict["seq-middle"].append(x)
                    
                    if(third_tile == 1 and hand.count(x+3) == 0):
                        x += 2
                
            x += 1

        return return_dict

    # 1. Determine a list of goals for the yaku (by the tile distance and needed tile remaining to calculate the possibility) and have a threshold. 
    def yaku_goal_list(self,yaku_dict):
        prob_dict = {}
        for yaku in yaku_dict:
            num_waiting = yaku_dict[yaku][0]
            waiting_tile_list = yaku_dict[yaku][1]
            partition_str = yaku_dict[yaku][3]
            possibility = 1
            # 1 - (1-p1)*(1-p2)
            # p1*p2
            for item in waiting_tile_list:
                if(type(item) is int):
                    possibility *= 1 - (1 - (self.tile_count[item]/self.num_remain_tile))**5
                
                else:
                    temp_total = 0
                    for index in item:
                        temp_total += self.tile_count[index]
                    possibility *= 1 - (1 - (temp_total/self.num_remain_tile))**5

            print(yaku,':',possibility)
            prob_dict.setdefault(yaku,possibility)
        
        print(prob_dict)
                            
    #2. Determine the tiles used in these yaku, modified by the possibility of that yaku and the point value to give these tile a weight. 
        # yaku that are set up as goals
        tile_weight_dict = {}
        for yaku in prob_dict:
            prob = prob_dict[yaku]
            # calculate yaku's point value
            # 1 han
            used_tile_list = yaku_dict[yaku][2]
            point_value = 2000
        
            for tile in used_tile_list:
                if(tile in tile_weight_dict.keys()):
                    tile_weight_dict[tile] += point_value*prob
                else:
                    tile_weight_dict.setdefault(tile,point_value*prob)    

    # 3. For incomplete seq or single tile, calculate the possibility of some sort of advancing (for example, from single tile to seq-two-way, or from seq-one-way to seq-two-way etc). Give tiles weight based on that possibility. Then we have a list of tiles with weight, the one with the least weight should be the least important.
        partition = self.partition_dict(self.hand,'seq')

        for tile in partition['seq-two-way']:
            total_remain = self.tile_count_getter(tile-1) + self.tile_count_getter(tile+2)
            prob = total_remain / self.num_remain_tile
            if(tile in tile_weight_dict.keys()):
                tile_weight_dict[tile] += prob
            else:
                tile_weight_dict.setdefault(tile,prob)
            
        for tile in partition['seq-one-way']:
            if(tile % 9 == 0):
                total_remain = self.tile_count_getter(tile+2)
            else:
                total_remain = self.tile_count_getter(tile-1)
            prob = total_remain / self.num_remain_tile
            if(tile in tile_weight_dict.keys()):
                tile_weight_dict[tile] += prob
            else:
                tile_weight_dict.setdefault(tile,prob)

        for tile in partition['seq-middle']:
            prob = self.tile_count_getter(tile+1) / self.num_remain_tile
            if(tile in tile_weight_dict.keys()):
                tile_weight_dict[tile] += prob
            else:
                tile_weight_dict.setdefault(tile,prob)
        
        for tile in partition['pair']:
            prob = self.tile_count_getter(tile) / self.num_remain_tile
            if(tile in tile_weight_dict.keys()):
                tile_weight_dict[tile] += prob
            else:
                tile_weight_dict.setdefault(tile,prob)
        
        for tile in partition['single']:
            prob = self.tile_count_getter(tile) / self.num_remain_tile
            if(tile in tile_weight_dict.keys()):
                tile_weight_dict[tile] + prob
            else:
                tile_weight_dict.setdefault(tile,prob)

        return tile_weight_dict

    def predict_opponent(self,opponent_num):
        input = np.zeros((14,47))
        opponent = self.gameboard.opponent_getter(opponent_num)
        mlp = pickle.load(open('mlp_model.sav','rb'))
        for i in range(14):
            tile = self.hand[i]
            tile_attr = tile // 9
            tile_num = tile % 9
            input[i][34 + tile_attr] = 1
            input[i][37 + tile_num] = 1 
            
            for discard in opponent.discard_getter():
                input[i][discard] = 1
            
        prediction = mlp.predict_proba(input)

        return prediction
        


    def to_discard_tile(self):
        ma = Mahjong_AI.Mahjong_AI()
        partition_seq = self.partition_dict(self.hand,'seq')
        print('Partition: ',partition_seq)

        partition_tri = self.partition_dict(self.hand,'tri')
        partition_pair = self.partition_dict(self.hand,'pair')
        yaku_dict = ma.yaku_check(partition_seq,self.open_meld)
        print('Yaku_dict: ',yaku_dict)

        tile_weight_dict = self.yaku_goal_list(yaku_dict)
        print('Tile_weight_dict: ', tile_weight_dict)

        min_weight = 1
        min_tile = None
        for tile in tile_weight_dict.keys():
            if (tile_weight_dict[tile] < min_weight):
                min_weight = tile_weight_dict[tile]
                min_tile = tile
    
        return min_tile
    
    def try_to_call_meld(self,tile136,might_call_chi):

        return None,None
    
    def should_call_kan(self,tile136,from_opponent):

        return False,False
    
    def can_call_reach(self):

        return False,0


            
    
    def han_fu_calculation(self,han_string,partition):
        if('pinfu' in han_string):
            return 1,0
        
        if('all simple' in han_string):
            return 1,0


    def point_calculation(self,fu,han):
        self.fu += fu
        self.han += han
        if(self.han <= 4):
            return fu*2**(han+2)

        elif(self.han == 5):
            return 8000
        
        elif(self.han <= 7):
            return 12000
        
        elif(self.han <= 10):
            return 18000
        
        elif(self.han <= 12):
            return 24000
        
        else:
            return 36000

    def tile_count_getter(self,index):
        return self.tile_count[index]

    def tile_count_update(self,index):
        self.tile_count[index] -= 1
    
    def hand_add(self,tile):
        self.hand.append(tile)
        sorted(self.hand)

    def hand_discard(self,tile):
        self.hand.remove(tile)

    def hand_getter(self):
        return self.hand
    


# dummy = MahjongAgent()
# hand = [0,0,1,1,2,2,4,4,7,7,9,9,20,30]
# hand_2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
# hand_3 = [2,3,4,6,7,8,13,14,15,16,16,19,20,23]
# hand_4 = [9,10,12,13,14,19,20,21,23,24,25,30,30,31]
# hand_5 = [1,2,3,4,4,4,5,6,7,7,7,9,10,12]
# hand_6 = [2,2,3,3,3,4,4,4,5,11,12]
# hand_7 = [2, 2, 3, 4, 5, 5, 12, 13, 13, 14, 14, 15, 22, 23]
# hand_test = [1,3,5,7]

# yaku_check = {'pinfu':[2,[3,7],[1,2,3],'seq'],'all-simple':[3,[13,15,23],[3,4,5],'seq'],'tanyaou':[1,[6],[3,6,9],'seq']}

# print(dummy.yaku_goal_list(yaku_check,[1,2,4,5,8,9]))

# 3, 3, 5, 5, 5, 12, 13, 14, 18, 19, 21, 22, 23, 23
#2, 11, 12, 13, 20, 21, 22, 28, 28, 29, 29
# imp 2, 2, 3, 4, 5, 5, 12, 13, 13, 14, 14, 15, 22, 23
# 1, 2, 2, 3, 12, 12, 19, 20, 21, 22, 23, 23, 24, 25
# 2, 3, 4, 12, 12, 14, 15, 16, 31, 31, 31
# 2, 2, 2, 4, 5, 6, 13, 14, 15, 16, 16, 21, 22, 23
# 3,3,4,4,5,5,5,6,6

#print(dummy.tenpai_status_check(hand_test))



# dummy = MahjongAgent()
# dummy.single_handParti(0)
# dummy.single_handParti(1)
# dummy.single_handParti(2)
# dummy.tile_use_count()
# print(len(dummy.partition))
# print(dummy.partition)
# print(dummy.tile_needed())
# print(dummy.efficiency_map)