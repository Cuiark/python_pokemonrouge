import all_poke
import randompoke
import players 
import globals

name = input("you name: ")
player1 = players.Player.login(name)
big_round = 0

while True:
    available_pokes = [
        (slot, poke) for slot, poke in player1.pokemon_slots.items() 
        if poke and poke["Hp"] > 0
    ]
    
    if not available_pokes:
        print(f"你没有可以战斗的宝可梦了！游戏结束！")
        break
    
    big_round += 1
    print(f"第{big_round}轮开始")
    
    # 先进行战斗
    globals.battle(player1, randompoke.randompokes())
    
    # 战斗结束后给予奖励
    print("\n战斗结束，获得奖励！")
    globals.reward(player1)
    
    # 保存数据
    globals.save_player_data(player1)