# all_tools.py
from enum import IntEnum, unique
import json

try:
    @unique
    class ToolsType(IntEnum):
        #道具类型
        get_poke = 1
        get_blood = 2
        get_abl = 4
        get_level = 8
        get_life = 16
        get_Pp = 32

    class GetType(IntEnum):
        Get1 = 1 #系数为 1
        Get2 = 2 #系数为 1.5
        Get3 = 3 #系数为3
        Get4 = 4 #系数为4

    class BloodType(IntEnum):
        Blood1 = 1 #20HP
        Blood2 = 2 #60HP
        Blood3 = 4 #120HP
        all_Blood = 8 #全部HP

    class LifeType(IntEnum):
        life = 1 #复活，获得50%Hp
        life_all = 2 #复活，获得全部Hp

    class PpType(IntEnum):
        Pp1 = 1 #恢复10Pp
        Pp2 = 2 #恢复20Pp
        Pp3 = 4 #恢复全部Pp
except ValueError as e:
    print(e)

def get_tool_by_name(tool_name, num):
    """根据道具名称获取道具实例"""
    if tool_name in tool:  # 使用全局的tool字典
        tool_instance = tool[tool_name]
        new_tool = tools(
            name=tool_instance.name,
            num=num,
            ToolsType=tool_instance.ToolsType,
            GetType=tool_instance.GetType,
            BloodType=tool_instance.BloodType,
            LifeType=tool_instance.LifeType,
            PpType=tool_instance.PpType
        )
        return new_tool
    return None

def check_tool_type(tool, type_flag):
    """检查道具是否具有特定类型"""
    return bool(tool.ToolsType & type_flag)

class tools:
    def __init__(self, name, num, ToolsType, GetType=None, BloodType=None, LifeType=None, PpType=None):
        self.name = name
        self.num = num
        self.ToolsType = ToolsType
        self.GetType = GetType
        self.BloodType = BloodType
        self.LifeType = LifeType
        self.PpType = PpType

    def UseTools(self, poke):
        if self.ToolsType == ToolsType.get_poke:
            # 计算捕获概率
            catch_rate = self._calculate_catch_rate(poke)
            if self.GetType == GetType.Get1:
                catch_rate *= 1
            elif self.GetType == GetType.Get2:
                catch_rate *= 1.5
            elif self.GetType == GetType.Get3:
                catch_rate *= 3
            elif self.GetType == GetType.Get4:
                catch_rate *= 4
            # 返回捕获率供捕捉函数使用
            return catch_rate

        elif self.ToolsType == ToolsType.get_blood:
            if not poke.IsAlive():
                print(f"{poke.name} 已经失去战斗能力,不能使用回复药!")
                return False
                
            heal_amount = 0
            if self.BloodType == BloodType.Blood1:
                heal_amount = 20
            elif self.BloodType == BloodType.Blood2:
                heal_amount = 60
            elif self.BloodType == BloodType.Blood3:
                heal_amount = 120
            elif self.BloodType == BloodType.all_Blood:
                heal_amount = poke.HP - poke.Hp

            old_hp = poke.Hp
            poke.Hp = min(poke.Hp + heal_amount, poke.HP)
            actual_heal = poke.Hp - old_hp
            print(f"{poke.name} 恢复了 {actual_heal} 点HP!")
            return True

        elif self.ToolsType == ToolsType.get_life:
            if poke.IsAlive():
                print(f"{poke.name} 还活着,不需要使用复活药!")
                return False
                
            if self.LifeType == LifeType.life:
                poke.Hp = poke.HP // 2
            elif self.LifeType == LifeType.life_all:
                poke.Hp = poke.HP
            print(f"{poke.name} 复活了,当前HP: {poke.Hp}/{poke.HP}")
            return True

        elif self.ToolsType == ToolsType.get_abl:
            boost = 1.0
            if self.GetType == GetType.Get1:
                boost = 1.1
            elif self.GetType == GetType.Get2:
                boost = 1.2
            elif self.GetType == GetType.Get3:
                boost = 1.5

            poke.ATK = int(poke.ATK * boost)
            poke.DEF = int(poke.DEF * boost)
            poke.SPD = int(poke.SPD * boost)
            print(f"{poke.name} 的能力得到了提升!")
            return True

        elif self.ToolsType == ToolsType.get_level:
            exp_gain = 0
            if self.GetType == GetType.Get1:
                exp_gain = poke.NeedEXP * 0.3
            elif self.GetType == GetType.Get2:
                exp_gain = poke.NeedEXP * 0.5
            elif self.GetType == GetType.Get3:
                exp_gain = poke.NeedEXP

            poke.exp_up(int(exp_gain))
            print(f"{poke.name} 获得了 {int(exp_gain)} 点经验值!")
            return True
        elif self.ToolsType == ToolsType.get_Pp:
            # 检查是否有需要恢复PP的技能
            need_pp_recovery = False
            for skill in poke.skills:
                if skill['Pp'] < skill['PP']:
                    need_pp_recovery = True
                    break
                    
            if not need_pp_recovery:
                print(f"{poke.name} 的所有技能PP都是满的!")
                return False
                
            # 根据道具类型恢复不同量的PP
            for skill in poke.skills:
                if self.PpType == PpType.Pp1:
                    skill['Pp'] = min(skill['PP'], skill['Pp'] + 10)
                elif self.PpType == PpType.Pp2:
                    skill['Pp'] = min(skill['PP'], skill['Pp'] + 20)
                elif self.PpType == PpType.Pp3:
                    skill['Pp'] = skill['PP']
            print(f"{poke.name} 的技能PP得到了恢复!")
            return True

        return False

    def _calculate_catch_rate(self, poke):
        """计算宝可梦的捕获率"""
        # 捕获率 = (最大HP×3-当前HP×2)÷(最大HP×3)×精灵捕获系数×精灵球系数×状态系数÷255
        base_rate = (poke.HP * 3 - poke.Hp * 2) / (poke.HP * 3)
        pokemon_factor = 1  # 可以根据宝可梦种类调整
        status_factor = 1  # 可以根据状态(睡眠等)调整
        return base_rate * pokemon_factor * status_factor / 255



tool = {}

with open('tools.json', 'r+', encoding="utf-8") as temp:
    data = json.loads(temp.read())
    for tool_id, attributes in data[0].items():
        attributes['ToolsType'] = ToolsType(attributes['ToolsType'])
        if attributes.get('GetType') not in [None, 0]:
            attributes['GetType'] = GetType(attributes['GetType'])
        else:
            attributes['GetType'] = None

        if attributes.get('BloodType') not in [None, 0]:
            attributes['BloodType'] = BloodType(attributes['BloodType'])
        else:
            attributes['BloodType'] = None

        if attributes.get('LifeType') not in [None, 0]:
            attributes['LifeType'] = LifeType(attributes['LifeType'])
        else:
            attributes['LifeType'] = None

        # 创建道具实例
        tool[tool_id] = tools(**attributes)