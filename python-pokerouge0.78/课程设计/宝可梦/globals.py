import all_poke
import random
import all_skills
import json
import all_tools
import players

def save_player_data(player):
    try:
        with open('playerpoke.json', 'r', encoding='utf-8') as f:
            poke_data = json.load(f)
    except FileNotFoundError:
        poke_data = {}
    poke_data[player.name] = player.pokemon_slots
    with open('playerpoke.json', 'w', encoding='utf-8') as f:
        json.dump(poke_data, f, ensure_ascii=False, indent=4)
    try:
        with open('playertools.json', 'r', encoding='utf-8') as f:
            tools_data = json.load(f)
    except FileNotFoundError:
        tools_data = {}
    tools_data[player.name] = player.tools
    with open('playertools.json', 'w', encoding='utf-8') as f:
        json.dump(tools_data, f, ensure_ascii=False, indent=4)

def choose_player_poke(player, allow_return=True):
    while True:
        print("请选择一个宝可梦出战：")
        available_pokes = [
            (slot, poke) for slot, poke in player.pokemon_slots.items() if poke and poke["Hp"] > 0
        ]
        if not available_pokes:
            print("你没有可以战斗的宝可梦了！")
            return None
            
        if allow_return:
            print("0. 返回主菜单")
        for idx, (slot, poke) in enumerate(available_pokes, start=1):
            print(f"{idx}. {poke['name']} (槽位: {slot}, 当前Hp: {poke['Hp']})")
        try:
            choice = int(input("输入宝可梦编号："))
            if allow_return and choice == 0:
                return None
            if 1 <= choice <= len(available_pokes):
                return available_pokes[choice - 1][1]
            print("输入无效，请重新选择！")
        except (ValueError, IndexError):
            print("输入无效，请重新选择！")

