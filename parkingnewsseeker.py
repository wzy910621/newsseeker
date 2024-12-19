import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class ParkingNewsSeeker:
    def __init__(self, root):
        self.root = root
        self.root.title("停车新闻采集器")
        self.root.geometry("1800x1000")
        
        # 设置全局样式
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('微软雅黑', 14))
        self.style.configure('TButton', font=('微软雅黑', 14))
        self.style.configure('TRadiobutton', font=('微软雅黑', 14))
        self.style.configure('TLabelframe.Label', font=('微软雅黑', 14, 'bold'))
        self.style.configure('TLabelframe', borderwidth=2)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = tk.Label(title_frame, 
                              text="新闻采集器 1.0", 
                              font=('微软雅黑', 28, 'bold'),
                              fg='#1a73e8',  # Google蓝色
                              pady=20)
        title_label.pack()
        
        # 添加分隔线
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # 创建上部分框架
        self.create_top_frame()
        
        # 创建下部分框架
        self.create_bottom_frame()
        
        # 创建进度条框架
        self.create_progress_frame()

    def create_top_frame(self):
        """创建顶部框架"""
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 采集时间框架
        time_frame = ttk.LabelFrame(top_frame, text="采集时间", padding="15")
        time_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 快捷时间选择
        quick_frame = ttk.Frame(time_frame)
        quick_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.time_var = tk.StringVar(value="custom")
        for text, value in [("过去24小时", "24h"), ("过去一周", "1w"), ("自定义", "custom")]:
            radio = ttk.Radiobutton(quick_frame, text=text, value=value, 
                                   variable=self.time_var, command=self.update_date_range)
            radio.pack(side=tk.LEFT, padx=20)
            self.style.configure('TRadiobutton', font=('微软雅黑', 14))
        
        # 日期选择
        date_frame = ttk.Frame(time_frame)
        date_frame.pack(fill=tk.X)
        
        ttk.Label(date_frame, text="起始日期:", font=('微软雅黑', 14)).pack(side=tk.LEFT, padx=(0, 10))
        self.start_date = DateEntry(date_frame, width=15, font=('微软雅黑', 14))
        self.start_date.pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Label(date_frame, text="结束日期:", font=('微软雅黑', 14)).pack(side=tk.LEFT, padx=(0, 10))
        self.end_date = DateEntry(date_frame, width=15, font=('微软雅黑', 14))
        self.end_date.pack(side=tk.LEFT)
        
        # 采集内容框架
        content_frame = ttk.LabelFrame(top_frame, text="采集内容", padding="15")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # 关键词选择
        keywords_frame = ttk.Frame(content_frame)
        keywords_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.parking_var = tk.BooleanVar(value=True)
        self.bike_var = tk.BooleanVar(value=False)
        self.share_var = tk.BooleanVar(value=False)
        
        # 使用自定义样式的Checkbutton
        style = ttk.Style()
        style.configure('Big.TCheckbutton', font=('微软雅黑', 14))
        
        for text, var in [("停车", self.parking_var), 
                         ("非机动车", self.bike_var), 
                         ("共享单车", self.share_var)]:
            cb = ttk.Checkbutton(keywords_frame, text=text, variable=var, style='Big.TCheckbutton')
            cb.pack(side=tk.LEFT, padx=20)
        
        # 其他关键词
        other_frame = ttk.Frame(content_frame)
        other_frame.pack(fill=tk.X)
        
        ttk.Label(other_frame, text="其他关键词:", 
                 font=('微软雅黑', 14)).pack(side=tk.LEFT, padx=(0, 10))
        self.keywords = ttk.Entry(other_frame, width=40, font=('微软雅黑', 14))
        self.keywords.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_bottom_frame(self):
        """创建底部框架"""
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建自定义样式的按钮
        style = ttk.Style()
        style.configure('Big.TButton', 
                       font=('微软雅黑', 16, 'bold'),
                       padding=(20, 10))
        
        # 开始采集按钮
        self.collect_btn = ttk.Button(bottom_frame, 
                                    text="开始采集", 
                                    command=self.start_collection,
                                    style='Big.TButton',
                                    width=25)
        
        # 添加鼠标悬停效果
        def on_enter(e):
            self.collect_btn.configure(style='BigHover.TButton')
        
        def on_leave(e):
            self.collect_btn.configure(style='Big.TButton')
        
        style.configure('BigHover.TButton', 
                       font=('微软雅黑', 16, 'bold'),
                       padding=(20, 10),
                       background='#1a73e8',
                       foreground='white')
        
        self.collect_btn.bind('<Enter>', on_enter)
        self.collect_btn.bind('<Leave>', on_leave)
        self.collect_btn.pack(pady=(0, 20))

    def create_progress_frame(self):
        """创建进度展示框架"""
        progress_frame = ttk.LabelFrame(self.main_frame, text="采集进度", padding="15")
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # 设置进度条样式
        style = ttk.Style()
        style.configure("Blue.Horizontal.TProgressbar", 
                       background='#1a73e8',
                       troughcolor='#E0E0E0',
                       bordercolor='#1a73e8',
                       lightcolor='#1a73e8',
                       darkcolor='#1a73e8')
        
        # 进度条
        self.progress = ttk.Progressbar(progress_frame, 
                                      length=300, 
                                      mode='determinate',
                                      style="Blue.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # 进度信息
        self.progress_label = ttk.Label(progress_frame, 
                                      text="准备开始采集...",
                                      font=('微软雅黑', 14))
        self.progress_label.pack()

    def start_collection(self):
        """开始采集"""
        # 这里添加实际的采集逻辑
        self.progress['value'] = 0
        self.progress_label['text'] = "正在采集中..."
        # 模拟进度
        self.root.after(100, self.update_progress)

    def update_progress(self, current=0):
        """更新进度条"""
        if current <= 100:
            self.progress['value'] = current
            self.progress_label['text'] = f"已完成 {current}%"
            self.root.after(100, lambda: self.update_progress(current + 2))
        else:
            self.progress_label['text'] = "采集完成！"

    def update_date_range(self):
        """根据选择的时间范围更新日期"""
        now = datetime.now()
        end_date = now
        
        if self.time_var.get() == "24h":
            start_date = now - timedelta(days=1)
            # 禁用日期选择
            self.start_date.configure(state='disabled')
            self.end_date.configure(state='disabled')
        elif self.time_var.get() == "1w":
            start_date = now - timedelta(weeks=1)
            # 禁用日期选择
            self.start_date.configure(state='disabled')
            self.end_date.configure(state='disabled')
        else:  # custom
            # 启用日期选择
            self.start_date.configure(state='normal')
            self.end_date.configure(state='normal')
            return
        
        # 更新日期选择器的值
        self.start_date.set_date(start_date)
        self.end_date.set_date(end_date)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingNewsSeeker(root)
    root.mainloop()
