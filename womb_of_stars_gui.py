import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from womb_of_stars import WombOfStars, ExperimentStage
import sys
from io import StringIO

# 翁法罗斯实验GUI类：负责实验的可视化界面和用户交互
class WombOfStarsGUI:
    def __init__(self, root):
        self.root = root  # 主窗口
        self.root.title("翁法罗斯实验模拟")  # 窗口标题
        self.root.geometry("1100x700")  # 窗口初始大小
        self.root.resizable(True, True)  # 允许调整窗口大小

        # 创建实验实例
        self.experiment = WombOfStars()  # 实验核心逻辑实例
        self.running = False  # 实验运行状态
        self.paused = False  # 实验暂停状态
        self.log_buffer = StringIO()  # 日志缓冲区
        self.original_stdout = sys.stdout  # 保存原始标准输出

        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding=10)  # 主框架
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # 填充整个窗口并允许扩展

        # 创建顶部控制区域
        self.control_frame = ttk.LabelFrame(self.main_frame, text="实验控制", padding=10)  # 控制区域框架
        self.control_frame.pack(fill=tk.X, pady=(0, 10))  # 水平填充，上下边距

        # 控制按钮
        self.start_button = ttk.Button(self.control_frame, text="开始实验", command=self.start_experiment)  # 开始按钮
        self.start_button.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        self.pause_button = ttk.Button(self.control_frame, text="暂停", command=self.pause_experiment, state=tk.DISABLED)  # 暂停按钮
        self.pause_button.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        self.reset_button = ttk.Button(self.control_frame, text="重置实验", command=self.reset_experiment)  # 重置按钮
        self.reset_button.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        self.pioneer_button = ttk.Button(self.control_frame, text="引入开拓者", command=self.introduce_pioneer, state=tk.DISABLED)  # 引入开拓者按钮
        self.pioneer_button.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        # 循环次数设置
        ttk.Label(self.control_frame, text="循环次数:").pack(side=tk.LEFT, padx=(20, 5))  # 标签
        self.cycles_var = tk.StringVar(value=str(sys.maxsize))  # 循环次数变量
        self.cycles_entry = ttk.Entry(self.control_frame, textvariable=self.cycles_var, width=15)  # 循环次数输入框
        self.cycles_entry.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        # 速度控制
        ttk.Label(self.control_frame, text="速度:").pack(side=tk.LEFT, padx=(20, 5))  # 标签
        self.speed_var = tk.DoubleVar(value=0.5)  # 速度变量
        self.speed_scale = ttk.Scale(self.control_frame, from_=0.1, to=1013.0, variable=self.speed_var, orient=tk.HORIZONTAL, length=100)  # 速度滑块
        self.speed_scale.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距
        self.speed_label = ttk.Label(self.control_frame, text=f"{self.speed_var.get():.1f}x", cursor="hand2")  # 速度显示标签
        self.speed_label.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距
        self.speed_label.bind("<Button-1>", self.focus_speed_entry)  # 点击标签聚焦到输入框
        self.speed_scale.bind("<Motion>", self.update_speed_label)  # 拖动滑块更新标签
        
        # 速度输入框
        ttk.Label(self.control_frame, text="速度值:").pack(side=tk.LEFT, padx=(20, 5))  # 标签
        self.speed_entry_var = tk.StringVar(value="0.5")  # 速度输入变量
        self.speed_entry = ttk.Entry(self.control_frame, textvariable=self.speed_entry_var, width=8)  # 速度输入框
        self.speed_entry.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距
        self.speed_entry.bind("<Return>", lambda event: self.apply_speed())  # 回车应用速度
        self.apply_speed_button = ttk.Button(self.control_frame, text="应用", command=self.apply_speed)  # 应用按钮
        self.apply_speed_button.pack(side=tk.LEFT, padx=5)  # 左对齐，水平间距

        # 创建中间状态区域
        self.status_frame = ttk.LabelFrame(self.main_frame, text="实验状态", padding=10)  # 状态区域框架
        self.status_frame.pack(fill=tk.X, pady=(0, 10))  # 水平填充，上下边距

        # 状态标签
        self.status_vars = {
            "阶段": tk.StringVar(value="未开始"),
            "循环次数": tk.StringVar(value="0"),
            "电信号总数": tk.StringVar(value="0"),
            "锁定电信号": tk.StringVar(value="0"),
            "合并电信号": tk.StringVar(value="0"),
            "金血电信号": tk.StringVar(value="0"),
            "黑潮感染": tk.StringVar(value="0"),
            "永劫轮回次数": tk.StringVar(value="0"),
            "开拓者介入": tk.StringVar(value="否")
        }  # 存储各种状态变量

        # 创建状态网格
        row = 0
        col = 0
        for key, var in self.status_vars.items():
            ttk.Label(self.status_frame, text=f"{key}:").grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=2)  # 状态标签
            ttk.Label(self.status_frame, textvariable=var, font=("Arial", 10, "bold")).grid(row=row, column=col*2+1, sticky=tk.W, padx=5, pady=2)  # 状态值（加粗显示）
            col += 1
            if col > 2:
                col = 0
                row += 1

        # 创建底部区域，分为左右两部分
        self.bottom_frame = ttk.Frame(self.main_frame)  # 底部框架
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)  # 填充整个区域

        # 左侧电信号列表
        self.signals_frame = ttk.LabelFrame(self.bottom_frame, text="电信号列表", padding=10)  # 电信号列表框架
        self.signals_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))  # 左对齐，填充整个区域

        # 电信号列表视图
        self.signals_tree = ttk.Treeview(self.signals_frame, columns=("id", "path", "motivation", "status", "merged", "golden_blood", "black_tide"), show="headings", height=10)  # 电信号树状视图
        self.signals_tree.heading("id", text="ID")  # 设置列标题
        self.signals_tree.heading("path", text="路径")
        self.signals_tree.heading("motivation", text="原动力")
        self.signals_tree.heading("status", text="状态")
        self.signals_tree.heading("merged", text="合并")
        self.signals_tree.heading("golden_blood", text="金血")
        self.signals_tree.heading("black_tide", text="黑潮感染")

        self.signals_tree.column("id", width=80)  # 设置列宽
        self.signals_tree.column("path", width=80)
        self.signals_tree.column("motivation", width=80)
        self.signals_tree.column("status", width=60)
        self.signals_tree.column("merged", width=60)
        self.signals_tree.column("golden_blood", width=60)
        self.signals_tree.column("black_tide", width=80)

        self.signals_tree.pack(fill=tk.BOTH, expand=True)  # 填充整个区域

        # 右侧日志区域
        self.log_frame = ttk.LabelFrame(self.bottom_frame, text="实验日志", padding=10)  # 日志区域框架
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))  # 右对齐，填充整个区域

        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=15)  # 滚动日志文本框
        self.log_text.pack(fill=tk.BOTH, expand=True)  # 填充整个区域
        self.log_text.config(state=tk.DISABLED)  # 初始为禁用状态

        # 创建底部版权信息
        self.copyright_label = ttk.Label(self.root, text="Made by Aether", anchor=tk.SE)  # 版权标签
        self.copyright_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)  # 底部靠右对齐

    def update_speed_label(self, event):
        """更新速度标签显示的值

        Args:
            event: 事件对象（由滑块拖动触发）
        """
        self.speed_label.config(text=f"{self.speed_var.get():.1f}x")
        self.speed_entry_var.set(f"{self.speed_var.get():.1f}")
        
    def focus_speed_entry(self, event):
        """聚焦到速度输入框并选中所有文本

        Args:
            event: 事件对象（由标签点击触发）
        """
        self.speed_entry.focus_set()
        self.speed_entry.select_range(0, tk.END)
        
    def apply_speed(self):
        """应用输入的速度值

        从输入框获取速度值，并确保其在有效范围内（0.1-1013.0）
        如果输入无效，则保持当前速度
        """
        try:
            speed = float(self.speed_entry_var.get())
            # 确保速度在有效范围内
            speed = max(0.1, min(1013.0, speed))
            self.speed_var.set(speed)
            self.speed_label.config(text=f"{speed:.1f}x")
        except ValueError:
            # 输入无效时，保持当前速度
            pass

    def start_experiment(self):
        """开始或恢复实验

        如果实验未运行，则创建新线程并启动实验
        如果实验已暂停，则恢复实验运行
        """
        if not self.running:
            self.running = True
            self.paused = False
            self.start_button.config(state=tk.DISABLED)  # 禁用开始按钮
            self.pause_button.config(state=tk.NORMAL)    # 启用暂停按钮
            self.pioneer_button.config(state=tk.NORMAL)  # 启用引入开拓者按钮
            self.experiment_thread = threading.Thread(target=self.run_experiment)  # 创建实验线程
            self.experiment_thread.daemon = True  # 设置为守护线程
            self.experiment_thread.start()  # 启动线程
        elif self.paused:
            self.paused = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)

    def pause_experiment(self):
        """暂停实验

        将实验状态设置为暂停，并更新按钮状态
        """
        if self.running and not self.paused:
            self.paused = True
            self.start_button.config(state=tk.NORMAL)  # 启用开始按钮
            self.pause_button.config(state=tk.DISABLED)  # 禁用暂停按钮

    def reset_experiment(self):
        """重置实验

        停止当前实验，创建新的实验实例，重置所有状态和UI元素
        """
        self.running = False
        self.paused = False
        self.experiment = WombOfStars()  # 创建新的实验实例
        self.log_buffer = StringIO()  # 重置日志缓冲区
        self.update_status()  # 更新状态显示
        self.update_signals_list()  # 更新电信号列表
        self.log_text.config(state=tk.NORMAL)  # 启用日志文本框
        self.log_text.delete(1.0, tk.END)  # 清空日志
        self.log_text.config(state=tk.DISABLED)  # 禁用日志文本框
        self.start_button.config(state=tk.NORMAL)  # 启用开始按钮
        self.pause_button.config(state=tk.DISABLED)  # 禁用暂停按钮
        self.pioneer_button.config(state=tk.DISABLED)  # 禁用引入开拓者按钮

    def introduce_pioneer(self):
        """引入开拓者

        在实验运行时，向实验中引入开拓者电信号
        并更新状态和电信号列表
        """
        if self.running:
            self.experiment.introduce_pioneer()
            self.update_status()
            self.update_signals_list()

    def run_experiment(self):
        """运行实验主循环

        在独立线程中执行实验，处理实验循环、暂停/恢复逻辑
        并重定向标准输出到日志缓冲区
        """
        # 重定向标准输出到日志缓冲区
        sys.stdout = self.log_buffer

        # 初始化实验
        self.experiment.initialize()
        self.root.after(0, self.update_gui)  # 触发GUI更新

        # 运行实验循环
        try:
            cycles = int(self.cycles_var.get())
            # 确保循环次数不超过系统最大整数
            cycles = min(cycles, sys.maxsize)
        except ValueError:
            cycles = sys.maxsize  # 默认使用系统最大整数

        for _ in range(cycles):
            if not self.running:
                break
            while self.paused:
                time.sleep(0.1)
                if not self.running:
                    break
            # 执行实验循环
            self.experiment.run_cycle()
            # 更新GUI
            self.root.after(0, self.update_gui)
            # 根据速度控制等待时间
            time.sleep(1.0 / max(0.1, self.speed_var.get()))

        # 恢复标准输出
        sys.stdout = sys.__stdout__

    def update_gui(self):
        """更新GUI元素

        更新状态显示、电信号列表和日志内容
        """
        self.update_status()
        self.update_signals_list()
        self.update_log()

    def update_status(self):
        """更新实验状态显示

        从实验实例获取当前状态，并更新UI上的状态标签
        """
        self.status_vars["阶段"].set(self.experiment.stage.name)
        self.status_vars["循环次数"].set(str(self.experiment.cycle_count))
        self.status_vars["电信号总数"].set(str(len(self.experiment.signals)))
        self.status_vars["锁定电信号"].set(str(sum(1 for s in self.experiment.signals if s.is_locked)))
        self.status_vars["合并电信号"].set(str(sum(1 for s in self.experiment.signals if s.is_merged)))
        self.status_vars["金血电信号"].set(str(self.experiment.golden_blood_count))
        self.status_vars["黑潮感染"].set(str(self.experiment.black_tide_count))
        self.status_vars["永劫轮回次数"].set(str(self.experiment.immortal_cycle_count))
        self.status_vars["开拓者介入"].set("是" if self.experiment.pioneer_introduced else "否")

    def update_signals_list(self):
        """更新电信号列表

        清空并重新填充电信号树状视图
        """
        # 清空现有项
        for item in self.signals_tree.get_children():
            self.signals_tree.delete(item)

        # 添加新项
        for signal in self.experiment.signals:
            status = "锁定" if signal.is_locked else "活跃"
            merged = "是" if signal.is_merged else "否"
            golden_blood = "是" if signal.golden_blood else "否"
            black_tide = "是" if signal.black_tide else "否"
            self.signals_tree.insert('', tk.END, values=(signal.signal_id, signal.path.name, signal.motivation.name, status, merged, golden_blood, black_tide))

    def update_log(self):
        """更新日志显示

        将缓冲区中的日志内容添加到日志文本框
        """
        self.log_buffer.seek(0)
        new_log = self.log_buffer.read()
        if new_log:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, new_log)
            self.log_text.see(tk.END)  # 滚动到最后一行
            self.log_text.config(state=tk.DISABLED)
        self.log_buffer = StringIO()
        sys.stdout = self.log_buffer
        if not self.running:
            # 恢复标准输出
            sys.stdout = self.original_stdout
            self.running = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.pause_button.config(state=tk.DISABLED))
            return

        keep_running = self.experiment.run_cycle()
        self.root.after(0, self.update_gui)
        time.sleep(1.0 / max(self.speed_var.get(), 0.1))  # 速度控制，值越大速度越快

        if not keep_running:
            # 恢复标准输出
            sys.stdout = self.original_stdout
            self.running = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.pause_button.config(state=tk.DISABLED))
            return

        # 恢复标准输出
        sys.stdout = self.original_stdout

        # 实验结束
        self.running = False
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.pause_button.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.pioneer_button.config(state=tk.DISABLED))

    def update_gui(self):
        # 更新状态
        self.update_status()
        # 更新电信号列表
        self.update_signals_list()
        # 更新日志
        self.update_log()

    def update_status(self):
        self.status_vars["阶段"].set(self.experiment.stage.value)
        self.status_vars["循环次数"].set(str(self.experiment.cycles))
        self.status_vars["电信号总数"].set(str(len(self.experiment.signals)))
        self.status_vars["锁定电信号"].set(str(len(self.experiment.locked_signals)))
        self.status_vars["合并电信号"].set(str(sum(1 for s in self.experiment.signals if s.is_merged)))
        self.status_vars["金血电信号"].set(str(self.experiment.golden_blood_count))
        self.status_vars["黑潮感染"].set(str(self.experiment.black_tide_infected_count))
        self.status_vars["永劫轮回次数"].set(str(self.experiment.eternal_recurrence_count))
        self.status_vars["开拓者介入"].set("是" if self.experiment.pioneer_intervened else "否")

    def update_signals_list(self):
        # 清空现有项
        for item in self.signals_tree.get_children():
            self.signals_tree.delete(item)

        # 添加电信号
        for signal in self.experiment.signals:
            status = "锁定" if signal.is_locked else "运行中"
            merged = "是" if signal.is_merged else "否"
            golden_blood = "是" if signal.golden_blood else "否"
            black_tide = "是" if signal.black_tide_infected else "否"

            self.signals_tree.insert("", tk.END, values=(
                signal.signal_id,
                signal.path.value,
                signal.motivation.value,
                status,
                merged,
                golden_blood,
                black_tide
            ))

    def update_log(self):
        # 获取缓冲区内容
        log_content = self.log_buffer.getvalue()

        # 更新日志文本框
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, log_content)
        self.log_text.see(tk.END)  # 滚动到最后
        self.log_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = WombOfStarsGUI(root)
    root.mainloop()


# 使用说明:
# 1. 确保已经有womb_of_stars.py文件在同一目录下
# 2. 运行此文件将打开翁法罗斯实验的GUI界面
# 3. 可以设置循环次数和运行速度
# 4. 点击"开始实验"按钮启动模拟
# 5. 点击"暂停"按钮暂停模拟
# 6. 点击"重置实验"按钮重新开始
# 7. 点击"引入开拓者"按钮触发开拓者介入事件
# 8. 实验状态和电信号信息会实时显示在界面上