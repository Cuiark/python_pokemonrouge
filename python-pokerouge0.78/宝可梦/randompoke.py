import json
import random
import all_poke

# 读取玩家数据
def randompokes():
    try:
        with open("playerpoke.json", 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                player_data = json.loads(content)
            else:
                raise json.JSONDecodeError("Empty file", content, 0)

    except (FileNotFoundError, json.JSONDecodeError):
        player_data = {}  # 初始化为空数据
        with open("playerpoke.json", 'w', encoding='utf-8') as file:
            json.dump(player_data, file, ensure_ascii=False, indent=4)

    # 找到最高等级
    max_level = -1
    for slot, pokemon in player_data.items():
        if pokemon and isinstance(pokemon, dict) and "level" in pokemon:
            max_level = max(max_level, pokemon["level"])

    # 根据随机等级实例化宝可梦
    down_level = max_level - 3
    if down_level <= 0:
        down_level = 2
    up_level = max_level + 3
    now_level = random.randint(down_level, up_level)
    random_poke = random.sample(all_poke.pokemons, 1)
    wild = all_poke.wildpoke(random_poke[0][1], level=now_level)
    print(wild.skills)
    # 保存实例化的宝可梦到文件，包括名字、等级、技能等信息
    try:
        with open("wildpoke.json", 'r+', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                wild_data = json.loads(content)
            else:
                wild_data = {"Wild": {}}
    except (FileNotFoundError, json.JSONDecodeError):
        wild_data = {"Wild": {}}

    # 更新 wild 数据
    wild_data["Wild"] = {
        "name": wild.name,
        "attribute": wild.attribute,
        "attributes": wild.attributes,
        "level": wild.level,
        "ATK": wild.ATK,
        "DEF": wild.DEF,
        "SPD": wild.SPD,
        "ACC": wild.ACC,
        "HP": wild.HP,
        "Hp": wild.Hp,
        "EXP": wild.EXP,
        "NeedEXP": wild.NeedEXP,
        "skills": wild.skills,
        "learn_skills": wild.learn_skills
    }

    # 将更新后的数据保存到文件
    with open("wildpoke.json", 'w', encoding='utf-8') as file:
        json.dump(wild_data, file, ensure_ascii=False, indent=4)

    return wild

'''
#这里觉得要先定义道具类
def get_poke_random(poke,tools):
    options = [True,False]
    #捕捉率= (最大HP×3-当前HP×2)÷ (最大HP×3)×精灵捕获系数×精灵球系数×状态系数÷255
    how_true = (poke.HP * 3 - poke.Hp * 2) / (poke.HP * 3) * tools
'''