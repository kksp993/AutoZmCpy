from enum import Enum
import traceback
from ZmxyOL import *
from AutoScriptor import *
from logzero import logger
class FFT_difficulty(Enum):
    past = "过去"
    now = "现在"

class FFT_preference(Enum):
    yellow = "烦恼"
    purple = "恶意"
    red = "恶语"


def battle():
    wait_for_disappear(I("加载中"))
    from ZmxyOL.battle.character.hero import h
    sleep(0.5)
    h.skill(4, 0.95) # 使用4技能， 按住0.95秒
    h.zhenling()    # 使用真灵合体
    h.huashen()     # 使用化身
    h.prop()        # 使用剑阵葫芦
    h.zhenwu()  # 使用真武使用真武
    h.sleep(0.5)
    h.skill(6)
    bg.add(
        name="FTT_battle",
        identifier=(T("确认"),T("前往新一层")),
        callback=lambda: [bg.set_signal("try_exit", True),bg.clear()]
    )
    cnt = 1
    bg.set_signal("try_exit", False)
    while not bg.signal("try_exit"):
        h.prop()
        if cnt % 2 == 0: h.skill(6)
        else: h.skill(5,4)
        cnt += 1
    click((T("确认"),T("前往新一层")))
    wait_for_disappear(I("加载中"))

def FTT_battle_one_round(preference:list[FFT_preference]):
    if first(get_colors(B(94,623,2,3)))!="灰色": return logger.info("可以挑战天魔，跳过轮回轮次")
    final = False
    preference_list = [T(p.value) for p in preference]
    preference_list.append(T("终劫"))
    preference_list = tuple(preference_list)
    while not final:
        final = ui_T(T("终劫"))
        if final: logger.info(f"本关是终劫，final={final}")
        while ui_F(preference_list):
            click(T("更替"))
            sleep(0.5)
            click(T("确定"))
            sleep(2)
        click(preference_list)
        click(T("入劫"))
        battle()
        wait_for_appear(T("入劫"))

def FTT_TianMo():
    while ui_F(T("天魔禁忌",box=Box(732,342,77,27))):
        click(B(94,623,2,3))
    sleep(0.5)
    click(I("梵天塔-天魔挑战"))
    battle()
    wait_for_appear(T("入劫"))

# @register_task
def fanTianTa(battle_times=50, difficulty=FFT_difficulty.past, preference=(FFT_preference.purple,FFT_preference.yellow)):
    ensure_in("极北",-1)
    click(B(0,120,90,100))
    sleep(3)
    click(T(difficulty.value),offset=(0,100))
    sleep(3)
    click(T("确认"), if_exist=True)
    sleep(5)
    for _ in range(battle_times):
        FTT_battle_one_round(preference)
        sleep(3)
        FTT_TianMo()
        sleep(3)
    click(B(30,30,30,30))
    sleep(1)
    click(B(30,30,30,30))


# 登录游戏后，在主界面直接运行就行

if __name__ == "__main__":
    try:
        # fanTianTa()
        print(locate(T("进入游戏")))
    except Exception as e:
        traceback.print_exc()
    finally:
        bg.stop()
        exit(0)