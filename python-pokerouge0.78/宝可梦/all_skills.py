#`import globals
import json
from enum  import IntEnum,unique
import random



try:
    @unique
    class ObjOfAction(IntEnum):
        #这里是执行对象的标志
        self=1,
        other=2,
        self_abl=4,
        abl=8,
        blood_atk=16
    class EffectType(IntEnum):
        all_blood = 1
        half_blood = 2
        half_half_blood = 4
except ValueError as e:
    print(e)

def load_skills():
    with open("skills.json", "r", encoding="utf-8") as file:
        skills_data = json.load(file)
    return skills_data[0]  # 获取第一个对象中的技能数据

def calc_hurt (poke_self,poke,skill):
    hurt = skill.hurt
    # （（攻击方等级×2÷5+2））×技能威力×攻击方攻击÷防守方能力值÷50+2）×（85～100）÷100
    hurt = ((poke_self.level * 2 / 5 + 2) * hurt * poke_self.ATK / poke.DEF / 50 + 2)
    if poke.attribute in poke_self.attributes  :
        hurt = 2 * hurt
    if poke.attribute in skill.attributes:
        hurt = 1.5 * hurt
    if poke.HP > 0:
        return hurt

def calc_blood (poke_self,skill):
    if skill.blood_type == 1:
        return -poke_self.HP
    elif skill.blood_type == 2:
        return -(poke_self.HP)/2
    elif skill.blood_type == 4 :
        return -(poke_self.HP)/4


def get_hurt (poke,hurt):
    if poke.Hp - hurt < 0:
        poke.Hp = 0
    else :
        poke.Hp =poke.Hp - hurt
    print(f"{poke.name} 受到了 {int(hurt)} 点伤害！")

def get_blood (poke,blood):
    if poke.Hp + blood > poke.HP:
        poke.Hp = poke.HP   #这里需要改：第一个poke.HP应该是真实HP，而第二个是最大HP
    else :
        poke.Hp = poke.Hp + blood #同上
    print(f"{poke.name} 受到了 {int(blood)} 点体力值！")
def ApplyDmage(poke,poke_other,damage,skill):
    damage = int(damage)
    if skill.skill_type == 2 :
        if damage ==0:
            print("似乎对{}没造成伤害".format(poke.name))
        elif damage < 0:
            return
    else :
        if damage >=0 :
            return
    if skill.blood_type == 0 :
        get_hurt(poke_other,damage)
    else :
        get_blood(poke,damage)

    #对poke的属性操作的结束阶段

# 查找技能的函数
def get_skill_by_name(skill_name,Pp):
    if skill_name in skills_data:
        skill_info = skills_data[skill_name]  # 获取技能的详细信息
        # 使用技能信息来创建 SkillBase 对象
        skill = SkillBase(
            name=skill_info["name"],
            hurt=skill_info["hurt"],
            ACC=skill_info["ACC"],
            PP=skill_info["PP"],
            Pp=Pp,
            attributes=skill_info["attributes"],
            attribute=skill_info["attribute"],
            skill_type=skill_info["skill_type"],
            blood_type=skill_info["blood_type"],
            effects=skill_info.get("effects", [])  # 如果没有 effects 则为空列表
        )
        return skill
    else:
        print(f"技能 {skill_name} 未找到!")
        return None


class SkillBase:
    def __init__(self, name, hurt, ACC, PP, Pp, attributes, attribute, skill_type, blood_type, cooldown=0, effects=None):
        self.name = name
        self.hurt = hurt
        self.ACC = ACC
        self.PP = PP  # 总PP
        self.Pp = Pp  # 剩余PP
        self.attributes = attributes
        self.attribute = attribute
        self.skill_type = skill_type
        self.blood_type = blood_type
        self.cooldown = cooldown
        self.effects = effects or []

    def has_pp(self):
        """检查是否有剩余 PP"""
        return self.Pp > 0

    def check_hit(self):
        """检查技能是否命中"""
        return random.randint(1, 100) <= self.ACC

    def apply(self, attacker, defender):
        """技能释放逻辑"""
        if not self.has_pp():
            print(f"{self.name} 的 PP 已用完！")
            return 0

        print(f"{attacker.name} 使用了 {self.name}！")

        if self.skill_type == 2:
            if not self.check_hit():
                print(f"{attacker.name} 的 {self.name} 未命中！")
                return 0
            damage = calc_hurt(attacker,defender,self)
        if self.skill_type == 1:
            damage = calc_blood(attacker,self)
        # 计算伤害
        # 使用技能后减少 PP
        self.Pp -= 1
        return int(damage)


skills_data = load_skills()

# 根据技能名字查找并实例化技能对象
def save_player_poke(player, filename='playerpoke.json'):
    """将玩家宝可梦实例数据保存到 playerpoke.json 文件"""
    try:
        with open(filename, 'r+', encoding='utf-8') as file:
            players_data = json.load(file)
    except FileNotFoundError:
        players_data = {}

    # 处理玩家数据
    if player.name not in players_data:
        players_data[player.name] = {}

    # 保存宝可梦信息
    for slot, content in player.pokemon_slots.items():
        if content:
            pokemon_data = {
                "name": content["name"],
                "attribute": content["attribute"],
                "attributes": content["attributes"],
                "level": content["level"],
                "ATK": content["ATK"],
                "DEF": content["DEF"],
                "SPD": content["SPD"],
                "ACC": content["ACC"],
                "HP": content["HP"],
                "Hp": content["Hp"],
                "EXP": content["EXP"],
                "NeedEXP": content["NeedEXP"],
                "skills": content["skills"],  # 存储技能
                "learn_skills": content["learn_skills"]
            }
            players_data[player.name][slot] = pokemon_data

    # 将数据写回文件
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(players_data, file, ensure_ascii=False, indent=4)

    print(f"玩家 {player.name} 的宝可梦数据已保存。")


skills = {}

with open('skills.json', 'r', encoding='utf-8') as skill_file:
    skill_data = json.load(skill_file)
    for skill_group in skill_data:  # 解析每个技能组
        for skill_name, skill_attributes in skill_group.items():
            skills[skill_name] = SkillBase(**skill_attributes)