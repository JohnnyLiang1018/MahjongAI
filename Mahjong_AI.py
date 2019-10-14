class Mahjong_AI:
    # hand_partition, meld: list of tuple(partition_str,index_int)
    #hand_partition ex: {seq-complete:[start_tile_seq1, start_tile_seq2, etch],  pair:tile}
    def yaku_check(self,hand_partition,meld):
        return_dict = {}
        # 1. pinfu 
        # condition: all concealed hand, 3 seq-complete, 1 seq-two-way, 1 pair 
        if len(meld) == 0:
            num_seq_com = len(hand_partition['seq-complete'])
            if num_seq_com > 3: 
                num_waiting = 1
            else: # +2 waiting tiles for every seq-com under 3
                temp = 3 - num_seq_com
                num_waiting = temp * 2
            num_seq_two = len(hand_partition['seq-two-way'])
            if num_seq_two == 0: 
                num_waiting = num_waiting + 1 # need +1 to complete two-way-seq
            else: # -1 waiting tile for every two-way-seq over the needed 1
                temp = num_seq_two - 1
                num_waiting = num_waiting - temp
            if len(hand_partition['pair']) == 0: #add 1 if there is no pair
                num_waiting = num_waiting + 1

            return_dict.setdefault("pinfu", num_waiting)
        # 2. all simple
        # condition: check each partition's index != 1 or 9 or honor, and for sequence, index+1 and index+2 if necessary
        # 3. honor yaku
        # condition: check if honor triplet exist
        # 4. two identical seq
        # condition: all concealed hand, 2 seq with same index
        # 5. straight
        # condtion: 3 seq with index 0, 3, 6
        # 6. three color seq
        # condition: 3 seq with the same index after mod 9
        # 7. three color triplet
        # condition: 3 triplet with the same index
        # 8. all triplet
        # condition: 4 triplet with 1 pair 
        # 9. terminal in all meld
        # condition: (seq + triplet) = 4, index is 1 or 9 or honor, for seq check index+1 and index+2 
        # 10. seven pair 
        # condition: 7 pair partition
        return return_dict