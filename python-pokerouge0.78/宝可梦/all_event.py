# 随机事件（娱乐事件） 对战事件  宿敌对战事件 普通事件
import players
import randompoke
#事件：注册,第一次游戏:
def FristTime():
    name_player = input("你的名字:")
    player1 = players.player(name_player)
    selected_pokemon = players.choose_pokemons()
    if selected_pokemon:
        print(selected_pokemon)
        player1.get_poke(selected_pokemon)
    else:
        print("没有选择宝可梦。")
    return player1
#事件:遇到宝可梦：
def Find_poke():
    print("发现了一只宝可梦！")
    wild_poke = randompoke.randompoke()
    return wild_poke
#发生对战

