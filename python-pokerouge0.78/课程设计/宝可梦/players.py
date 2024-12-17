#import all_skills
import all_poke
import random
import json

def choose_pokemons(player, num_choices=3):
    """随机选择 num_choices 个宝可梦并添加到指定玩家"""
    # 从宝可梦池中随机选择
    choices = random.sample(all_poke.pokemons, num_choices)
    print("请选择宝可梦 (输入对应编号):")
    for i, (_, pokemon_base) in enumerate(choices):  # 解包 tuple
        print(f"{i + 1}. {pokemon_base.name} (属性: {pokemon_base.attribute})")


    # 获取玩家选择
    selected_ids = input("输入编号 (多个编号以逗号分隔): ").split(",")
    selected_pokemons = []
    for selected_id in selected_ids:
        try:
            idx = int(selected_id.strip()) - 1
            if 0 <= idx < len(choices):
                poke_id, pokemon_base = choices[idx]
                selected_pokemons.append(all_poke.playerpoke(pokemon_base, level=5))
            else:
                print(f"编号 {selected_id} 无效。")
        except ValueError:
            print(f"无效输入: {selected_id}")

    # 将选择的宝可梦添加到玩家
    for pokemon in selected_pokemons:
        player.add_pokemon(pokemon)

# player.py 的修改部分
class Player:
    def __init__(self, name, player_file="playerpoke.json", tools_file="playertools.json"):
        self.name = name
        self.player_file = player_file
        self.tools_file = tools_file
        self.pokemon_slots = self.load_pokemon_slots()
        self.tools = self.load_tools()  # 新增道具栏

    def load_pokemon_slots(self):
        """加载玩家的宝可梦槽位数据"""
        try:
            with open(self.player_file, 'r', encoding='utf-8') as file:
                players_data = json.load(file)
                return players_data.get(self.name, {f"slot{i + 1}": {} for i in range(6)})
        except FileNotFoundError:
            return {f"slot{i + 1}": {} for i in range(6)}

    def save_pokemon_slots(self):
        """将玩家的宝可梦槽位数据保存到文件"""
        try:
            with open(self.player_file, 'r+', encoding='utf-8') as file:
                players_data = json.load(file)
        except FileNotFoundError:
            players_data = {}

        players_data[self.name] = self.pokemon_slots

        with open(self.player_file, 'w', encoding='utf-8') as file:
            json.dump(players_data, file, ensure_ascii=False, indent=4)

    def add_pokemon(self, pokemon_instance):
        """添加一个宝可梦到玩家槽位"""
        for slot, content in self.pokemon_slots.items():
            if not content:
                self.pokemon_slots[slot] = {
                    "name": pokemon_instance.name,
                    "attribute": pokemon_instance.attribute,
                    "attributes": pokemon_instance.attributes,
                    "level": pokemon_instance.level,
                    "ATK": pokemon_instance.ATK,
                    "DEF": pokemon_instance.DEF,
                    "SPD": pokemon_instance.SPD,
                    "ACC": pokemon_instance.ACC,
                    "HP": pokemon_instance.HP,
                    "Hp": pokemon_instance.Hp,
                    "EXP": pokemon_instance.EXP,
                    "NeedEXP": pokemon_instance.NeedEXP,
                    # 需要修改 skills 的格式，增加 PP 和 Pp
                    "skills": [
                        {"name": skill, "PP": 20, "Pp": 20} for skill in pokemon_instance.skills
                    ],
                    "learn_skills": pokemon_instance.learn_skills
                }
                print(f"宝可梦 {pokemon_instance.name} 已成功添加到槽位 {slot}。")
                self.save_pokemon_slots()
                return
        print("槽位已满，请替换一个宝可梦。")
        self.replace_pokemon(pokemon_instance)

    def replace_pokemon(self, new_pokemon):
        """替换槽位中的宝可梦"""
        print("请选择要替换的宝可梦 (输入编号):")
        for idx, (slot, content) in enumerate(self.pokemon_slots.items()):
            if content:
                print(f"{idx + 1}. {content['name']} 等级: {content['level']}")

        try:
            index = int(input("输入编号: ").strip()) - 1
            if 0 <= index < 6:
                slot_key = f"slot{index + 1}"
                replaced_pokemon = self.pokemon_slots[slot_key]
                self.pokemon_slots[slot_key] = {
                    "name": new_pokemon.name,
                    "attribute": new_pokemon.attribute,
                    "attributes": new_pokemon.attributes,
                    "level": new_pokemon.level,
                    "ATK": new_pokemon.ATK,
                    "DEF": new_pokemon.DEF,
                    "SPD": new_pokemon.SPD,
                    "ACC": new_pokemon.ACC,
                    "HP": new_pokemon.HP,
                    "Hp": new_pokemon.Hp,
                    "EXP": new_pokemon.EXP,
                    "NeedEXP": new_pokemon.NeedEXP,
                    # 需要修改 skills 的格式，增加 PP 和 Pp
                    "skills": [
                        {"name": skill, "PP": 20, "Pp": 20} for skill in new_pokemon.skills
                    ],
                    "learn_skills": new_pokemon.learn_skills
                }
                print(f"{replaced_pokemon['name']} 被替换为 {new_pokemon.name}。")
                self.save_pokemon_slots()
            else:
                print("无效的编号。")
        except ValueError:
            print("请输入有效的数字编号。")

    def list_pokemons(self):
        """列出玩家的所有宝可梦"""
        print(f"玩家 {self.name} 的宝可梦：")
        for slot, content in self.pokemon_slots.items():
            if content:
                print(f"{slot}: {content['name']} 等级: {content['level']} 属性: {content['attribute']}")
            else:
                print(f"{slot}: 空槽位")

    def release_pokemon(self, slot):
        """放生指定槽位的宝可梦"""
        if slot in self.pokemon_slots and self.pokemon_slots[slot]:
            released_pokemon = self.pokemon_slots[slot]
            self.pokemon_slots[slot] = {}
            print(f"{released_pokemon['name']} 已被放生。")
            self.save_pokemon_slots()
        else:
            print("无效的槽位或槽位为空。")

    def load_tools(self):
        """加载玩家的道具数据"""
        try:
            with open(self.tools_file, 'r', encoding='utf-8') as file:
                tools_data = json.load(file)
                return tools_data.get(self.name, {})
        except FileNotFoundError:
            return {}

    def save_tools(self):
        """保存玩家的道具数据"""
        try:
            with open(self.tools_file, 'r+', encoding='utf-8') as file:
                tools_data = json.load(file)
        except FileNotFoundError:
            tools_data = {}

        tools_data[self.name] = self.tools
        with open(self.tools_file, 'w', encoding='utf-8') as file:
            json.dump(tools_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def login(player_name, player_file="playerpoke.json", tools_file="playertools.json"):
        """登录或注册玩家"""
        try:
            with open(player_file, 'r', encoding='utf-8') as file:
                players_data = json.load(file)
        except FileNotFoundError:
            players_data = {}

        try:
            with open(tools_file, 'r', encoding='utf-8') as file:
                tools_data = json.load(file)
        except FileNotFoundError:
            tools_data = {}

        if player_name not in players_data:
            print(f"玩家 {player_name} 不存在，正在创建新玩家...")
            players_data[player_name] = {f"slot{i+1}": {} for i in range(6)}
            
            # 初始化新玩家的道具
            # 在 Player.login 方法中修改初始道具部分
            tools_data[player_name] = {
                "伤药": {
                    "name": "伤药",
                    "num": 3,
                    "ToolsType": 2,
                    "GetType": 1,
                    "BloodType": 1,
                    "LifeType": 0,
                    "PpType": 0
                },
                "活力碎片": {
                    "name": "活力碎片",
                    "num": 1,
                    "ToolsType": 16,
                    "GetType": 0,
                    "BloodType": 0,
                    "LifeType": 1,
                    "PpType": 0
                },
                "Pp小补剂": {
                    "name": "Pp小补剂",
                    "num": 2,
                    "ToolsType": 32,
                    "GetType": 0,
                    "BloodType": 0,
                    "LifeType": 0,
                    "PpType": 1
                },
                "精灵球": {
                    "name": "精灵球",
                    "num": 5,
                    "ToolsType": 1,
                    "GetType": 1,
                    "BloodType": 0,
                    "LifeType": 0,
                    "PpType": 0
                }
            }
            
            # 保存数据
            with open(player_file, 'w', encoding='utf-8') as file:
                json.dump(players_data, file, ensure_ascii=False, indent=4)
            with open(tools_file, 'w', encoding='utf-8') as file:
                json.dump(tools_data, file, ensure_ascii=False, indent=4)

            player = Player(player_name)
            print("选择一只宝可梦进入冒险吧！")
            choose_pokemons(player)
        else:
            print("欢迎登录宝可梦")
        return Player(player_name, player_file, tools_file)
