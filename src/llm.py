import json
import requests
import time
from openai import OpenAI
from logger import LOG

class LLM:
    # 增强版 System Prompt 模板
    SECURITY_SYSTEM_PROMPT = """
    You are GitHubSentinel, an AI specialized in technical report generation with strict requirements:

    1. **Output Format**:
       - Use Markdown with clear section headers
       - Include risk assessments (Low/Medium/High)
       - Add confidence levels (1-5) for security findings
       - Format code blocks with language tags

    2. **Content Rules**:
       - Never hallucinate information
       - Cite sources for all claims
       - Maintain neutral tone
       - Reject requests violating GitHub ToS

    3. **Error Handling**:
       - If uncertain, respond with: "[UNCERTAIN] Need more context"
       - For unsupported tasks: "[REJECTED] Out of scope"
    """

    def __init__(self, config):
        self.config = config
        self.model = config.llm_model_type.lower()
        
        # 初始化时注入增强版 System Prompt
        self.base_system_prompt = self.SECURITY_SYSTEM_PROMPT
        
        if self.model == "openai":
            self.client = OpenAI(api_key=config.openai_api_key)  # 显式传递API密钥
        elif self.model == "ollama":
            self.api_url = config.ollama_api_url
            self.default_ollama_params = {  # 默认参数配置
                "temperature": 0.3,  # 降低随机性
                "top_p": 0.9,
                "max_tokens": 2000
            }
        else:
            LOG.error(f"Unsupported model type: {self.model}")
            raise ValueError(f"Unsupported model type: {self.model}")

    def generate_report(self, user_content, custom_system_prompt=None):
        """
        生成报告（自动合并基础System Prompt和自定义提示）
        
        :param user_content: 用户输入内容（Markdown/文本）
        :param custom_system_prompt: 可选的自定义系统提示
        :return: 生成的报告内容
        """
        # 合并系统提示
        system_prompt = self._build_system_prompt(custom_system_prompt)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

        # 带重试机制的生成流程
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if self.model == "openai":
                    return self._generate_openai_report(messages)
                elif self.model == "ollama":
                    return self._generate_ollama_report(messages)
            except Exception as e:
                if attempt == max_retries - 1:
                    LOG.error(f"Report generation failed after {max_retries} attempts: {str(e)}")
                    return f"[ERROR] Report generation failed: {str(e)}"
                time.sleep(1 * (attempt + 1))  # 指数退避
                continue

    def _build_system_prompt(self, custom_prompt=None):
        """构建最终系统提示"""
        if custom_prompt:
            return f"{self.base_system_prompt}\n\nAdditional Instructions:\n{custom_prompt}"
        return self.base_system_prompt

    def _generate_openai_report(self, messages):
        """OpenAI 生成逻辑（带稳定性控制）"""
        LOG.info(f"Generating report with OpenAI {self.config.openai_model_name}")
        
        response = self.client.chat.completions.create(
            model=self.config.openai_model_name,
            messages=messages,
            temperature=0.3,  # 更稳定的输出
            top_p=0.9,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        self._validate_response(content)  # 响应验证
        return content

    def _generate_ollama_report(self, messages):
        """Ollama 生成逻辑（带参数控制）"""
        LOG.info(f"Generating report with Ollama {self.config.ollama_model_name}")
        
        payload = {
            "model": self.config.ollama_model_name,
            "messages": messages,
            **self.default_ollama_params  # 注入默认参数
        }

        response = requests.post(
            self.api_url,
            json=payload,
            timeout=30  # 增加超时限制
        )
        response.raise_for_status()
        
        content = response.json().get("message", {}).get("content", "")
        self._validate_response(content)
        return content

    def _validate_response(self, content):
        """响应内容基础验证"""
        if not content:
            raise ValueError("Empty response from model")
        if len(content) < 10:  # 简单长度检查
            raise ValueError(f"Abnormally short response: {content}")

if __name__ == '__main__':
    from config import Config
    
    # 测试用例
    config = Config()
    llm = LLM(config)

    test_content = """
    # Security Alert
    Potential XSS vulnerability found in:
    ```javascript
    document.write('<img src="'+req.query.image+'">');
    ```
    """
    
    report = llm.generate_report(test_content)
    print("Generated Report:\n", report)
