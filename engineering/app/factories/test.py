from llmFactory import LLMFactory

llm = LLMFactory.create()
res = llm.invoke("Hello, how are you?")
print(res)