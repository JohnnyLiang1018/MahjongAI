class Mahjong_AI:
    # hand_partition, meld: list of tuple(partition_str,index_int)
    # hand_partition ex: {seq-complete:[start_tile_seq1, start_tile_seq2, etch],  pair:tile}
    def yaku_check(self,hand_partition,meld):
        return_dict = {}
        # 1. pinfu 
        # condition: all concealed hand, 3 seq-complete, 1 seq-two-way, 1 pair 
        if len(meld) == 0:
            num_seq_com = len(hand_partition['seq-complete'])
            if num_seq_com > 3: 
                num_waiting = 99
            else: # +2 waiting tiles for every seq-com under 3
                temp = 3 - num_seq_com
                num_waiting = temp * 2
                num_waiting = num_waiting - len(hand_partition['seq-middle'])
            num_seq_two = len(hand_partition['seq-two-way'])
            if num_seq_two == 0: 
                num_waiting = num_waiting + 1 # need +1 to complete two-way-seq
            else: # -1 waiting tile for every two-way-seq over the needed 1
                temp = num_seq_two - 1
                num_waiting = num_waiting - temp
            if len(hand_partition['pair']) == 0: #add 1 if there is no pair
                num_waiting = num_waiting + 1
        else: num_waiting = 99
        return_dict.setdefault("pinfu", num_waiting)
        num_waiting = 0

        # 2. all simple
        # condition: check each partition's index != 1 or 9 or honor, and for sequence, index+1 and index+2 if necessary
        for k, v in hand_partition.items():
            for tile in v:
                mod_var = tile % 9
                if (mod_var is (0 or 8)) or (tile > 26):
                    num_waiting = num_waiting + 1
                if 'seq' in k:
                    if k == 'seq-com':
                        if mod_var is 6: # 789 sequence
                            num_waiting = num_waiting + 1
                    if k == 'seq-one-way':
                        if mod_var is 0: # Have already added 1 waiting tile in previous check
                            num_waiting = num_waiting + 1
                        else:
                            num_waiting = num_waiting + 2
                    if k == 'seq-two-way':
                        num_waiting = num_waiting + 1
                    if k == 'seq-middle':
                        if mod_var is 6: # 7_9 sequence 
                            num_waiting = num_waiting + 2
                        else:
                            num_waiting = num_waiting + 1
        return_dict.setdefault('all-simple', num_waiting)
        num_waiting = 0

        # 3. honor yaku
        # condition: check if honor triplet exist
        if any(t >= 27 for t in hand_partition['triplet']):
            num_waiting = 0
        elif any(t >= 27 for t in hand_partition['pair']):
            num_waiting = 1
        elif any(t >= 27 for t in hand_partition['single']):
            num_waiting = 2
        else:
            num_waiting = 3
        return_dict.setdefault('honor-yaku', num_waiting)
        num_waiting = 0

        # 4. two identical seq
        # condition: all concealed hand, 2 seq with same index
        if len(meld) == 0:
            for k, v in hand_partition.items():
                if 'seq' in k:
                    if k is 'seq-com':
                        for temp_k, temp_v in hand_partition.items():
                            if temp_k is 'seq-com' and v is temp_v: #identical seq-com
                                num_waiting = 0
                            elif 'seq' in temp_k and v in temp_k: #1 seq-com and 1 incomplete seq with same index
                                num_waiting = 1
                            elif temp_k is 'seq-two-way' and (v % 9) + 1 is temp_v: #seq-two-way index starts at seq-com index+1
                                num_waiting = 1
                    elif any(v.count(x) > 1 for x in v): #2 identical incomplete seq
                        num_waiting = 2
                else:
                    num_waiting = 4 * len(hand_partition['pair']) #pairs could possible become identical seq
        else: num_waiting = 99
        return_dict.setdefault('two-identical-seq', num_waiting)
        num_waiting = 0
        ## above Christoph 1-4 ##

        # 5. straight
        # condtion: 3 seq with index 0, 3, 6
        # 6. three color seq
        # condition: 3 seq with the same index after mod 9
        # 7. three color triplet
        # condition: 3 triplet with the same index
        ## above Dane  5-7 ##

        num_pair = len(hand_partition['pair'])
        num_triplet = len(hand_partition['triplet'])
        num_seq = len(hand_partition['seq-complete'])

        # 8. all triplet
        # condition: 4 triplet ( or quads) with 1 pair
        if num_pair > 1:
            extra_pair = num_pair - 1 # get number of extra pair
        else:
            extra_pair = 0     

        if num_triplet == 4: # 4 tri
            num_waiting = 0
        else: # less than 4 tri
            temp = 4 - num_triplet # triplet to complete
            num_waiting = temp * 2
            num_waiting = temp - extra_pair # -1 for each extra pair
        if num_pair == 0: # no pair wait +1
            num_waiting = num_waiting + 1    
        return_dict.setdefault("all_triplet", num_waiting)

        # 9. terminal in all meld
        # condition: (seq + triplet) = 4, index is 1 or 9 or honor, for seq check index+1 and index+2 
        num_com = 0
        num_almost = 0
        pair_used = 0
        for k, v in hand_partition.items():
            if 'triplet' in k:
                if v < 26:
                    if(v % 9) is 0 or 8:
                        num_com = num_com + 1
                else:
                    num_com = num_com + 1
            if 'seq-complete' in k:
                if (v % 9) is 0 or 6:
                    num_com = num_com + 1
            if 'seq-one-way' in k:
                if (v % 9) is 0 or 6:
                    num_almost = num_almost + 1
            if 'seq-two-way' in k:
                if (v % 9) is 1 or 6:
                    num_almost = num_almost + 1
            if 'seq-middle' in k:
                if (v % 9) is 0 or 6:
                    num_almost = num_almost + 1
            if 'pair' in k:
                if(v % 9) is 0 or 8:
                    num_almost = num_almost + 1
                    pair_used = pair_used +1                                                          
        temp = 4 - num_com 
        num_waiting = (temp * 2) - num_almost
        if (num_pair - pair_used) < 1 :
            num_waiting = num_waiting + 1
        return_dict.setdefault("ternimal_in_all", num_waiting)

        # 10. seven pair 
        # condition: 7 pair partition
        if len(meld) == 0:
            if num_pair < 7:
                temp = 7 - num_pair
                num_waiting = temp - num_triplet 
        else: num_waiting = 99         
        return_dict.setdefault("seven_pairs", num_waiting)
        ## above Lee 8-10 ##
        
        return return_dict


def main():
    mai = Mahjong_AI()
    hand_partition = {'seq-complete':[1,2,3], 'seq-middle': [], 'seq-two-way': [1], 'pair': [1], 
                        'triplet': [], 'single': []}
    meld = []
    print(mai.yaku_check(hand_partition, meld))

if __name__ == '__main__':
    main()
