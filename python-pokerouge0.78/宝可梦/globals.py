import all_poke
import random
import all_skills
import json 
import all_tools

def save_player_data(player):
    """保存玩家数据到文件"""
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

def get_exp(wild_poke):
    """获取野生宝可梦的经验值"""
    return wild_poke.level * 10 + wild_poke.EXP * 2 * wild_poke.level * 4

def choose_player_poke(player, allow_return=True):
    """选择玩家的宝可梦"""
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
    """战斗系统"""
    # 初始化时就创建实例
    player_poke = None
    
    # 检查是否有可用的宝可梦
    available_pokes = [
        (slot, poke) for slot, poke in player.pokemon_slots.items() 
        if poke and poke["Hp"] > 0
    ]
    
    if not available_pokes:
        print("你没有可以战斗的宝可梦了！")
        return
        
    # 如果slot1有活着的宝可梦就用它，否则让玩家选择
    if player.pokemon_slots.get('slot1') and player.pokemon_slots['slot1']["Hp"] > 0:
        player_poke = all_poke.PlayerPoke(player.pokemon_slots.get('slot1'))
    else:
        print("请选择宝可梦！")
        selected_poke = choose_player_poke(player, allow_return=False)
        if not selected_poke:
            return
        player_poke = all_poke.PlayerPoke(selected_poke)

    # 初始化战斗
    print(f"战斗开始！\n玩家宝可梦：{player_poke.name} 等级: {player_poke.level}")
    print(f"野生宝可梦：{wild_poke.name} 等级: {wild_poke.level}")
    round = 1
    
    while True:
        action_completed = False  # 标记是否完成了有效的行动
        
        while not action_completed:  # 直到完成有效的行动才能结束回合
            print(f"\n玩家宝可梦：{player_poke.name} 当前Hp: {player_poke.Hp}")
            print(f"野生宝可梦：{wild_poke.name} 当前Hp: {wild_poke.Hp}\n")
            print("请选择你的行动：")
            print("1. 攻击")
            print("2. 使用道具")
            print("3. 更换宝可梦")
            print("4. 退出")
            print("5. 查看当前宝可梦状态")
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
                    print("0. 返回主菜单")
                    print("\n请选择技能：")
                    
                    for idx, skill in enumerate(player_poke.skills, start=1):
                        print(f"{idx}. {skill['name']} (PP: {skill['Pp']})")

                    try:
                        skill_choice = int(input("请输入技能的编号："))
                        if skill_choice == 0:  # 返回主菜单
                            break
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
                        action_completed = True
                        
                        # 更新玩家宝可梦数据
                        for slot, poke in player.pokemon_slots.items():
                            if poke and poke["name"] == player_poke.name:
                                poke["skills"] = player_poke.skills
                                break
                        save_player_data(player)
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
                        break
                    try:
                        choice_idx = int(tool_choice) - 1
                        if 0 <= choice_idx < len(player.tools):
                            tool_name = list(player.tools.keys())[choice_idx]
                            tool_data = player.tools[tool_name]
                            if tool_data['num'] <= 0:
                                print("该道具数量不足！请选择其他道具。")
                                continue
                            tool_obj = all_tools.get_tool_by_name(tool_name, tool_data['num'])
                            # 处理精灵球的特殊情况
                            if tool_name in ["精灵球", "超级球", "高级球", "大师球"]:
                                print(f"\n尝试捕捉 {wild_poke.name}...")
                                if tool_obj.UseTools(wild_poke):
                                    print(f"成功捕捉了 {wild_poke.name}!")
                                    tool_data['num'] -= 1
                                    # 创建完整的宝可梦数据
                                    wild_poke_data = {
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
                                        "EXP": 0,
                                        "NeedEXP": wild_poke.NeedEXP,
                                        "skills": wild_poke.skills,
                                        "learn_skills": wild_poke.learn_skills
                                    }
                                    
                                    # 寻找空槽位并保存
                                    for slot in ["slot1", "slot2", "slot3", "slot4", "slot5", "slot6"]:
                                        if not player.pokemon_slots.get(slot):
                                            player.pokemon_slots[slot] = wild_poke_data
                                            break
                                    save_player_data(player)
                                    return
                                else:
                                    print(f"{wild_poke.name} 挣脱了精灵球!")
                                    tool_data['num'] -= 1
                                    action_completed = True
                                    save_player_data(player)
                                    break
                            else:
                                # 其他道具的使用逻辑
                                print(f"\n选择要使用 {tool_data['name']} 的目标：")
                                # 显示所有宝可梦，不仅仅是当前战斗的
                                available_pokes = []
                                for slot, poke in player.pokemon_slots.items():
                                    if poke:  # 确保槽位有宝可梦
                                        try:
                                            # 创建一个临时的PlayerPoke实例来确保数据完整性
                                            temp_poke = all_poke.PlayerPoke(poke)
                                            available_pokes.append((slot, temp_poke))
                                        except Exception as e:
                                            print(f"警告：槽位 {slot} 的宝可梦数据可能损坏: {e}")
                                            continue

                                if not available_pokes:
                                    print("没有可用的宝可梦！")
                                    continue
                                for idx, (slot, poke) in enumerate(available_pokes, 1):
                                    print(f"{idx}. {poke.name} (槽位: {slot}, HP: {poke.Hp}/{poke.HP})")
                                print("0. 返回")
                                target_choice = input("请选择目标宝可梦: ").strip()
                                if target_choice == '0':
                                    continue
                                try:
                                    target_idx = int(target_choice) - 1
                                    if 0 <= target_idx < len(available_pokes):
                                        target_slot, target_poke = available_pokes[target_idx]
                                        if tool_obj.UseTools(target_poke):
                                            print(f"成功使用了 {tool_data['name']}!")
                                            tool_data['num'] -= 1
                                            # 更新宝可梦状态
                                            player.pokemon_slots[target_slot] = target_poke.to_dict()
                                            save_player_data(player)
                                            action_completed = True
                                            # 如果是当前战斗的宝可梦，更新其状态
                                            if target_poke.name == player_poke.name:
                                                player_poke = target_poke
                                            break
                                        else:
                                            print("道具使用失败!")
                                            continue
                                    else:
                                        print("无效的选择!")
                                        continue
                                except ValueError:
                                    print("请输入有效的数字!")
                                    continue
                        else:
                            print("无效的道具编号!")
                            continue
                    except ValueError:
                        print("请输入有效的数字!")
                        continue

            elif action == '3':
                # 先保存当前宝可梦状态
                for slot, poke in player.pokemon_slots.items():
                    if poke and poke["name"] == player_poke.name:
                        poke.update({
                            "Hp": player_poke.Hp,
                            "EXP": player_poke.EXP,
                            "level": player_poke.level,
                            "ATK": player_poke.ATK,
                            "DEF": player_poke.DEF,
                            "SPD": player_poke.SPD,
                            "HP": player_poke.HP,
                            "NeedEXP": player_poke.NeedEXP,
                            "skills": player_poke.skills
                        })
                        break
                
                new_poke = choose_player_poke(player)
                if new_poke:
                    player_poke = all_poke.PlayerPoke(new_poke)
                    action_completed = True
                    save_player_data(player)

            elif action == '4':
                # 保存当前宝可梦状态后退出
                for slot, poke in player.pokemon_slots.items():
                    if poke and poke["name"] == player_poke.name:
                        poke.update({
                            "Hp": player_poke.Hp,
                            "EXP": player_poke.EXP,
                            "level": player_poke.level,
                            "ATK": player_poke.ATK,
                            "DEF": player_poke.DEF,
                            "SPD": player_poke.SPD,
                            "HP": player_poke.HP,
                            "NeedEXP": player_poke.NeedEXP,
                            "skills": player_poke.skills
                        })
                        break
                save_player_data(player)
                print("成功逃跑了")
                return

            elif action == '5':
                print("体力值:{}/{}".format(player_poke.Hp,player_poke.HP))
                print("等级:{}".format(player_poke.level))
                print("经验值:{}/{}".format(player_poke.EXP,player_poke.NeedEXP))
                what = input("继续游戏[y/n]")
                if what == "y":
                    continue
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
            
            # 更新玩家宝可梦数据
            for slot, poke in player.pokemon_slots.items():
                if poke and poke["name"] == player_poke.name:
                    poke["Hp"] = player_poke.Hp
                    break
            save_player_data(player)

        if not player_poke.IsAlive():
            print(f"{player_poke.name} 被击败了！")
            # 更新玩家存档中的宝可梦数据
            for slot, poke in player.pokemon_slots.items():
                if poke and poke["name"] == player_poke.name:
                    poke["Hp"] = player_poke.Hp
                    break
            
            selected_poke = choose_player_poke(player, allow_return=False)
            if not selected_poke:
                print("你没有可以战斗的宝可梦了！战斗失败！")
                save_player_data(player)
                return
            player_poke = all_poke.PlayerPoke(selected_poke)

        # 检查战斗是否结束
        if not wild_poke.IsAlive():
            print(f"\n{player_poke.name} 胜利！")
            exp = get_exp(wild_poke)
            player_poke.exp_up(exp)
            print(f"{player_poke.name} 获得了10点经验！")
            
            # 更新玩家存档中的宝可梦数据
            for slot, poke in player.pokemon_slots.items():
                if poke and poke["name"] == player_poke.name:
                    poke.update({
                        "Hp": player_poke.Hp,
                        "EXP": player_poke.EXP,
                        "level": player_poke.level,
                        "ATK": player_poke.ATK,
                        "DEF": player_poke.DEF,
                        "SPD": player_poke.SPD,
                        "HP": player_poke.HP,
                        "Hp": player_poke.Hp,
                        "EXP": player_poke.EXP,
                        "NeedEXP": player_poke.NeedEXP,
                        "skills": player_poke.skills,
                        "learn_skills": player_poke.learn_skills
                    })
                    break
            
            save_player_data(player)
            return

        round += 1
        print(f"第{round}回合")

