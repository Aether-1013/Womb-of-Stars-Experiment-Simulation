import random
import time
from enum import Enum
from typing import List, Dict, Optional, Tuple

# 路径枚举类：定义电信号的不同发展路径
class Path(Enum):
    NEGATIVE_WORLD = "负世"
    TIME = "岁月"
    TRICKERY = "诡计"
    DEATH = "死亡"
    REASON = "理性"
    # 其他路径可以根据需要添加

# 原动力枚举类：定义电信号的行为动机
class Motivation(Enum):
    HATRED = "憎恨"
    DESIRE = "渴望"
    PEACE = "平和"
    CRITICISM = "批判"
    # 其他原动力可以根据需要添加

# 实验阶段枚举类：定义实验的不同阶段
class ExperimentStage(Enum):
    INORGANIC = "无机"
    ORGANIC = "有机"
    HUMAN = "人类"
    REGENESIS = "再创世"
    ETERNAL_RECURRENCE = "永劫轮回"

# 电信号类：实验中的基本单位
class ElectricalSignal:
    def __init__(self, signal_id: str, path: Path, motivation: Motivation):
        self.signal_id = signal_id  # 电信号ID
        self.path = path  # 电信号路径
        self.motivation = motivation  # 电信号原动力
        self.is_locked = False  # 是否被锁定
        self.is_merged = False  # 是否已合并
        self.memory = []  # 电信号记忆
        self.golden_blood = False  # 毁灭特征
        self.black_tide_infected = False  # 黑潮感染

    def __str__(self) -> str:
        """返回电信号的字符串表示"""
        status = "锁定" if self.is_locked else "运行中"
        merged = "已合并" if self.is_merged else "未合并"
        golden_blood = "有" if self.golden_blood else "无"
        infected = "已感染" if self.black_tide_infected else "未感染"
        return f"{self.signal_id} - 路径: {self.path.value}, 原动力: {self.motivation.value}, 状态: {status}, {merged}, 金血: {golden_blood}, 黑潮: {infected}"

    def inherit_memory(self, other: 'ElectricalSignal') -> None:
        """继承另一个电信号的记忆
        
        Args:
            other: 被继承记忆的电信号对象
        """
        self.memory.extend(other.memory)
        print(f"{self.signal_id} 继承了 {other.signal_id} 的记忆")

    def mutate(self) -> None:
        """电信号变异：随机改变电信号的属性
        
        可能的变异包括：路径变化、获得金血特征、感染黑潮
        """
        # 随机发生变异
        if random.random() < 0.1:
            # 可能的变异：路径变化
            new_path = random.choice(list(Path))
            print(f"{self.signal_id} 发生变异: 路径从 {self.path.value} 变为 {new_path.value}")
            self.path = new_path
        elif random.random() < 0.2:
            # 可能的变异：获得金血
            if not self.golden_blood:
                self.golden_blood = True
                print(f"{self.signal_id} 获得了金血特征")
        elif random.random() < 0.3:
            # 可能的变异：感染黑潮
            if not self.black_tide_infected:
                self.black_tide_infected = True
                print(f"{self.signal_id} 被黑潮感染")

    def make_decision(self, context: Dict) -> str:
        """基于原动力做出决策
        
        Args:
            context: 决策上下文，包含当前实验阶段和循环次数
        
        Returns:
            str: 决策描述
        """
        if self.motivation == Motivation.HATRED:
            # 憎恨：破坏性决策
            return f"{self.signal_id} 因憎恨做出破坏性行动"
        elif self.motivation == Motivation.DESIRE:
            # 渴望：利己决策
            return f"{self.signal_id} 因渴望做出利己行动"
        elif self.motivation == Motivation.PEACE:
            # 平和：最小扰动决策
            return f"{self.signal_id} 因平和做出最小扰动行动"
        elif self.motivation == Motivation.CRITICISM:
            # 批判：求解决策
            return f"{self.signal_id} 因批判做出求解行动"
        else:
            return f"{self.signal_id} 做出普通行动"

