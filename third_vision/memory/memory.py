import json
import os

# ======================================================================
# memory.py —— 把「桌子」存到硬盘，再从硬盘搬回来
#   桌子 = to_run 里的 message（内存里的列表，函数一返回就没了）
#   抽屉 = history.json（硬盘上的文件，关掉程序也还在）
# ======================================================================


# ---------------- json 的四个函数：作用 与 区别 ----------------
#   s = string。带 s 的跟「字符串」打交道；不带 s 的跟「文件把手」打交道。
#
#   json.loads(文本)     字符串    → 列表/字典    （读进来）
#   json.dumps(对象)     列表/字典 → 字符串      （倒出去）
#   json.load(f)         文件把手  → 列表/字典    （读进来）  ← read_history 用这个
#   json.dump(对象, f)   列表/字典 → 文件把手    （倒出去）  ← save_history 用这个
#
#   区别只有两点：
#     ① 给它的东西不同：带 s 给「字符串」；不带 s 给 open() 递出来的「把手 f」
#     ② 方向不同：load = 读进来（文本/文件 → Python 对象）
#                 dump = 倒出去（Python 对象 → 文本/文件）
#   参数顺序也不同：load(f) 只给把手；dump(对象, f) 先给「要写的东西」，再给把手。
this=os.path.dirname(os.path.abspath(__file__)) 

class memory:
    def __init__(self,history):
        self.history = os.path.join(this, "history", history)

    @staticmethod
    def get_history():
        count=0
        historys=os.listdir(os.path.join(this, "history")) or []

        if historys!=[]:
            for i in historys:
                print(f"{count+1}."+i)
                count+=1
            chio=int(input("请选择你想回到的对话，输入每次对话前的数字,开启新对话请输入0:"))
        else:
            chio=int(input("当前无对话，开启新对话请输入0:"))
        
        while(1):
            if chio<=len(historys) and chio>0:
                return historys[chio-1]
            elif chio==0:
                name=input("请输入新对话的名字:")
                return name+".json"
            else:
                chio=int(input("输入错误，请重新输入:"))


    def read_history(self):
        """文件不存在 → 返回空列表；存在 → 读出列表"""
        # 先问一句「文件在不在」：第一次跑还没有这个文件，
        # 直接 open 去读会抛 FileNotFoundError（当场崩）。
        if not os.path.exists(self.history):
            return []
        if os.path.getsize(self.history)==0:
            return []

        # with open(路径, encoding=...) as f:
        #   open(...) = 开门。它给你的不是「文件内容」，是一个「文件把手」f
        #   as f      = 给把手起个名，下面用 f 指这个文件
        #   with      = 自动关门器：这段缩进走完自动 f.close()，哪怕中途报错也关
        #   encoding  = 读的时候按 utf-8 解，避免中文乱码
        with open(self.history, encoding="utf-8") as f:
            # json.load（不带 s）：把「文件把手」交给翻译官
            #   → 从文件里读出文字，解析成 Python 列表
            #   写成 json.loads(f) 会报错：loads 要的是字符串，不是把手
            return json.load(f)

    def save_history(self,message):
        """把列表写进文件"""
        # "w" = 写模式（默认是 "r" 读模式）：
        #   ① 用读模式去写会报错
        #   ② "w" 会先把文件清空再写 → 所以这里是「把整张桌子重写一遍」的快照，
        #      不是往后追加一条（因为 message 本身就是全量历史）
        with open(self.history, "w", encoding="utf-8") as f:
            # json.dump（不带 s）：把 message 变成 JSON 文本，倒进文件把手 f
            #   ensure_ascii=False → 中文原样写；默认 True 会写成 \u6211 这种转义码
            #                        （转义码也是合法 JSON，load 读回来一样，只是人看不懂）
            #   indent=2           → 每层缩进 2 空格；默认 None 会把整个 JSON 挤成一行
            #   （这两个参数只影响「好不好看」，不影响程序能不能读回来）
            json.dump(message, f, ensure_ascii=False, indent=2)