def reward(player):
    """战斗后的奖励系统"""
    print("\n------奖励回合------")
    
    # 从tools.json中获取所有可能的道具
    with open('tools.json', 'r', encoding='utf-8') as f:
        tools_data = json.load(f)
    available_tools = list(tools_data[0].keys())
    
    # 随机选择两个不同的道具
    tool_rewards = random.sample(available_tools, 2)
    
    # 定义能力提升选项（包括基础属性和成长值）
    stat_rewards = [
        ("ATK提升", "提升宝可梦的攻击力5点"),
        ("DEF提升", "提升宝可梦的防御力5点"),
        ("SPD提升", "提升宝可梦的速度5点"),
        ("HP提升", "提升宝可梦的最大HP5点"),
        ("ATK成长提升", "提升宝可梦的攻击成长1点"),
        ("DEF成长提升", "提升宝可梦的防御成长1点"),
        ("SPD成长提升", "提升宝可梦的速度成长1点"),
        ("HP成长提升", "提升宝可梦的HP成长1点")
    ]
    
    # 随机选择一个能力提升
    stat_reward = random.choice(stat_rewards)
    
    # 组合奖励选项
    rewards = [
        (tool_rewards[0], f"获得道具: {tool_rewards[0]}"),
        (tool_rewards[1], f"获得道具: {tool_rewards[1]}"),
        (stat_reward[0], stat_reward[1])
    ]
    
    print("请选择一个奖励：")
    for i, (reward_name, description) in enumerate(rewards, 1):
        print(f"{i}. {description}")
        
    while True:
        try:
            choice = int(input("输入奖励编号(1-3): "))
            if 1 <= choice <= 3:
                selected_reward = rewards[choice-1]
                reward_name = selected_reward[0]
                
                # 处理道具奖励
                if reward_name in available_tools:
                    print(f"\n获得了 {reward_name}!")
                    use_now = input("是否立即使用？(y/n): ").lower()
                    
                    if use_now == 'y':
                        print("\n选择要使用道具的宝可梦：")
                        target_poke = choose_player_poke(player)
                        if target_poke:
                            tool_obj = all_tools.get_tool_by_name(reward_name, 1)
                            poke_instance = all_poke.PlayerPoke(target_poke)
                            if tool_obj.UseTools(poke_instance):
                                # 更新宝可梦状态
                                for slot, poke in player.pokemon_slots.items():
                                    if poke and poke["name"] == target_poke["name"]:
                                        poke.update({
                                            "Hp": poke_instance.Hp,
                                            "HP": poke_instance.HP,
                                            "skills": poke_instance.skills
                                        })
                                save_player_data(player)
                    else:
                        # 将道具添加到玩家背包
                        if reward_name in player.tools:
                            player.tools[reward_name]["num"] += 1
                        else:
                            tool_data = all_tools.tool[reward_name]
                            player.tools[reward_name] = {
                                "name": tool_data.name,
                                "num": 1,
                                "ToolsType": tool_data.ToolsType,
                                "GetType": tool_data.GetType,
                                "BloodType": tool_data.BloodType,
                                "LifeType": tool_data.LifeType,
                                "PpType": tool_data.PpType
                            }
                        save_player_data(player)
                        print(f"{reward_name} 已添加到背包!")
                
                # 处理能力提升奖励
                else:
                    print(f"\n获得了 {reward_name}!")
                    print("选择要强化的宝可梦：")
                    target_poke = choose_player_poke(player)
                    if target_poke:
                        poke_instance = all_poke.PlayerPoke(target_poke)
                        if "ATK提升" == reward_name:
                            poke_instance.ATK += 5
                        elif "DEF提升" == reward_name:
                            poke_instance.DEF += 5
                        elif "SPD提升" == reward_name:
                            poke_instance.SPD += 5
                        elif "HP提升" == reward_name:
                            poke_instance.HP += 5
                            poke_instance.Hp += 5
                        elif "ATK成长提升" == reward_name:
                            poke_instance.atk += 1
                        elif "DEF成长提升" == reward_name:
                            poke_instance.Def += 1
                        elif "SPD成长提升" == reward_name:
                            poke_instance.spd += 1
                        elif "HP成长提升" == reward_name:
                            poke_instance.hp += 1
                            
                        # 更新宝可梦状态
                        for slot, poke in player.pokemon_slots.items():
                            if poke and poke["name"] == target_poke["name"]:
                                poke.update({
                                    "ATK": poke_instance.ATK,
                                    "DEF": poke_instance.DEF,
                                    "SPD": poke_instance.SPD,
                                    "HP": poke_instance.HP,
                                    "Hp": poke_instance.Hp,
                                    "EXP": poke_instance.EXP,
                                    "NeedEXP": poke_instance.NeedEXP,
                                    "skills": poke_instance.skills,
                                    "atk": poke_instance.atk,
                                    "Def": poke_instance.Def,
                                    "spd": poke_instance.spd,
                                    "hp": poke_instance.hp
                                })
                        save_player_data(player)
                        print(f"{target_poke['name']} 的能力得到了提升！")
                
                break
            else:
                print("请输入1-3之间的数字！")
        except ValueError:
            print("请输入有效的数字！")