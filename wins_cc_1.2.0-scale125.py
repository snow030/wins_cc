import tkinter as tk
import win32gui as GUI
import pytesseract as OCR
from PIL import ImageGrab
from threading import Thread
from chrome_trans import trans_li
from time import sleep
from os import popen
import re
popen(r"C:/Windows/System32/LiveCaptions.exe")

def thd(func):
    def wrapper(*args, **kwargs):
        Thread(target = func, args = args, kwargs = kwargs, daemon=True).start()
    return wrapper

# Pattern List
ill_ptn    = re.compile(r"(?:I|1)\'11"    , re.S) # I will
newln_ptn  = re.compile(r"(?<!\n)\n(?!\n)", re.S) # newline
double_ptn = re.compile(r"\n\n"           , re.S) # real new sentence
period_ptn = re.compile(r"(\.|\?|,|!) "   , re.S) # push § after full stop
space_ptn  = re.compile(r"\S+?(?=\s|$)+"  , re.S) # space to pattern
cut_ptn    = re.compile(r"[^§]+?(?=§|$)"  , re.S) # split by §

pre_list = [] #[('en','zh'),]
rect   = (0, 0, 0, 0)
margin = (5, 5, -94, -5)
screen = (0, 0, 0, 0)

# Create pane
root = tk.Tk()
root.title("CC字幕")
root.geometry("0x0")
root.configure(bg='black')
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "black")

# Create textarea
text_area = tk.Text(root,
    font = ("Microsoft YaHei", 14),
    bg   = "black",
    fg   = "white",
    wrap = "word",
    padx = 10,
    pady = 10
)
text_area.pack(expand=True, fill="both")
text_area.config(state=tk.DISABLED)

sleep(.5)
hwnd_caption = GUI.FindWindow(None, "Live Captions")
GUI.MoveWindow(hwnd_caption, 0, 0, 730, 300, False)

# 避免中文字幕被背景覆盖
def reshow(event): root.lift()

# 截取caption并转为有效句式
def fetch_cc() -> str:
    img = ImageGrab.grab(screen)
    cc = OCR.image_to_string(img, lang="eng")
    cc = ill_ptn   .sub("I\'ll", cc)
    cc = newln_ptn .sub(" "    , cc)
    cc = double_ptn.sub("\n"   , cc)
    cc = period_ptn.sub(r"\1§" , cc)
    return cc

# 用longest common subsentence算法截取新内容&旧内容
def long_common(new_list:list[str]) -> list[str]:
    global pre_list
    len_p = len(pre_list)
    len_n = len(new_list)
    board = [[0]*len_n for _ in range(len_p)]
    class longest: len = end_p = end_n = 0
    # Check longest
    for idx_n in range(len_n):
        pattern_n = stn2ptn(new_list[idx_n])
        for idx_p in range(len_p):
            not_match = not re.match(pattern_n, pre_list[idx_p][0], re.S)
            if not_match: continue

            length = board[idx_p][idx_n] = board[max(idx_p-1,0)][max(idx_n-1,0)] + 1
            if length != 0 and length >= longest.len:
                longest.len   = length
                longest.end_p = idx_p
                longest.end_n = idx_n
    # Cut
    if longest.len > 1 or (longest.len == 1 and len(pre_list[longest.end_p][0]) > 40):
        temp_sta = len_n - max(15, longest.len + 2) - 1
        start_p  = max(0, longest.end_p - longest.end_n + temp_sta)
        start_n  = max(longest.end_n + 1, temp_sta)
        pre_list = pre_list[start_p : longest.end_p + 1]
        new_list = new_list[start_n : ]
    else:
        pre_list = []
    return new_list

# 翻译功能接口
def stn_trans(en_list:list[str]) -> list[str,str]|None:
    if not en_list: return []
    try:
        trans_list = trans_li(en_list, "zh-CN", "en")
    except Exception as err:
        update_text_area(str(err))
        return
    return list(zip(en_list, trans_list))

# 整合文本列
def combine_stn(stn_list:list[tuple[str,str]]) -> str:
    return "".join(stn[1] for stn in stn_list)

# 内容渲染
def update_text_area(content:str, mark_idx:int|None = None) -> None:
    text_area.config(state=tk.NORMAL)

    text_area.replace("1.0", tk.END, content)
    if mark_idx is not None:
        text_area.tag_add("mark", f"1.{mark_idx}", tk.END)
        text_area.tag_config("mark", foreground="yellow")

    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)

# 单句转为可用pattern
def stn2ptn(str1:str) -> str:
    word_list = space_ptn.findall(str1)
    return r".*?" + r"\s*".join([re.escape(W) for W in word_list])

# second thread
def bg_tk():
    # Create background
    root_bg = tk.Tk()
    root_bg.title("CC字幕_bg")
    root_bg.geometry("0x0")
    root_bg.configure(bg="black")
    root_bg.overrideredirect(True)
    root_bg.wm_attributes("-topmost", True)
    root_bg.attributes("-alpha", 0.6)
    root_bg.bind("<Button-1>", reshow)
    root_bg.bind("<Button-2>", reshow)
    root_bg.bind("<Button-3>", reshow)

    # 让中文cc黏附live caption
    def sticky() -> None:
        global rect, screen
        new_rect = GUI.GetWindowRect(hwnd_caption)
        if rect != new_rect:
            rect = new_rect
            screen = tuple( round((rect[idx]+margin[idx])*1.25) for idx in range(4) ) # scale 125%
            new_geo = f"{rect[2]-rect[0]+margin[2]}x{round((rect[3]-rect[1])*0.8)}+{rect[0]}+{rect[3]}"
            root_bg.geometry(new_geo)
            root.geometry(new_geo)
    
    # third thread
    def rt_main() -> None:
        global pre_list
        while GUI.IsWindow(hwnd_caption):
            sticky()
            # 主循环
            cc = fetch_cc()
            new_list = cut_ptn.findall(cc)
            new_list = long_common(new_list)
            new_list = stn_trans(new_list)
            if new_list is None:
                sleep(2)
                continue
            pre_stn = combine_stn(pre_list)
            new_stn = combine_stn(new_list)
            pre_list += new_list
            update_text_area(pre_stn + new_stn, len(pre_stn))
            sleep(.2)
        # 结束程序
        root_bg.quit()
        root.quit()
        root.destroy()

    thd(rt_main)()
    root_bg.mainloop()

thd(bg_tk)()
root.lift()
root.mainloop()
