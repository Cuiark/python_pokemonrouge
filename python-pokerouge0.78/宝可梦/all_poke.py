import globals
#import all_skills as ski
import json
import random
import json

def get_pokemon_stats_by_name(name, file_path='poketmp.json'):
    try:
        # 读取 poketmp.json 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历 poketmp 数据查找对应名字的宝可梦
        for poke_data in data:
            for poke_id, attributes in poke_data.items():
                if attributes['name'] == name:
                    # 找到匹配的宝可梦，返回其属性
                    return attributes["atk"],attributes["Def"],attributes["spd"],attributes["hp"],attributes["exp"]

        # 如果未找到该宝可梦
        return f"没有找到名字为 {name} 的宝可梦。"

    except FileNotFoundError:
        return "poketmp.json 文件未找到！"
    except json.JSONDecodeError:
        return "文件内容解析错误！"
class poke_base:
    def __init__(self, name, attribute, attributes, ATK, DEF, SPD, ACC, HP, Hp, EXP, atk, Def, spd, hp, NeedEXP, exp, learn_skills, skills=[]):
        self.name = name
        self.attribute = attribute
        self.attributes = attributes
        self.ATK = ATK
        self.DEF = DEF
        self.SPD = SPD
        self.ACC = ACC
        self.HP = HP
        self.Hp = Hp
        self.EXP = EXP
        self.atk = atk
        self.Def = Def
        self.spd = spd
        self.hp = hp
        self.NeedEXP = NeedEXP
        self.exp = exp
        self.skills = skills  # 只存储技能名称和PP
        self.learn_skills = learn_skills or {}

    def create_instance(self, level=1):
        return playerpoke(self, level)

    def IsAlive(self):
        return self.Hp > 0

    def to_dict(self):
        # 只保存技能名称和剩余PP
        for skill in self.skills:
            print(skill)
        return {
            "name": self.name,
            "attribute": self.attribute,
            "attributes": self.attributes,
            "level": self.level,
            "ATK": self.ATK,
            "DEF": self.DEF,
            "SPD": self.SPD,
            "ACC": self.ACC,
            "HP": self.HP,
            "Hp": self.Hp,
            "EXP": self.EXP,
            "NeedEXP": self.NeedEXP,
            "skills": [{"name": skill['name'], "PP":skill['PP'] ,"Pp": skill['Pp']} for skill in self.skills],
            "learn_skills": self.learn_skills,
        }
class playerpoke:
    def __init__(self, temp, level=5):
        self.temp = temp
        self.name = temp.name
        self.attribute = temp.attribute
        self.attributes = temp.attributes
        self.level = level
        self.ATK = temp.ATK + temp.atk * level
        self.DEF = temp.DEF + temp.Def * level
        self.SPD = temp.SPD + temp.spd * level
        self.ACC = temp.ACC
        self.HP = temp.HP + temp.hp * level
        self.Hp = temp.Hp + temp.hp * level
        self.EXP = temp.EXP
        self.skills = temp.skills
        self.learn_skills = temp.learn_skills
        self.NeedEXP = temp.NeedEXP + temp.exp * level * level
        self.get_skill()

    def exp_up(self, exp):
        """经验值提升方法"""
        self.EXP = self.EXP + exp
        print(f"当前经验值: {self.EXP}/{self.NeedEXP}")  # 添加经验值提示
        
        while self.EXP >= self.NeedEXP:
            self.EXP = self.EXP - self.NeedEXP
            self.level = self.level + 1
            self.ATK = self.ATK + self.atk
            self.DEF = self.DEF + self.Def
            self.SPD = self.SPD + self.spd
            self.HP = self.HP + self.hp
            self.Hp = self.Hp + self.hp
            self.NeedEXP = self.NeedEXP + self.exp * self.level * self.level
            print(f"{self.name} 升级了! 当前等级: {self.level}")  # 添加升级提示
            self.get_skill()

    def get_skill(self):
        for skill in self.learn_skills:
            if skill["level"] <= self.level:
                if len(self.skills) < 4:
                    self.skills.append(skill["name"])
                else:
                    self.change_skills(skill["name"])

    def change_skills(self, name):
        a = input("是否遗忘一个技能[y/n]:")
        if a == "n":
            return
        else:
            pop_name = input("选择要遗忘的技能" + str(self.skills))
            print("....{}遗忘了{}".format(self.name, pop_name))
            self.skills.pop(self.skills.index(pop_name))
            print("....{}学会了{}".format(self.name, name))
            self.skills.append(name)

    def to_dict(self):
        return {
            "name": self.name,
            "attribute": self.attribute,
            "attributes": self.attributes,
            "level": self.level,
            "ATK": self.ATK,
            "DEF": self.DEF,
            "SPD": self.SPD,
            "HP": self.HP,
            "skills": self.skills,
            "learn_skills": self.learn_skills,
        }
