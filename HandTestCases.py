import MahjongAgent as ma
import Mahjong_AI as mai

def main():   
    test_hands = [  [1,2,3,4,5,6,9,10,11,15,16,32,32,33],
                    [0,2,3,4,5,6,9,10,11,15,16,32,32,33]]
    agent = ma.MahjongAgent()
    ai = mai.Mahjong_AI()
    for i in test_hands:
        print("Testing Hand {}".format(i))
        print(agent.partition_dict(i,'seq'))
        print(ai.yaku_check(agent.partition_dict(i,'seq'),''))
        print("="*20)

if __name__ == '__main__':
    main()
   