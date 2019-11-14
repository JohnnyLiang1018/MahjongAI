import random

import MahjongKit as mjkit
import MahjongAgent as mjagent

import MahjongAgent as ma
import Mahjong_AI as mai

def main():   
    test_hands =    [  
                        [1,2,3,4,5,6,9,10,11,15,16,32,32,33],
                        [0,2,3,4,5,6,9,10,11,15,16,32,32,33],
                        [1,2,3,1,2,3,5,6,5,6,10,12,10,12,32],
                        [0,0,0,1,2,4,5,5,5,6,6,15,16,17],
                        [1,2,3,5,5,5,6,6,6,14,15,16,19,19],
                        [0,3,4,8,10,10,15,18,19,20,20,31,32, 33]
                    ]

    agent = ma.MahjongAgent()
    ai = mai.Mahjong_AI()
    for i in test_hands:
        print("Testing Hand {}".format(i))
        print(agent.partition_dict(i,'seq'))
        print(ai.yaku_check(agent.partition_dict(i,'seq'),''))
        print("="*20)

if __name__ == '__main__':
    main()
   