class wildpoke:
    def __init__(self, temp, level=1):
        self.temp = temp
        self.name = temp.name
        self.attribute = temp.attribute
        self.attributes = temp.attributes
        self.level = level
        self.ATK = temp.ATK + temp.atk * level
        self.DEF = temp.DEF + temp.Def * level
        self.SPD = temp.SPD + temp.spd * level
        self.ACC = temp.ACC
        self.HP = temp.HP + temp.hp * level
        self.Hp = temp.Hp + temp.hp * level
        self.EXP = temp.EXP
        self.learn_skills = temp.learn_skills
        self.skills = self.get_random_skills(temp.learn_skills)
        self.NeedEXP = temp.NeedEXP + temp.exp * level * level

    def get_random_skills(self, learn_skills):
        """
        从 learn_skills 随机选择最多 4 个技能作为初始技能。
        """
        available_skills = [skill['name'] for skill in learn_skills if skill['level'] <= self.level]
        selected_skills = random.sample(available_skills, min(len(available_skills), 4))
        return [{"name": skill, "PP": 20, "Pp": 20} for skill in selected_skills]

    def IsAlive(self):
        return self.Hp > 0

    def to_dict(self):
        return {
            "name": self.name,
            "attribute": self.attribute,
            "level": self.level,
            "ATK": self.ATK,
            "DEF": self.DEF,
            "SPD": self.SPD,
            "HP": self.HP,
            "skills": self.skills,
        }


#name,attribute,attributes,ATK,DEF,SPD,ACC,HP,Hp,EXP,atk,Def,spd,hp,NeedEXP,exp,learn_skills,skills=[]
class PlayerPoke(poke_base):
    def __init__(self, filepoke):
        a,b,c,d,e = get_pokemon_stats_by_name(filepoke["name"])
        super().__init__(
            name=filepoke["name"],
            attribute=filepoke["attribute"],
            attributes=filepoke["attributes"],
            ATK=filepoke["ATK"],
            DEF=filepoke["DEF"],
            SPD=filepoke["SPD"],
            ACC=filepoke["ACC"],
            HP=filepoke["HP"],
            Hp=filepoke["Hp"],
            EXP=filepoke["EXP"],
            NeedEXP=filepoke["NeedEXP"],
            learn_skills=filepoke["learn_skills"],
            skills=filepoke["skills"],
            atk=a,
            Def=b,
            spd=c,
            hp=d,
            exp=e
        )
        self.level = filepoke["level"]
        self.temp = self  # 保存自身引用用于经验计算

    def exp_up(self, exp):
        """经验值提升方法"""
        self.EXP = self.EXP + exp
        while self.EXP >= self.NeedEXP:
            self.EXP -= self.NeedEXP
            self.level = self.level + 1
            self.ATK = self.ATK + self.atk
            self.DEF = self.DEF + self.Def
            self.SPD = self.SPD + self.spd
            self.HP = self.HP + self.hp
            self.Hp = self.Hp + self.hp
            self.NeedEXP = self.NeedEXP + self.exp * self.level * self.level
            self.get_skill()

    def get_skill(self):
        """获取技能方法"""
        for skill in self.learn_skills:
            if skill["level"] <= self.level:
                if len(self.skills) < 4:
                    self.skills.append({"name": skill["name"], "PP": 20, "Pp": 20})
                else:
                    self.change_skills(skill["name"])

    def change_skills(self, new_skill_name):
        """更换技能方法"""
        a = input("是否遗忘一个技能[y/n]:")
        if a == "n":
            return
        else:
            print("当前技能:", [skill["name"] for skill in self.skills])
            pop_name = input("选择要遗忘的技能名称: ")
            for i, skill in enumerate(self.skills):
                if skill["name"] == pop_name:
                    print(f"....{self.name}遗忘了{pop_name}")
                    self.skills.pop(i)
                    print(f"....{self.name}学会了{new_skill_name}")
                    self.skills.append({"name": new_skill_name, "PP": 20, "Pp": 20})
                    return
            print("未找到指定技能!")

    def IsAlive(self):
        """检查是否存活"""
        return self.Hp > 0

    def to_save_dict(self):
        """返回用于保存的数据字典"""
        return {
            "name": self.name,
            "attribute": self.attribute,
            "attributes": self.attributes,
            "level": self.level,
            "ATK": self.ATK,
            "DEF": self.DEF,
            "SPD": self.SPD,
            "HP": self.HP,
            "Hp": self.Hp,
            "EXP": self.EXP,
            "NeedEXP": self.NeedEXP,
            "skills": self.skills,
            "learn_skills": self.learn_skills,
            "ACC": self.ACC
        }
pokemons = []

with open('poketmp.json','r+',encoding="utf-8") as temp:
    data = json.loads(temp.read())
    for poke_id, attributes in data[0].items():
        pokemon = poke_base(**attributes)
        pokemons.append((poke_id, pokemon))

def to_dict(self):
    """将宝可梦实例转换为字典格式"""
    return {
        "name": self.name,
        "attribute": self.attribute,
        "attributes": self.attributes,
        "level": self.level,
        "ATK": self.ATK,
        "DEF": self.DEF,
        "SPD": self.SPD,
        "HP": self.HP,
        "Hp": self.Hp,
        "EXP": self.EXP,
        "NeedEXP": self.NeedEXP,
        "skills": self.skills,
        "learn_skills": self.learn_skills,
        "ACC": self.ACC,
        "atk": self.atk,
        "Def": self.Def,
        "spd": self.spd,
        "hp": self.hp
    }