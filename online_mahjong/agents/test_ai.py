from agents.ai_interface import AIInterface
from agents.utils.wait_calc import WaitCalc
from agents.utils.win_calc import WinCalc
from client.mahjong_meld import Meld
from client.mahjong_tile import Tile
from client.mahjong_player import OpponentPlayer
from client.mahjong_table import GameTable
import pickle
import numpy as np

class testAI(AIInterface):

    def to_discard_tile(self):
        input = np.zeros((14,47))
        opponents_list = self.game_table.get_opponents()
        mlp = pickle.load(open('mlp_model.sav','rb'))
        weight_sum_list = np.zeros((14,2))
        for opponent in opponents_list:
            for i in range(14):
                tile = self.hand34[i]
                tile_attr = tile // 9
                tile_num = tile % 9
                input[i][34 + tile_attr] = 1
                input[i][37 + tile_num] = 1 
                
                for discard in opponent.discard34:
                    input[i][discard] = 1
                
            prediction = mlp.predict_proba(input)
            weight_sum_list = np.add(weight_sum_list,prediction)
        
        
        min_value = 1
        min_index = 1
        for i in range(14):
            if(weight_sum_list[i][1] < min_value):
                min_value = weight_sum_list[i][1]
                min_index = i
        
        return self.tile_34_to_136(self.hand34[min_index])
            
    
    def should_call_kan(self,tile136,from_opponent):
        return False, False

    def try_to_call_meld(self,tile136,might_call_chi):
        return None,None

    def can_call_reach(self):
        return False, 0


    def model_testing(self,hand,opponent_discard):
        input = np.zeros((14,47))
        for i in range(14):
            tile = hand[i]
            tile_attr = tile // 9
            tile_num = tile % 9
            input[i][34+tile_attr] = 1
            input[i][37+tile_num] = 1
            for discard in opponent_discard:
                input[i][discard] = 1
        
        mlp = pickle.load(open('mlp_model.sav','rb'))
        predictions = mlp.predict_proba(input)
        print(predictions)

        # predictions_prob = (mlp.predict_proba(input)[:,1] >= 0.001).astype(int)
        min_value = 1
        min_index = -1
        for i in range(14):
            if(predictions[i][1] < min_value):
                min_value = predictions[i][1]
                min_index = i
        
        return min_index

# hand = [1,3,5,7,8,12,15,19,21,22,23,24,26,31]
# opponent_discard = [1,2,3,4,5,6,7,8]

# dummy = testAI()
# print(dummy.model_testing(hand,opponent_discard))
                

