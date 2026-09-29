from agent import Agent

God = Agent()

while 1:
    try:
        a = input("请你提问：")
        ans = God.to_run(a)
        print(f"它说：{ans}")
    except KeyboardInterrupt:
        print("")
        print("再见!")
        break
    except EOFError:
        print("")
        print("再见!")
        break
