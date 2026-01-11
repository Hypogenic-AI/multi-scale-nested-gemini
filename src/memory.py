from abc import ABC, abstractmethod
from src.data_loader import format_example

class Memory(ABC):
    def __init__(self, limit_chars=8000): # approx 2000 tokens
        self.limit_chars = limit_chars
        
    @abstractmethod
    def add_examples(self, examples):
        pass
        
    @abstractmethod
    def commit_task(self, task_name, llm_client=None):
        pass
        
    @abstractmethod
    def retrieve(self):
        pass

class FlatMemory(Memory):
    def __init__(self, limit_chars=8000):
        super().__init__(limit_chars)
        self.examples_buffer = [] # List of formatted strings
        
    def add_examples(self, examples):
        # examples is a list of dicts (dataset rows)
        for ex in examples:
            self.examples_buffer.append(format_example(ex, include_answer=True))
            
    def commit_task(self, task_name, llm_client=None):
        # Flat memory doesn't distinguish tasks, just keeps adding
        pass
        
    def retrieve(self):
        # Return recent examples fitting in limit
        context = ""
        # Iterate backwards
        for ex in reversed(self.examples_buffer):
            if len(context) + len(ex) < self.limit_chars:
                context = ex + "\n---\n" + context
            else:
                break
        return context

class NestedMemory(Memory):
    def __init__(self, limit_chars=8000):
        super().__init__(limit_chars)
        self.long_term_memory = [] # List of summaries
        self.short_term_buffer = [] # Current task examples
        # Split budget: 50% LTM, 50% STM
        self.ltm_limit = limit_chars // 2
        self.stm_limit = limit_chars // 2
        
    def add_examples(self, examples):
        for ex in examples:
            self.short_term_buffer.append(format_example(ex, include_answer=True))
            
    def commit_task(self, task_name, llm_client):
        if not self.short_term_buffer:
            return
            
        print(f"Summarizing task: {task_name}...")
        # Concatenate all short term examples
        full_text = "\n".join(self.short_term_buffer)
        
        # Chunk if too large for summarizer context (gpt-4o is 128k, so should be fine for 50 examples)
        # 50 examples * 500 chars = 25k chars. Fine.
        
        summary = llm_client.get_summary(full_text)
        self.long_term_memory.append(f"Subject: {task_name}\nKey Insights:\n{summary}\n")
        
        # Clear short term buffer for next task
        self.short_term_buffer = []
        
    def retrieve(self):
        # Construct context: LTM + STM
        context = ""
        
        # 1. Add LTM (Summaries)
        ltm_text = ""
        for summary in self.long_term_memory:
            if len(ltm_text) + len(summary) < self.ltm_limit:
                ltm_text += summary + "\n===\n"
        
        # 2. Add STM (Recent examples)
        stm_text = ""
        # Iterate backwards
        for ex in reversed(self.short_term_buffer):
            if len(stm_text) + len(ex) < self.stm_limit:
                stm_text = ex + "\n---\n" + stm_text
            else:
                break
                
        return f"Past Knowledge:\n{ltm_text}\n\nCurrent Examples:\n{stm_text}"