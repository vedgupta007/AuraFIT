from google import genai
from google.genai import types

fc = types.FunctionCall(name="test", args={"search": "apple"})
print(type(fc.args))
