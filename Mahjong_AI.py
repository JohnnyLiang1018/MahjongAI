

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
            if (v%9 is 0 or 8) or (v > 26):
                num_waiting = num_waiting + 1
            if 'seq' in k:
                if k == 'seq-com':
                    if ((v+2)%9) is 0 or 8:
                        num_waiting = num_waiting + 1
                if k == 'seq-one-way':
                    num_waiting = num_waiting + 2
                if k == 'seq-two-way':
                    num_waiting = num_waiting + 1
                if k == 'seq-middle':
                    if(v%9) is 6:
                        num_waiting = num_waiting + 2
                    else:
                        num_waiting = num_waiting + 1
        return_dict.setdefault('all-simple', num_waiting)
        num_waiting = 0
        # 3. honor yaku
        # condition: check if honor triplet exist
        if hand_partition['triplet'] >= 27:
            num_waiting = 0
        elif hand_partition['pair'] >= 27:
            num_waiting = 1
        elif hand_partition['single'] >= 27:
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
                        if any(v.count(x) > 1 for x in v): #2 identical seq-com
                            num_waiting = 0
                            break
                        for s in hand_partition:
                            if 'seq' in s and v in s: #1 seq-com and 1 incomplete seq with same
                                num_waiting = 1
                    elif any(v.count(x) > 1 for x in v): #2 identical partial seq
                        num_waiting = 2
                else:
                    num_waiting = 4 * len(hand_partition['pair']) #pairs could possible become identical seq
        else: num_waiting = 99
        return_dict.setdefault('honor-yaku', num_waiting)
        num_waiting = 0
        ## above Christoph 1-4 ##

        # 5. straight
        # condtion: 3 seq with index 0, 3, 6
        # 6. three color seq
        # condition: 3 seq with the same index after mod 9
        # 7. three color triplet
        # condition: 3 triplet with the same index
        ## above Dane  5-7 ##

        # 8. all triplet
        # condition: 4 triplet with 1 pair 
        # 9. terminal in all meld
        # condition: (seq + triplet) = 4, index is 1 or 9 or honor, for seq check index+1 and index+2 
        # 10. seven pair 
        # condition: 7 pair partition
        ## above Lee 8-10 ##
        
        return return_dict


def main():
    mai = Mahjong_AI()
    hand_partition = {'seq-complete':[], 'seq-middle': [], 'seq-two-way': [], 'pair': [], 
                        'triplet': [], 'single': []}
    meld = []
    mai.yaku_check(hand_partition, meld)

if __name__ == '__main__':
    main()