def battle(player, wild_poke):
    player_poke = player.pokemon_slots.get('slot1')  # 默认第一个槽位的宝可梦出场
    if not player_poke:
        print("请选择宝可梦！")
        player_poke = choose_player_poke(player, allow_return=False)
        if not player_poke:
            return

    player_poke = all_poke.PlayerPoke(player_poke)  # 获取玩家宝可梦实例

    # 初始化
    print(f"战斗开始！\n玩家宝可梦：{player_poke.name} 等级: {player_poke.level}")
    print(f"野生宝可梦：{wild_poke.name} 等级: {wild_poke.level}")
    round = 1
    available_pokes = [
        (slot, poke) for slot, poke in player.pokemon_slots.items() if poke and poke["Hp"] > 0
    ]
    
    while available_pokes and wild_poke.IsAlive():
        action_completed = False  # 标记是否完成了有效的行动
        
        while not action_completed:  # 直到完成有效的行动才能结束回合
            print(f"\n玩家宝可梦：{player_poke.name} 当前Hp: {player_poke.Hp}")
            print(f"野生宝可梦：{wild_poke.name} 当前Hp: {wild_poke.Hp}\n")
            print("请选择你的行动：")
            print("1. 攻击")
            print("2. 使用道具")
            print("3. 更换宝可梦")
            print("4. 退出")
            action = input("请输入选择: ")

            if action == '1':
                while True:  # 技能选择循环
                    has_available_skill = False
                    for skill in player_poke.skills:
                        if skill['Pp'] > 0:
                            has_available_skill = True
                            break

                    if not has_available_skill:
                        print("所有技能的PP都已用完！请使用PP恢复道具或选择其他操作。")
                        break  

                    print("\n请选择技能：")
                    print("0. 返回主菜单")
                    for idx, skill in enumerate(player_poke.skills, start=1):
                        print(f"{idx}. {skill['name']} (PP: {skill['Pp']})")

                    try:
                        skill_choice = int(input("请输入技能的编号："))
                        if skill_choice == 0:  # 返回主菜单
                            break  # 只退出技能选择循环，不完成行动
                        if skill_choice < 1 or skill_choice > len(player_poke.skills):
                            print(f"请输入0到{len(player_poke.skills)}之间的数字！")
                            continue

                        skill = player_poke.skills[skill_choice - 1]
                        if skill["Pp"] <= 0:
                            print(f"{skill['name']} 的 PP 已用完！请选择其他技能。")
                            continue

                        skill_obj = all_skills.get_skill_by_name(skill["name"], skill["Pp"])
                        damage = skill_obj.apply(player_poke, wild_poke)
                        if damage == 0:
                            continue

                        skill["Pp"] = skill["Pp"] - 1
                        all_skills.ApplyDmage(player_poke, wild_poke, damage, skill_obj)
                        action_completed = True  # 成功使用技能后设置为True
                        break
                    except ValueError:
                        print("请输入有效的数字！")
                        continue

            elif action == '2':
                while True:  # 道具使用循环
                    print("\n你的道具:")
                    if not player.tools:
                        print("你没有任何道具!")
                        break

                    print("0. 返回主菜单")
                    for idx, (tool_name, tool_data) in enumerate(player.tools.items(), 1):
                        print(f"{idx}. {tool_data['name']} (数量: {tool_data['num']})")

                    tool_choice = input("输入道具编号使用，或输入 '0' 返回: ").strip()

                    if tool_choice == '0':
                        break  # 只退出道具选择循环，不完成行动

                    try:
                        choice_idx = int(tool_choice) - 1
                        if 0 <= choice_idx < len(player.tools):
                            tool_name = list(player.tools.keys())[choice_idx]
                            tool_data = player.tools[tool_name]
                            if tool_data['num'] <= 0:
                                print("该道具数量不足！请选择其他道具。")
                                continue
                                
                            tool_obj = all_tools.get_tool_by_name(tool_name,tool_data['num'])
                            print(f"\n使用 {tool_data['name']} 于:")
                            print(f"1. {player_poke.name} (我方, HP: {player_poke.Hp}/{player_poke.HP})")

                            target_choice = input("请选择目标 (输入1): ").strip()
                            if target_choice == '1':
                                if tool_obj.UseTools(player_poke):
                                    print(f"成功使用了 {tool_data['name']}!")
                                    tool_data['num'] -= 1
                                    all_skills.save_player_poke(player)
                                    action_completed = True  # 成功使用道具后设置为True
                                    break
                                else:
                                    print("道具使用失败!")
                                    continue
                            else:
                                print("无效的选择!")
                                continue
                        else:
                            print("无效的道具编号!")
                            continue
                    except ValueError:
                        print("请输入有效的数字!")
                        continue

            elif action == '3':
                new_poke = choose_player_poke(player)
                if new_poke:
                    player_poke = all_poke.PlayerPoke(new_poke)
                    action_completed = True  # 成功更换宝可梦后设置为True

            elif action == '4':
                print("成功逃跑了")
                return

            else:
                print("无效的选择！")
                continue

        # 只有在完成有效行动后才执行野生宝可梦的回合
        if action_completed and player_poke.IsAlive() and wild_poke.IsAlive():
            wild_skill = random.choice(wild_poke.skills)
            wild_skill_obj = all_skills.get_skill_by_name(wild_skill["name"], wild_skill["Pp"])
            if not wild_skill_obj.has_pp():
                print(f"{wild_poke.name} 的 {wild_skill['name']} 的 PP 已用完！")
                continue
            wild_skill["Pp"] = wild_skill["Pp"] - 1
            damage = wild_skill_obj.apply(wild_poke, player_poke)
            all_skills.ApplyDmage(wild_poke, player_poke, damage, wild_skill_obj)
            
            # 每回合结束时保存数据
            save_player_data(player)

            with open("wildpoke.json", 'w', encoding='utf-8') as file:
                wild_data = {
                    "name": wild_poke.name,
                    "attribute": wild_poke.attribute,
                    "attributes": wild_poke.attributes,
                    "level": wild_poke.level,
                    "ATK": wild_poke.ATK,
                    "DEF": wild_poke.DEF,
                    "SPD": wild_poke.SPD,
                    "ACC": wild_poke.ACC,
                    "HP": wild_poke.HP,
                    "Hp": wild_poke.Hp,
                    "EXP": wild_poke.EXP,
                    "NeedEXP": wild_poke.NeedEXP,
                    "skills": wild_poke.skills,
                    "learn_skills": wild_poke.learn_skills
                }
                json.dump(wild_data, file, ensure_ascii=False, indent=4)

        if not player_poke.IsAlive():
            print(f"{player_poke.name} 被击败了！")
            player_poke = choose_player_poke(player, allow_return=False)
            if not player_poke:
                print("你没有可以战斗的宝可梦了！战斗失败！")
                return
            player_poke = all_poke.PlayerPoke(player_poke)

        available_pokes = [
            (slot, poke) for slot, poke in player.pokemon_slots.items() if poke and poke["Hp"] > 0
        ]

        if action_completed:  # 只有在完成有效行动后才增加回合数
            round += 1
            print(f"第{round}回合")

    # 战斗结果
    if player_poke.IsAlive():
        print(f"\n{player_poke.name} 胜利！")
        player_poke.exp_up(10)
        print(f"{player_poke.name} 获得了10点经验！")
    else:
        print(f"\n{wild_poke.name} 胜利！")
        print(f"{player_poke.name} 被击败！")