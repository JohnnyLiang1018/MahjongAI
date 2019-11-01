class Mahjong_AI:
    # hand_partition, meld: list of tuple(partition_str,index_int)
    # hand_partition ex: {seq-complete:[start_tile_seq1, start_tile_seq2, etch],  pair:tile}

    # return dict : {yaku_name: [num_waiting,[waiting_tiles_list], tiles_used_list]}
    def yaku_check(self,hand_partition,meld):
        return_dict = {}
        num_waiting = 0
        tiles_needed = []
        tiles_used = []
        # 1. pinfu 
        # condition: all concealed hand, 3 seq-complete, 1 seq-two-way, 1 pair 
        if len(meld) == 0:
            num_waiting = 1
            num_seq_com = len(hand_partition['seq-complete'])
            if num_seq_com > 3: 
                num_waiting = 99
            else: # +2 waiting tiles for every seq-com under 3
                temp = 3 - num_seq_com
                num_waiting = num_waiting + temp * 2
                for x  in hand_partition['seq-complete']:
                    tiles_used.append(x)
                    tiles_used.append(x + 1)
                    tiles_used.append(x + 2)
                num_waiting = num_waiting - len(hand_partition['seq-middle'])
                for x in hand_partition['seq-middle']:
                    tiles_needed.append(x + 1) # need index tile + 1
                    tiles_used.append(x)
                    tiles_used.append(x + 2)
                num_waiting = num_waiting - len(hand_partition['seq-one-way'])
                for x in hand_partition['seq-one-way']:
                    if x % 9 == 0: # 123 one way
                        tiles_needed.append(x + 2)
                        tiles_used.append(x)
                        tiles_used.append(x + 1)
                    else: # 789 one way
                        tiles_needed.append(x - 1)
                        tiles_used.append(x)
                        tiles_used.append(x + 1)
            num_seq_two = len(hand_partition['seq-two-way'])
            if num_seq_two == 0: 
                num_waiting = num_waiting + 1 # need +1 tile to complete two-way-seq
                for x in hand_partition['single']:
                    if 7 > (x % 9) > 1 and x < 26:
                        tiles_needed.append([x-1, x+1]) # every single needs + or - 1 to become 2-way
                        tiles_used.append(x)
            else: # -1 waiting tile for every two-way-seq over the needed 1
                temp = num_seq_two - 1
                num_waiting = num_waiting - temp
                for x in hand_partition['seq-two-way']:
                    tiles_needed.append([x-1, x+2]) # each 2-way is waiting for x-1 or x+2
                    tiles_used.append(x)
                    tiles_used.append(x + 1)
            if len(hand_partition['pair']) == 0: #add 1 if there is no pair
                num_waiting = num_waiting + 1
        else: num_waiting = 99
        return_dict.setdefault("pinfu", [num_waiting, tuple(tiles_needed), tuple(tiles_used)])
        num_waiting = 0
        tiles_needed.clear()
        tiles_used.clear()

        # 2. all simple
        # condition: check each partition's index != 1 or 9 or honor, and for sequence, index+1 and index+2 if necessary
        for k, v in hand_partition.items():
            for tile in v:
                mod_var = tile % 9
                if (mod_var == (0 or 8)) or (tile > 26):
                    num_waiting = num_waiting + 1
                    if k == 'triplet':
                        num_waiting = num_waiting + 2
                    elif k == 'pair':
                        num_waiting = num_waiting + 1
                else:
                    tiles_used.append(tile)
                    if k == 'triplet':
                        tiles_used.append(tile)
                        tiles_used.append(tile)
                    elif k == 'pair':
                        tiles_used.append(tile)
                if 'seq' in k:
                    if k == 'seq-complete':
                        if mod_var == 6: # 789 sequence
                            num_waiting = num_waiting + 1
                            tiles_needed.append(tile - 1) # need tile 6
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                        if mod_var == 0: # 123 sequence
                            tiles_needed.append(tile + 3) # need tile 4
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                    if k == 'seq-one-way':
                        if mod_var == 0: # Have already added 1 waiting tile in previous check
                            num_waiting = num_waiting + 1
                            tiles_needed.extend([tile+2, tile+3]) # need 3, 4
                            tiles_used.append(tile + 1)
                        else:
                            num_waiting = num_waiting + 2
                            tiles_needed.extend([tile-1, tile-2]) # need 7, 6
                            tiles_used.append(tile)
                    if k == 'seq-two-way':
                        if mod_var == 6: #78 two way
                            num_waiting = num_waiting + 1
                            tiles_needed.append(tile - 1)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                        if mod_var == 1: #23 two way
                            num_waiting = num_waiting + 1
                            tiles_needed.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 2)
                        else:
                            num_waiting = num_waiting + 1
                            tiles_needed.append([tile-1, tile+2])
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                    if k == 'seq-middle':
                        if mod_var == 6: # 7_9 sequence 
                            num_waiting = num_waiting + 2
                            tiles_needed.extend([tile+1, tile-1]) # need 6, 8
                            tiles_used.append(tile)
                        if mod_var == 0: # 1_3 sequence
                            num_waiting = num_waiting + 1 # already added one from before
                            tiles_needed.extend([tile+1, tile+3])
                            tiles_used.append(tile+2)
                        else:
                            num_waiting = num_waiting + 1
                            tiles_needed.append(tile + 1) # need middle tile
                            tiles_used.append(tile)
                            tiles_used.append(tile + 2)
                # Possibly need to deal with single tiles
        return_dict.setdefault('all-simple', [num_waiting, tuple(tiles_needed), tuple(tiles_used)])
        num_waiting = 0
        tiles_needed.clear()

        # 3. honor yaku
        # condition: check if honor triplet exist
        num_waiting = 3
        for t in hand_partition['single']:
            if t >= 27:
                num_waiting = 2
                tiles_needed.append(t)
                tiles_used.append(t)
        for t in hand_partition['pair']:
            if t >= 27:
                num_waiting = 1
                tiles_needed.clear()
                tiles_used.clear()
                tiles_needed.append(t)
                tiles_used.append(t)
                tiles_used.append(t)
        if any(t >= 27 for t in hand_partition['triplet']):
            num_waiting = 0
            tiles_needed.clear()
            tiles_used.append(t)
            tiles_used.append(t)
            tiles_used.append(t)
        # TODO how to handle 0 honor tiles in hand for tiles_needed
        return_dict.setdefault('honor-yaku', [num_waiting, tuple(tiles_needed), tuple(tiles_used)])
        num_waiting = 0
        tiles_needed.clear()

        # 4. two identical seq
        # condition: all concealed hand, 2 seq with same index
        # current only checks partial seq with eachother, not checking singles etc
        if len(meld) == 0:
            num_waiting = 6
            for k, v in hand_partition.items():
                if k == 'seq-two-way':
                    for tile in v:
                        if v.count(tile) > 1: # two identical two-ways
                            num_waiting = 2
                            tiles_needed.append([tile-1, tile+2])
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                        if (tile + 1) in hand_partition['seq-two-way']:
                            num_waiting = 2
                            tiles_needed.extend([tile, tile+2])
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                        if (tile - 1) in hand_partition['seq-two-way']:
                            num_waiting = 2
                            tiles_needed.extend([tile+1, tile-1])
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile - 1)
                            tiles_used.append(tile)
                elif k == 'seq-one-way':
                    for tile in v:
                        if v.count(tile) > 1:
                            num_waiting = 2
                            if tile % 9 == 0:  # 12 seq
                                tiles_needed.append(tile+2)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                            else:  # 89 seq
                                tiles_needed.append(tile-1)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                elif k == 'seq-middle':
                    for tile in v:
                        if v.count(tile) > 1:
                            num_waiting = 2
                            tiles_needed.append(tile+1)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 2)
                elif k == 'seq-complete':
                    for tile in v:
                        if v.count(tile) > 1: # 2 identical seq-com
                            num_waiting = 0
                            tiles_needed.clear()
                            tiles_used.clear()
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                            break
                        if (tile + 1) in hand_partition['seq-two-way']: #check if seq-com same as incomplete seqs
                            if num_waiting > 1: #clear tiles_needed if waiting on less tiles
                                tiles_needed.clear()
                                tiles_used.clear()
                            num_waiting = 1
                            tiles_needed.append(tile)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                        if tile in hand_partition['seq-two-way']:
                            if num_waiting > 1: #clear tiles_needed if waiting on less tiles
                                tiles_needed.clear()
                                tiles_used.clear()
                            num_waiting = 1
                            tiles_needed.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                        if tile in hand_partition['seq-one-way'] or (tile + 1) in hand_partition['seq-one-way']:
                            if num_waiting > 1: #clear tiles_needed if waiting on less tiles
                                tiles_needed.clear()
                                tiles_used.clear()
                            num_waiting = 1
                            if tile % 9 == 0: 
                                tiles_needed.append(tile + 2)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                                tiles_used.append(tile + 2)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                            else: 
                                tiles_needed.append(tile)
                                tiles_used.append(tile)
                                tiles_used.append(tile + 1)
                                tiles_used.append(tile + 2)
                                tiles_used.append(tile + 1)
                                tiles_used.append(tile + 2)
                        if tile in hand_partition['seq-middle']:
                            if num_waiting > 1: #clear tiles_needed if waiting on less tiles
                                tiles_needed.clear()
                            num_waiting = 1
                            tiles_needed.append(tile + 1)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 1)
                            tiles_used.append(tile + 2)
                            tiles_used.append(tile)
                            tiles_used.append(tile + 2)
        else: num_waiting = 99
        return_dict.setdefault('two-identical-seq', [num_waiting, tuple(tiles_needed), tuple(tiles_used)])
        num_waiting = 0
        ## above Christoph 1-4 ##

        # 5. straight
        # condtion: 3 seq with index 0, 3, 6

        # 6. three color seq
        # condition: 3 seq with the same index after mod 9
        if(len(meld)<2):
            min_waiting = 9
            min_index = -1
            waiting_tiles_list = ()
            used_tiles_list = ()

            for i in range(7):
                waiting_count = 9
                temp_wait_list = [i,i+1,i+2,i+9,i+10,i+11,i+18,i+19,i+20]
                temp_use_list = []
                for index in hand_partition['seq-complete']:
                    if (index % 9 == i):
                        print(index)
                        print(temp_wait_list)
                        print(type(temp_wait_list))
                        print(type(temp_wait_list[0]))
                        waiting_count -= 3
                        temp_wait_list.remove(index)
                        temp_wait_list.remove(index+1)
                        temp_wait_list.remove(index+2)
                        temp_use_list.append(index)
                        temp_use_list.append(index+1)
                        temp_use_list.append(index+2)

                for index in hand_partition['triplet']:
                    if (index % 9 == i):
                        waiting_count -= 1
                        if(index in temp_wait_list):
                            temp_wait_list.remove(index)
                        temp_use_list.append(index)
                
                for index in hand_partition['pair']:
                    if(index % 9 == i):
                        waiting_count -= 1
                        if(index in temp_wait_list):
                            temp_wait_list.remove(index)
                        temp_use_list.append(index)
                
                for index in hand_partition['single']:
                    if (index % 9 >= i and index % 9 <= i+2):
                        waiting_count -= 1
                        if(index in temp_wait_list):
                            temp_wait_list.remove(index)
                        temp_use_list.append(index)
                
                if(waiting_count < min_waiting):
                    min_waiting = waiting_count
                    min_index = i
                    waiting_tiles_list = tuple(temp_wait_list)
                    used_tiles_list = tuple(temp_use_list)

            
            value_list = [min_waiting,waiting_tiles_list,used_tiles_list,'seq']
            return_dict.setdefault('three-color-seq',value_list)     


        # 7. three color triplet
        # condition: 3 triplet with the same index
        ## above Dane  5-7 ##

        # num_pair = len(hand_partition['pair'])
        # num_triplet = len(hand_partition['triplet'])
        # num_seq = len(hand_partition['seq-complete'])

        # # 8. all triplet
        # # condition: 4 triplet ( or quads) with 1 pair
        # if num_pair > 1:
        #     extra_pair = num_pair - 1 # get number of extra pair
        # else:
        #     extra_pair = 0     

        # if num_triplet == 4: # 4 tri
        #     num_waiting = 0
        # else: # less than 4 tri
        #     temp = 4 - num_triplet # triplet to complete
        #     num_waiting = temp * 2
        #     num_waiting = temp - extra_pair # -1 for each extra pair
        # if num_pair == 0: # no pair wait +1
        #     num_waiting = num_waiting + 1    
        # return_dict.setdefault("all_triplet", num_waiting)

        # # 9. terminal in all meld
        # # condition: (seq + triplet) = 4, index is 1 or 9 or honor, for seq check index+1 and index+2 
        # num_com = 0
        # num_almost = 0
        # pair_used = 0
        # for k, v in hand_partition.items():
        #     if 'triplet' in k:
        #         if v < 26:
        #             if(v % 9) is 0 or 8:
        #                 num_com = num_com + 1
        #         else:
        #             num_com = num_com + 1
        #     if 'seq-complete' in k:
        #         if (v % 9) is 0 or 6:
        #             num_com = num_com + 1
        #     if 'seq-one-way' in k:
        #         if (v % 9) is 0 or 6:
        #             num_almost = num_almost + 1
        #     if 'seq-two-way' in k:
        #         if (v % 9) is 1 or 6:
        #             num_almost = num_almost + 1
        #     if 'seq-middle' in k:
        #         if (v % 9) is 0 or 6:
        #             num_almost = num_almost + 1
        #     if 'pair' in k:
        #         if(v % 9) is 0 or 8:
        #             num_almost = num_almost + 1
        #             pair_used = pair_used +1                                                          
        # temp = 4 - num_com 
        # num_waiting = (temp * 2) - num_almost
        # if (num_pair - pair_used) < 1 :
        #     num_waiting = num_waiting + 1
        # return_dict.setdefault("ternimal_in_all", num_waiting)

        # # 10. seven pair 
        # # condition: 7 pair partition
        # if len(meld) == 0:
        #     if num_pair < 7:
        #         temp = 7 - num_pair
        #         num_waiting = temp - num_triplet 
        # else: num_waiting = 99         
        # return_dict.setdefault("seven_pairs", num_waiting)
        # ## above Lee 8-10 ##
        
        # print("result:")
        # print(return_dict)
        return return_dict


def main():
    mai = Mahjong_AI()
    hand_partition = {'seq-complete':[9,18], 'seq-middle': [], 'seq-two-way': [1], 'pair': [7], 
                        'triplet': [5], 'single': [1,2]}
    meld = []
    print(mai.yaku_check(hand_partition, meld))

if __name__ == '__main__':
    main()
