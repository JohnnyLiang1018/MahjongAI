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
    # glc.db_show_tables()
    Errors = {}
    if path.exists('test.csv'):     
        remove('test.csv')
    header = []
    for i in range(9):
        header.append('Discard_{}'.format(i))
    header.append('waiting_tile')
    with open('test.csv', 'a') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(header)
        
    for i in range(5):
        try:
            log = gene.__next__()
            res = mjkit.PreProcessing.process_one_log(log)
        except Exception as e:
            Errors[i] = e
            pass
        for r, sa in res.items():
            for state in sa[-1:]:
                random_tile = random.randrange(34)
                testhand = state.s_hand34
                testhand.append(random_tile)
                testhand.sort()
                discard = state.s_discard34[:9]
                row = []
                row.extend(discard)
                row.append(state.s_hand34)
                print('discard and hand:', row)
                # waiting = waiting_calc(hand) ###TODO####
                # draw_tile = random_tile() todo
                waiting_tile = []
                waiting_dict = agent.tenpai_status_check(testhand)
                print('waiting_dict:', waiting_dict)
                for dis in waiting_dict:
                    waiting_tile.append(waiting_dict[dis])
                row.append(waiting_tile)

                print('final:', row)
                # with open('test.csv', 'a') as csvFile:
                #     wr = csv.writer(csvFile)
                #     wr.writerow(row)

    # print('Finished Writing to CSV')



if __name__ == '__main__':
    main()