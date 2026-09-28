class combine:
    tools_explain=[]
    tools_list={}
    def __init__(self,tool):
        combine.tools_explain+=tool.tool_explain
        combine.tools_list[tool.name]=tool.tol
        