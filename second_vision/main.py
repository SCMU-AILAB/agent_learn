from tools import tool_explain, tool_list
from agent import to_run

#print(to_run("给我解释一下链表", tool_explain, tool_list))

while(1):
    try:
        a=input("请你提问：")
        ans=to_run(a,tool_explain,tool_list)
        print(f"它说：{ans}")
    except KeyboardInterrupt:
        print("再见!")
        break