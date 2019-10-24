import csv
import random

import MahjongKit as mjkit
import MahjongAgent as mjagent

from os import path
from os import remove


def main():
    random.seed()
    glc = mjkit.GameLogCrawler()
    agent = mjagent.MahjongAgent()
    gene = glc.db_get_logs_where_players_lv_gr(19)
    glc.db_show_tables()
    if path.exists('test.csv'):     
        remove('test.csv')
    with open('test.csv', 'a') as csvFile:
        wr = csv.writer(csvFile, lineterminator='\n')
        header = []
        for i in range(34):
            header.append('discard_tile_{}'.format(i))
            header.append('discard_list')
            header.append('hand')
            header.append('meld')
            # header.append('random_tile')
            header.append('random_man')
            header.append('random_pin')
            header.append('random_sou')
            header.append('random_honor')
            for i in range(9):
                header.append('random_tile_num_{}'.format(i))
            header.append('waiting_tile')
            header.append('result')
            wr.writerow(header)
        for i in range(5):
            try:
                log = gene.__next__()
                res = mjkit.PreProcessing.process_one_log(log)
                for r, sa in res.items():
                    for state in sa[-1:]:
                        if(len(state.s_discard34) < 9):
                            continue
                        random_tile = random.randrange(34)
                        testhand = []
                        testhand = state.s_hand34
                        testhand.append(random_tile)
                        testhand.sort()
                        waiting_tile = []
                        waiting_dict = agent.tenpai_status_check(testhand)
                        # print('waiting_dict:', waiting_dict)
                        for key in waiting_dict:
                            # print("Key:", key, "Waiting Tiles:", waiting_dict[key])
                            if(type(waiting_dict[key]) is int):
                                waiting_tile.append(waiting_dict[key])
                            else: waiting_tile.extend(waiting_dict[key])
                        for play_tile in range(34):
                            # play_tile = random.ran
                            # play_tile = random.randrange(34)
                            play_tile_attr = [0] * 4
                            play_tile_num = [0] * 9
                            play_tile_attr[play_tile // 9] = 1
                            play_tile_num[play_tile % 9] = 1
                            row = []
                            for j in range(34):
                                if j in state.s_discard34:
                                    row.append(1)
                                else: row.append(0)
                            if play_tile in waiting_tile:
                                result = 1
                            else: 
                                result = 0
                            # row.append(state.s_hand34)
                            row.append(state.s_discard34)
                            row.append(testhand)
                            row.append(state.s_meld34)
                            # row.append(play_tile)
                            row.extend(play_tile_attr)
                            row.extend(play_tile_num)
                            # print('discard and hand:', row)
                            row.append(waiting_tile)
                            row.append(result)
                            print('final:', row)
                            # wr = csv.writer(csvFile)
                            wr.writerow(row)
                print("Finished writing log {}".format(i))
            except Exception as e:
                print(e)
                pass
    # print('Finished Writing to CSV')



if __name__ == '__main__':
    main()