import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMClient:
    def __init__(self, model="gpt-4o"):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = None
        
        if not self.api_key:
            # Fallback for openrouter
            self.api_key = os.environ.get("OPENROUTER_API_KEY")
            if self.api_key:
                self.base_url = "https://openrouter.ai/api/v1"
            else:
                raise ValueError("OPENAI_API_KEY or OPENROUTER_API_KEY not found in environment variables.")
        
        if self.base_url:
             self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
             self.client = OpenAI(api_key=self.api_key)
             
        self.model = model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def complete(self, messages, temperature=0.0, max_tokens=500):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in LLM call: {e}")
            raise e

    def get_summary(self, text_chunk):
        prompt = f"""Summarize the following scientific concepts and examples into a concise 'Rule' or 'Key Insight' that would help answer similar questions in the future.
        
        examples:
        {text_chunk}
        
        Key Insight:"""
        
        messages = [{"role": "user", "content": prompt}]
        return self.complete(messages)

if __name__ == "__main__":
    client = LLMClient()
    print("Test response:", client.complete([{"role": "user", "content": "Hello, are you working?"}]))