# 翁法罗斯实验类：管理整个实验过程
class WombOfStars:
    def __init__(self):
        self.stage = ExperimentStage.INORGANIC  # 当前实验阶段
        self.cycles = 0  # 实验循环次数
        self.signals: List[ElectricalSignal] = []  # 电信号列表
        self.locked_signals: List[ElectricalSignal] = []  # 锁定的电信号列表
        self.golden_blood_count = 0  # 金血电信号计数
        self.black_tide_infected_count = 0  # 黑潮感染电信号计数
        self.eternal_recurrence_count = 0  # 永劫轮回计数
        self.pioneer_intervened = False  # 开拓者是否介入

    def initialize(self) -> None:
        """初始化实验
        
        打印实验初始化信息，创建初始电信号，并显示初始状态
        """
        print("=== 翁法罗斯实验初始化 ===")
        # 创建初始电信号
        self._create_initial_signals()
        print(f"初始阶段: {self.stage.value}")
        print(f"初始电信号数量: {len(self.signals)}")

    def _create_initial_signals(self) -> None:
        """创建初始电信号
        
        基于参考文档中的电信号创建示例电信号，包括不同路径和原动力
        """
        # 基于参考文档中的电信号创建一些示例
        self.signals.append(ElectricalSignal("NeiKos496", Path.NEGATIVE_WORLD, Motivation.HATRED))
        self.signals.append(ElectricalSignal("PhiLia093", Path.TIME, Motivation.HATRED))  # 原动力被屏蔽，这里暂时使用HATRED
        self.signals.append(ElectricalSignal("OreXis945", Path.TRICKERY, Motivation.DESIRE))
        self.signals.append(ElectricalSignal("EpieiKeia216", Path.DEATH, Motivation.PEACE))
        self.signals.append(ElectricalSignal("SkeMma720", Path.REASON, Motivation.CRITICISM))

    def run_cycle(self) -> bool:
        """运行一个实验循环
        
        执行一个完整的实验循环，包括阶段检查、电信号行动、变异等
        
        Returns:
            bool: 如果实验应继续运行则返回True，否则返回False
        """
        self.cycles += 1
        print(f"\n=== 循环 {self.cycles} - 阶段: {self.stage.value} ===")

        # 检查是否需要转换阶段
        self._check_stage_transition()

        # 电信号行动
        self._signals_action()

        # 电信号变异
        self._mutate_signals()

        # 检查永劫轮回状态
        if self.stage == ExperimentStage.ETERNAL_RECURRENCE:
            self.eternal_recurrence_count += 1
            print(f"永劫轮回计数: {self.eternal_recurrence_count}")
            # 检查是否突破永劫轮回
            if self.pioneer_intervened and random.random() < 0.05:
                print("外部变量介入，突破永劫轮回!")
                self.stage = ExperimentStage.REGENESIS
                return True

        # 检查实验是否结束
        if self.cycles >= 10000 or (self.stage == ExperimentStage.REGENESIS and self.eternal_recurrence_count > 0):
            print("实验结束")
            return False

        return True

    def _check_stage_transition(self) -> None:
        """检查是否需要转换实验阶段
        
        根据当前循环次数和阶段，决定是否转换到下一个实验阶段
        """
        if self.stage == ExperimentStage.INORGANIC and self.cycles >= 500:
            self.stage = ExperimentStage.ORGANIC
            print("转换至有机生命阶段")
        elif self.stage == ExperimentStage.ORGANIC and self.cycles >= 1500:
            self.stage = ExperimentStage.HUMAN
            print("转换至人类阶段")
        elif self.stage == ExperimentStage.HUMAN and self.cycles >= 3000:
            self.stage = ExperimentStage.REGENESIS
            print("转换至再创世阶段")
            # 锁定部分电信号
            for signal in random.sample(self.signals, min(3, len(self.signals))):
                signal.is_locked = True
                self.locked_signals.append(signal)
                print(f"电信号 {signal.signal_id} 被锁定")
        elif self.stage == ExperimentStage.REGENESIS and random.random() < 0.1:
            # 随机进入永劫轮回
            self.stage = ExperimentStage.ETERNAL_RECURRENCE
            print("进入永劫轮回阶段")
            # NeiKos496通常会在永劫轮回中起关键作用
            neikos = next((s for s in self.signals if s.signal_id == "NeiKos496"), None)
            if neikos:
                neikos.is_locked = True
                self.locked_signals.append(neikos)
                print(f"电信号 {neikos.signal_id} 在永劫轮回中被锁定")

    def _signals_action(self) -> None:
        """电信号行动模拟
        
        模拟所有电信号的行动，包括决策和互动
        """
        context = {"stage": self.stage.value, "cycles": self.cycles}
        for signal in self.signals:
            if not signal.is_merged:
                action = signal.make_decision(context)
                print(action)
                # 记录记忆
                signal.memory.append(f"循环 {self.cycles}: {action}")

        # 处理电信号之间的互动
        if len(self.signals) > 1 and random.random() < 0.3:
            signal1, signal2 = random.sample(self.signals, 2)
            if not signal1.is_merged and not signal2.is_merged:
                # 随机事件：电信号合并
                if random.random() < 0.1:
                    print(f"{signal1.signal_id} 与 {signal2.signal_id} 合并")
                    signal2.is_merged = True
                    signal1.inherit_memory(signal2)
                # 随机事件：电信号竞争
                elif random.random() < 0.2:
                    print(f"{signal1.signal_id} 与 {signal2.signal_id} 发生竞争")
                    # 胜者获得败者的部分记忆
                    winner = signal1 if random.random() < 0.5 else signal2
                    loser = signal2 if winner == signal1 else signal1
                    winner.inherit_memory(loser)

    def _mutate_signals(self) -> None:
        """电信号变异处理
        
        对所有未合并且未锁定的电信号应用变异机制，并更新金血和黑潮感染数量
        """
        for signal in self.signals:
            if not signal.is_merged and not signal.is_locked:
                signal.mutate()

        # 统计金血和黑潮感染数量
        self.golden_blood_count = sum(1 for s in self.signals if s.golden_blood)
        self.black_tide_infected_count = sum(1 for s in self.signals if s.black_tide_infected)
        print(f"金血电信号数量: {self.golden_blood_count}")
        print(f"黑潮感染电信号数量: {self.black_tide_infected_count}")

    def introduce_pioneer(self) -> None:
        """引入开拓者变量
        
        开拓者介入实验，可能会接替空缺的路径，特别是岁月路径
        这会影响实验进程，增加突破永劫轮回的可能性
        """
        print("\n=== 外部变量 '开拓者' 介入 ===")
        self.pioneer_intervened = True
        # 开拓者可能会接替空缺的路径
        time_path_signal = next((s for s in self.signals if s.path == Path.TIME), None)
        if time_path_signal and time_path_signal.is_merged:
            # 创建新的电信号接替岁月路径
            new_signal = ElectricalSignal("Pioneer", Path.TIME, Motivation.PEACE)
            self.signals.append(new_signal)
            print(f"开拓者接替了岁月路径，创建新电信号 {new_signal.signal_id}")
        else:
            print("开拓者介入，影响实验进程")

    def print_status(self) -> None:
        """打印当前实验状态"""
        print("\n=== 实验状态 ===")
        print(f"阶段: {self.stage.value}")
        print(f"循环次数: {self.cycles}")
        print(f"电信号总数: {len(self.signals)}")
        print(f"锁定电信号: {len(self.locked_signals)}")
        print(f"合并电信号: {sum(1 for s in self.signals if s.is_merged)}")
        print(f"金血电信号: {self.golden_blood_count}")
        print(f"黑潮感染电信号: {self.black_tide_infected_count}")
        print(f"永劫轮回次数: {self.eternal_recurrence_count}")
        print(f"开拓者介入: {self.pioneer_intervened}")

        print("\n电信号列表:")
        for signal in self.signals:
            print(f"  {signal}")

# 运行实验
if __name__ == "__main__":
    experiment = WombOfStars()
    experiment.initialize()
    experiment.print_status()

    # 运行一些初始循环
    for _ in range(5):
        if not experiment.run_cycle():
            break
        time.sleep(0.5)  # 为了更好的观察效果

    # 引入开拓者
    experiment.introduce_pioneer()

    # 继续运行循环
    for _ in range(5):
        if not experiment.run_cycle():
            break
        time.sleep(0.5)  # 为了更好的观察效果

    # 打印最终状态
    experiment.print_status()

    print("\n实验完成。要继续运行更多循环，请修改代码中的循环次数。")