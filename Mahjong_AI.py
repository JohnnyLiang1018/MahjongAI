class Mahjong_AI:
    # hand_partition, meld: list of tuple(partition_str,index_int)
    # hand_partition ex: {seq-complete:[start_tile_seq1, start_tile_seq2, etch],  pair:tile}

    # return dict : {yaku_name: [num_waiting,[waiting_tiles_list], tiles_used_list]}
    def yaku_check(self,hand_partition,meld):
        return_dict = {}
        num_waiting = 0
        tiles_needed_list = []
        tiles_used_list = []
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
                    tiles_used_list.append(x)
                    tiles_used_list.append(x + 1)
                    tiles_used_list.append(x + 2)
                num_waiting = num_waiting - len(hand_partition['seq-middle'])
                for x in hand_partition['seq-middle']:
                    tiles_needed_list.append(x + 1) # need index tile + 1
                    tiles_used_list.append(x)
                    tiles_used_list.append(x + 2)
                num_waiting = num_waiting - len(hand_partition['seq-one-way'])
                for x in hand_partition['seq-one-way']:
                    if x % 9 == 0: # 123 one way
                        tiles_needed_list.append(x + 2)
                        tiles_used_list.append(x)
                        tiles_used_list.append(x + 1)
                    else: # 789 one way
                        tiles_needed_list.append(x - 1)
                        tiles_used_list.append(x)
                        tiles_used_list.append(x + 1)
            num_seq_two = len(hand_partition['seq-two-way'])
            if num_seq_two == 0: 
                num_waiting = num_waiting + 1 # need +1 tile to complete two-way-seq
                for x in hand_partition['single']:
                    if 7 > (x % 9) > 1 and x < 26:
                        tiles_needed_list.append([x-1, x+1]) # every single needs + or - 1 to become 2-way
                        tiles_used_list.append(x)
            else: # -1 waiting tile for every two-way-seq over the needed 1
                temp = num_seq_two - 1
                num_waiting = num_waiting - temp
                for x in hand_partition['seq-two-way']:
                    tiles_needed_list.append([x-1, x+2]) # each 2-way is waiting for x-1 or x+2
                    tiles_used_list.append(x)
                    tiles_used_list.append(x + 1)
            if len(hand_partition['pair']) == 0: #add 1 if there is no pair
                num_waiting = num_waiting + 1
                for t in hand_partition['single']:
                    possible_pairs_list = []
                    if t not in tiles_used_list:
                        possible_pairs_list.append(t)
                    tiles_needed_list.append(possible_pairs_list)
                    tiles_used_list.append(possible_pairs_list)
            elif len(hand_partition['pair']) > 1:
                num_waiting = num_waiting + len(hand_partition['pair']) - 1
                for t in hand_partition['pair']:
                    tiles_needed_list.append(t)
                    tiles_used_list.append(t)       #TODO Deal with multiple pairs
        else: num_waiting = 99
        return_dict.setdefault("pinfu", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
        num_waiting = 0
        tiles_needed_list.clear()
        tiles_used_list.clear()

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
                    tiles_used_list.append(tile)
                    if k == 'triplet':
                        tiles_used_list.append(tile)
                        tiles_used_list.append(tile)
                    elif k == 'pair':
                        tiles_used_list.append(tile)
                if 'seq' in k:
                    if k == 'seq-complete':
                        if mod_var == 6: # 789 sequence
                            num_waiting = num_waiting + 1
                            tiles_needed_list.append(tile - 1) # need tile 6
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                        if mod_var == 0: # 123 sequence
                            tiles_needed_list.append(tile + 3) # need tile 4
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                    if k == 'seq-one-way':
                        if mod_var == 0: # Have already added 1 waiting tile in previous check
                            num_waiting = num_waiting + 1
                            tiles_needed_list.extend([tile+2, tile+3]) # need 3, 4
                            tiles_used_list.append(tile + 1)
                        else:
                            num_waiting = num_waiting + 2
                            tiles_needed_list.extend([tile-1, tile-2]) # need 7, 6
                            tiles_used_list.append(tile)
                    if k == 'seq-two-way':
                        if mod_var == 6: #78 two way
                            num_waiting = num_waiting + 1
                            tiles_needed_list.append(tile - 1)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                        elif mod_var == 1: #23 two way
                            num_waiting = num_waiting + 1
                            tiles_needed_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 2)
                        else:
                            num_waiting = num_waiting + 1
                            tiles_needed_list.append([tile-1, tile+2])
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                    if k == 'seq-middle':
                        if mod_var == 6: # 7_9 sequence 
                            num_waiting = num_waiting + 2
                            tiles_needed_list.extend([tile+1, tile-1]) # need 6, 8
                            tiles_used_list.append(tile)
                        elif mod_var == 0: # 1_3 sequence
                            num_waiting = num_waiting + 1 # already added one from before
                            tiles_needed_list.extend([tile+1, tile+3])
                            tiles_used_list.append(tile+2)
                        else:
                            num_waiting = num_waiting + 1
                            tiles_needed_list.append(tile + 1) # need middle tile
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 2)
                # Possibly need to deal with single tiles
        return_dict.setdefault('all-simple', [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
        num_waiting = 0
        tiles_needed_list.clear()
        tiles_used_list.clear()

        # 3. honor yaku
        # condition: check if honor triplet exist
        num_waiting = 3
        for t in hand_partition['single']:
            if t >= 27:
                num_waiting = 2
                tiles_needed_list.append(t)
                tiles_needed_list.append(t)
                tiles_used_list.append(t)
        for t in hand_partition['pair']:
            if t >= 27:
                num_waiting = 1
                tiles_needed_list.clear()
                tiles_used_list.clear()
                tiles_needed_list.append(t)
                tiles_used_list.append(t)
                tiles_used_list.append(t)
        if any(t >= 27 for t in hand_partition['triplet']):
            num_waiting = 0
            tiles_needed_list.clear()
            tiles_used_list.append(t)
            tiles_used_list.append(t)
            tiles_used_list.append(t)
        # TODO how to handle 0 honor tiles in hand for tiles_needed_list
        return_dict.setdefault('honor-yaku', [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
        num_waiting = 0
        tiles_needed_list.clear()
        tiles_used_list.clear()

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
                            tiles_needed_list.append([tile-1, tile+2])
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                        if (tile + 1) in hand_partition['seq-two-way']:
                            num_waiting = 2
                            tiles_needed_list.extend([tile, tile+2])
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                        if (tile - 1) in hand_partition['seq-two-way']:
                            num_waiting = 2
                            tiles_needed_list.extend([tile+1, tile-1])
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile - 1)
                            tiles_used_list.append(tile)
                elif k == 'seq-one-way':
                    for tile in v:
                        if v.count(tile) > 1:
                            num_waiting = 2
                            if tile % 9 == 0:  # 12 seq
                                tiles_needed_list.append(tile+2)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                            else:  # 89 seq
                                tiles_needed_list.append(tile-1)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                elif k == 'seq-middle':
                    for tile in v:
                        if v.count(tile) > 1:
                            num_waiting = 2
                            tiles_needed_list.append(tile+1)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 2)
                elif k == 'seq-complete':
                    for tile in v:
                        if v.count(tile) > 1: # 2 identical seq-com
                            num_waiting = 0
                            tiles_needed_list.clear()
                            tiles_used_list.clear()
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                            break
                        if (tile + 1) in hand_partition['seq-two-way']: #check if seq-com same as incomplete seqs
                            if num_waiting > 1: #clear tiles_needed_list if waiting on less tiles
                                tiles_needed_list.clear()
                                tiles_used_list.clear()
                            num_waiting = 1
                            tiles_needed_list.append(tile)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                        if tile in hand_partition['seq-two-way']:
                            if num_waiting > 1: #clear tiles_needed_list if waiting on less tiles
                                tiles_needed_list.clear()
                                tiles_used_list.clear()
                            num_waiting = 1
                            tiles_needed_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                        if tile in hand_partition['seq-one-way'] or (tile + 1) in hand_partition['seq-one-way']:
                            if num_waiting > 1: #clear tiles_needed_list if waiting on less tiles
                                tiles_needed_list.clear()
                                tiles_used_list.clear()
                            num_waiting = 1
                            if tile % 9 == 0: 
                                tiles_needed_list.append(tile + 2)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                                tiles_used_list.append(tile + 2)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                            else: 
                                tiles_needed_list.append(tile)
                                tiles_used_list.append(tile)
                                tiles_used_list.append(tile + 1)
                                tiles_used_list.append(tile + 2)
                                tiles_used_list.append(tile + 1)
                                tiles_used_list.append(tile + 2)
                        if tile in hand_partition['seq-middle']:
                            if num_waiting > 1: #clear tiles_needed_list if waiting on less tiles
                                tiles_needed_list.clear()
                            num_waiting = 1
                            tiles_needed_list.append(tile + 1)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 1)
                            tiles_used_list.append(tile + 2)
                            tiles_used_list.append(tile)
                            tiles_used_list.append(tile + 2)
        else: num_waiting = 99
        return_dict.setdefault('two-identical-seq', [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
        num_waiting = 0
        tiles_needed_list.clear()
        tiles_used_list.clear()
        ## above Christoph 1-4 ##

        # 5. straight
        # condtion: 3 seq with index 0, 3, 6
        
        if len(meld) > 1: # if > 1 exposed triplet
            num_waiting = 99

        # 3 arrays (9 total tiles per suit)
        # seq-complete partition check (ID suit; modify array) --> singles, pairs, and triplets (check for tiles in similar range (variable-- if yes))
        else:
            suit = "wan"
            suit_wan = [0] * 9
            suit_pin = [0] * 9
            suit_sou = [0] * 9

            for k, v in hand_partition.items(): # unique tile counted = 1, else 0
                for tile in v:

                    if 'seq-complete' in k:
                        if tile < 7:
                            suit_wan[tile] = suit_wan[tile + 1] = suit_wan[tile + 2] = 1
                            
                        elif 8 < tile < 16:
                            suit_pin[(tile % 9)] = suit_pin[(tile % 9) + 1] = suit_pin[(tile % 9) + 2] = 1

                        else:
                            suit_sou[(tile % 9)] = suit_sou[(tile % 9) + 1] = suit_sou[(tile % 9) + 2] = 1

                    if 'seq-two-way' in k:
                        if tile < 7:
                            suit_wan[tile] = suit_wan[tile + 1] = 1
                                
                        elif 8 < tile < 16:
                            suit_pin[(tile % 9)] = suit_pin[(tile % 9) + 1] = 1

                        else:
                            suit_sou[(tile % 9)] = suit_sou[(tile % 9) + 1] = 1

                    if 'seq-one-way' in k:
                        if tile == 0:
                            suit_wan[tile] = suit_wan[tile + 1] = 1
                        elif tile == 8:
                            suit_wan[tile] = suit_wan[tile - 1] = 1
                                
                        elif tile == 9:
                            suit_pin[(tile % 9)] = suit_pin[(tile % 9) + 1] = 1
                        elif tile == 17:
                            suit_pin[(tile % 9)] = suit_pin[(tile % 9) - 1] = 1

                        elif tile == 18:
                            suit_sou[(tile % 9)] = suit_sou[(tile % 9) + 1] = 1
                        else:
                            suit_sou[(tile % 9)] = suit_sou[(tile % 9) - 1] = 1

                    if 'seq-middle' in k:
                        if tile < 7:
                            suit_wan[tile] = suit_wan[tile + 2] = 1
                                
                        elif 8 < tile < 16:
                            suit_pin[(tile % 9)] = suit_pin[(tile % 9) + 2] = 1

                        else:
                            suit_sou[(tile % 9)] = suit_sou[(tile % 9) + 2] = 1
                            
                    if 'single' or 'pair' or 'triplet' in k and (tile < 27):
                        if tile < 9:
                            suit_wan[tile] = 1
                                
                        elif 8 < tile < 16:
                            suit_pin[(tile % 9)] = 1

                        else:
                            suit_sou[(tile % 9)] = 1

            num_waiting = suit_wan.count(0) # get the suit with the most unique tiles counted
            if (num_waiting > suit_pin.count(0)):
                num_waiting = suit_pin.count(0)
                suit = "pin"
            if (num_waiting > suit_sou.count(0)):
                num_waiting = suit_sou.count(0)
                suit = "sou"
                
            if suit == "wan": # append to the list of waiting tiles for the most complete suit
                for i in range (0, 9):
                    if suit_wan[i] == 0:
                        tiles_needed_list.append(i)

            elif suit == "pin":
                for i in range (0, 9):
                    if suit_pin[i] == 0:
                        tiles_needed_list.append((i + 9))

            else:
                for i in range (0, 9):
                    if suit_sou[i] == 0:
                        tiles_needed_list.append((i + 18))

            if suit == "wan": # append to the list of used tiles for the most complete suit
                for i in range (0, 9):
                    if suit_wan[i] == 1:
                        tiles_used_list.append(i)

            elif suit == "pin":
                for i in range (0, 9):
                    if suit_pin[i] == 1:
                        tiles_used_list.append((i + 9))

            else:
                for i in range (0, 9):
                    if suit_sou[i] == 1:
                        tiles_used_list.append((i + 18))

            #print(tiles_needed_list)
            return_dict.setdefault("straight", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
            num_waiting = 0
            tiles_needed_list.clear()
            tiles_used_list.clear()

        # 6. three color seq
        # condition: 3 seq with the same index after mod 9
        if(len(meld)<2):
            min_waiting = 9
            waiting_tiles_list = ()
            used_tiles_list = ()

            for i in range(7):
                waiting_count = 9
                temp_wait_list = [i,i+1,i+2,i+9,i+10,i+11,i+18,i+19,i+20]
                temp_use_list = []
                for index in hand_partition['seq-complete']:
                    if (index % 9 == i):
                        # print(index)
                        # print(temp_wait_list)
                        # print(type(temp_wait_list))
                        # print(type(temp_wait_list[0]))
                        if index in temp_wait_list:
                            waiting_count -= 3
                            temp_wait_list.remove(index)
                            temp_wait_list.remove(index+1)
                            temp_wait_list.remove(index+2)
                            temp_use_list.append(index)
                            temp_use_list.append(index+1)
                            temp_use_list.append(index+2)

                for index in hand_partition['triplet']:
                    if (index % 9 == i):
                        if(index in temp_wait_list):
                            waiting_count -= 1
                            temp_wait_list.remove(index)
                            temp_use_list.append(index)
                
                for index in hand_partition['pair']:
                    if(index % 9 == i):
                        if(index in temp_wait_list):
                            waiting_count -= 1
                            temp_wait_list.remove(index)
                            temp_use_list.append(index)
                
                for index in hand_partition['single']:
                    if (index % 9 >= i and index % 9 <= i+2):
                        if(index in temp_wait_list):
                            waiting_count -= 1
                            temp_wait_list.remove(index)
                            temp_use_list.append(index)
                
                if(waiting_count < min_waiting):
                    min_waiting = waiting_count
                    waiting_tiles_list = tuple(temp_wait_list)
                    used_tiles_list = tuple(temp_use_list)

            
            value_list = [min_waiting, waiting_tiles_list, used_tiles_list, 'seq']
            return_dict.setdefault('three-color-seq', value_list)     

        # 7. three color triplet
        # condition: 3 triplet with the same index
        if len(meld) > 1: # & len(meld['seq-complete']) > 1: # if > 1 exposed sequence
            num_waiting = 99

        else:
            closest_index = 0
            suit_wanT = [0] * 9
            suit_pinT = [0] * 9
            suit_souT = [0] * 9
            closestT = [0] * 9

            for k, v in hand_partition.items(): # find and store # of tiles at indexes respective to suits
                for tile in v:
                    if tile < 27:
                        if 'triplet' in k:
                            if tile < 9:
                                suit_wanT[tile] += 3
                                            
                            elif 8 < tile < 18:
                                suit_pinT[(tile % 9)] += 3

                            else:
                                suit_souT[(tile % 9)] += 3

                        if 'pair' in k:
                            if tile < 9:
                                suit_wanT[tile] += 2
                                            
                            elif 8 < tile < 18:
                                suit_pinT[(tile % 9)] += 2

                            else:
                                suit_souT[(tile % 9)] += 2

                        if 'single' in k:
                            if tile < 9:
                                suit_wanT[tile] += 1
                                            
                            elif 8 < tile < 18:
                                suit_pinT[(tile % 9)] += 1

                            else:
                                suit_souT[(tile % 9)] += 1

                        if 'seq-complete' in k:
                            if tile < 7:
                                suit_wanT[tile] += 1
                                suit_wanT[(tile + 1)] += 1
                                suit_wanT[(tile + 2)] += 1

                                            
                            elif 8 < tile < 16:
                                suit_pinT[(tile % 9)] += 1
                                suit_pinT[((tile % 9) + 1)] += 1
                                suit_pinT[((tile % 9) + 2)] += 1

                            else:
                                suit_souT[(tile % 9)] += 1
                                suit_souT[((tile % 9) + 1)] += 1
                                suit_souT[((tile % 9) + 2)] += 1

            for i in range (0, 9): # find and store the closest 3 color triplet setup
                closestT[i] = [suit_wanT[i], suit_pinT[i], suit_souT[i], (suit_wanT[i] + suit_pinT[i] + suit_souT[i])]
                if num_waiting > abs(9 - closestT[i][3]):
                    num_waiting = abs(9 - closestT[i][3])
                    closest_index = i

            for i in range (0, 3): # append needed tiles list
                if closestT[closest_index][i] < 3:
                    if i == 0:
                        for j in range (0, (3 - closestT[closest_index][i])):
                            tiles_needed_list.append(closest_index)

                    if i == 1:
                        for j in range (0, (3 - closestT[closest_index][i])):
                            tiles_needed_list.append(closest_index + 9)

                    if i == 2:
                        for j in range (0, (3 - closestT[closest_index][i])):
                            tiles_needed_list.append(closest_index + 18)

            for i in range (0, 3): # append used tiles list
                if i == 0:
                    for j in range (0, closestT[closest_index][i]):
                        tiles_used_list.append(closest_index)

                if i == 1:
                    for j in range (0, closestT[closest_index][i]):
                        tiles_used_list.append(closest_index + 9)

                if i == 2:
                    for j in range (0, closestT[closest_index][i]):
                        tiles_used_list.append(closest_index + 18)

            return_dict.setdefault("3-color-triplet", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
            num_waiting = 0
            tiles_needed_list.clear()
            tiles_used_list.clear()

        ## above Dane  5-7 ##

        tiles_needed_list = []
        tiles_used_list = []

        num_pair = len(hand_partition['pair'])
        num_triplet = len(hand_partition['triplet'])
        num_seq = len(hand_partition['seq-complete'])

        # 8. all triplet
        # condition: 4 triplet ( or quads) with 1 pair  
        if num_triplet == 4: # 4 tri
            num_waiting = 0
        else: # less than 4 tri
            need_tri = 4 - num_triplet # triplet to complete
            num_waiting = need_tri * 2
            if(need_tri - num_pair < 0):
                num_waiting = num_pair + 2(need_tri - num_pair) 
            else: 
                num_waiting = num_waiting - num_pair # -1 for each extra pair            
        for k, v in hand_partition.items():
            for index in v:
                if 'triplet' in k:
                    tiles_used_list.extend([index, index, index])
                if 'pair' in k:
                    if need_tri > 0:       
                        tiles_used_list.extend([index, index])
                        tiles_needed_list.extend([index])
                if 'single' in k:
                    if ((need_tri - num_pair) > 0):
                        tiles_used_list.extend([index])
                        tiles_needed_list.extend([index])
        return_dict.setdefault("all_triplet", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])

        # 9. terminal in all meld
        # condition: (seq + triplet) = 4, index is 1 or 9 or honor, for seq check index+1 and index+2 
        num_com = 0
        num_almost = 0
        num_two = 0
        pair_used = 0
        tiles_needed_list.clear()
        tiles_used_list.clear()
        temp_used = []
        
        for k, v in hand_partition.items():
            for index in v:
                if 'triplet' in k:
                    if index < 26:
                        if((index % 9) in (0, 8)): # 111 OR 999
                            num_com = num_com + 1
                            tiles_used_list.extend([index, index, index])
                    else: # Honor
                        num_com = num_com + 1
                        tiles_used_list.extend([index, index, index])
                if 'seq-complete' in k: # 123 OR 789
                    if ((index % 9) in (0, 6)):
                        num_com = num_com + 1
                        tiles_used_list.extend([index, index+1, index+2])
                if 'seq-one-way' in k: # 12(3) OR (7)89     
                    if ((index % 9) == 0): # 12(3)
                        num_almost = num_almost + 1
                        tiles_needed_list.extend([index + 2]) # 3
                        temp_used.extend([index, index + 1])
                        tiles_used_list.extend([index, index + 1])
                    if ((index % 9) == 7): # (7)89
                        num_almost = num_almost + 1
                        tiles_needed_list.extend(index - 1) # 7
                        temp_used.extend([index, index + 1])
                        tiles_used_list.extend([index, index + 1])
                if 'seq-two-way' in k: # (1)23 OR 78(9) 
                    if ((index % 9) == 1): # (1)23
                        num_almost = num_almost + 1
                        tiles_needed_list.extend([index - 1]) # 1
                        temp_used.extend([index, index + 1])
                        tiles_used_list.extend([index, index + 1])
                    if ((index % 9) == 6): # 78(9)
                        num_almost = num_almost + 1
                        tiles_needed_list.extend([index + 2]) # 9
                        temp_used.extend([index, index + 1])
                        tiles_used_list.extend([index, index + 1])                      
                if 'seq-middle' in k: # 1(2)3 OR 7(8)9
                    if ((index % 9) == 0): # 1(2)3
                        num_almost = num_almost + 1
                        tiles_needed_list.extend([index + 1]) # 2
                        temp_used.extend([index, index + 2])
                        tiles_used_list.extend([index, index + 2])
                    if ((index % 9) == 6): # 7(8)9
                        num_almost = num_almost + 1
                        tiles_needed_list.extend([index + 1]) # 8
                        temp_used.extend([index, index + 2])
                        tiles_used_list.extend([index, index + 2])                     
                if 'pair' in k:
                    if((index % 9) in (0, 8)): #11 or 99
                        num_almost = num_almost + 1
                        pair_used = pair_used + 1
                        tiles_needed_list.extend([index]) # 1 or 9
                        tiles_used_list.extend([index, index])
                if 'single' in k:
                    if index not in temp_used:
                        if((num_com + num_almost) < 4):
                            if((index % 9) in (0, 6)): # 1 or 7             
                                num_two = num_two + 1 
                                tiles_needed_list.extend([index + 1, index + 2]) #23 or 89
                                tiles_used_list.extend([index])
                            if((index % 9) in (1, 7)): # 2 or 8
                                num_two = num_two + 1
                                tiles_needed_list.extend([index - 1, index + 1]) #13 or 79
                                tiles_used_list.extend([index])                       
                            if((index % 9) in (2, 8)): #3 or 9
                                num_two = num_two + 1
                                tiles_needed_list.extend([index - 1, index - 2]) #12 or 78
                                tiles_used_list.extend([index])
        
        needed_com = 4 - num_com
        if needed_com > 0:
            if (needed_com - num_almost)  < 1:
                num_waiting = needed_com
            elif (needed_com - num_almost - num_two) < 1:
                needed_com = needed_com - num_almost
                num_waiting = num_almost + (2 * needed_com)
            else:
                needed_com = needed_com - num_almost - num_two
                num_waiting = num_almost + (2 * num_two) + (3 * needed_com)            
        else:
            num_waiting = 0
        return_dict.setdefault("ternimal_in_all", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])

        
        # 10. seven pair 
        # condition: 7 pair partition
        tiles_needed_list.clear()
        tiles_used_list.clear()
        if len(meld) == 0:
            if num_pair < 7:
                temp = 7 - num_pair
                num_waiting = temp - num_triplet
            for k, v in hand_partition.items():
                for index in v:
                    if ('pair' in k):
                        tiles_used_list.extend([index, index])
                    if (('single' in k) and (num_pair < 7)):
                        tiles_needed_list.extend([index])
        else: num_waiting = 99         
        return_dict.setdefault("seven_pairs", [num_waiting, tuple(tiles_needed_list), tuple(tiles_used_list)])
        tiles_needed_list.clear()
        tiles_used_list.clear()        
        ## above Lee 8-10 ##
        
        return return_dict

    def complete_hand(self, hand_partition, meld):
        
        return
        

def main():
    mai = Mahjong_AI()
    hand_partition = {'seq-complete':[9,18], 'seq-middle': [], 'seq-two-way': [1], 'pair': [7], 
                        'triplet': [5], 'single': [1,2], 'seq-one-way': []}
    meld = []
    print(mai.yaku_check(hand_partition, meld))

if __name__ == '__main__':
    main()
