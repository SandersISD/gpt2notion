class CallablesProps:
    def __init__(self, name: str, type: str, description: str, required: bool):
        self.name = name
        self.type = type
        self.description = description
        self.required = required

class Callables:
    def __init__(self, func, description: str, *args: CallablesProps):
        self.func = func
        self.description = description
        self.args = args

    def __call__(self, *args):
        return self.func(*args)
    
    def formatting(self):
        tool_doc = {
            "type": "function",
            "function": {
                "name": self.func.__name__,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            }
        }

        for arg in self.args:
            tool_doc["function"]["parameters"]["properties"][arg.name] = {"type":arg.type, "description":arg.description}
            if arg.required: 
                tool_doc["function"]["parameters"]["required"].append(arg.name)
        
        print("Created: " + str(tool_doc))
        return tool_doc

def callable_list(*clbs: Callables):
    list = []
    for clb in clbs:
        list.append(clb.formatting())
    print(list)
    return list

# def HelloWorld(a,b,c):
#     return (a + b +c)

# Call_HelloWorld = Callables(
#     HelloWorld,
#     "Do a + b + c",
#     Callables_Props("a","int", "a", True),
#     Callables_Props("b","int", "b", True),
#     Callables_Props("c","int", "c", True)
# )

# CallableList(
#     Call_HelloWorld
# )
