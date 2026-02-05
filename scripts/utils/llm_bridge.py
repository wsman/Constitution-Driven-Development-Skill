import os
import json
import yaml
import requests
from typing import Dict, Any
from pathlib import Path

class LLMBridge:
    """
    CDD LLM Bridge (Digital Airlock)
    ===============================
    Responsibility:
    1. Securely handle API Keys (Env vars only).
    2. Enforce Deterministic Outputs (Temp=0).
    3. Isolate network side-effects from core logic.
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config = self._load_config()
        self.auditor_config = self.config.get("external_auditor", {})
        
    def _load_config(self) -> Dict[str, Any]:
        """Load config with fallback strategy"""
        candidates = [
            self.project_root / "cdd_config.yaml",
            self.project_root / "templates" / "cdd_config.yaml"
        ]
        for p in candidates:
            if p.exists():
                try:
                    return yaml.safe_load(p.read_text(encoding="utf-8"))
                except Exception as e:
                    print(f"⚠️  [LLMBridge] Config warning: {e}")
        return {}

    def call_judge(self, system_prompt: str, user_content: str) -> Dict[str, Any]:
        """
        Execute a Judicial Review Request.
        """
        if not self.auditor_config.get("enabled", False):
            return {"verdict": "SKIPPED", "summary": "Semantic audit is disabled in config."}

        # 1. Security Check: API Key presence
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "verdict": "ERROR", 
                "error": "Missing API Key. Please set DEEPSEEK_API_KEY or OPENAI_API_KEY."
            }

        # 2. Construct the Payload (Enforcing Determinism)
        base_url = self.auditor_config.get("api", {}).get("base_url", "https://api.deepseek.com")
        model = self.auditor_config.get("provider", "deepseek-reasoner")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": self.auditor_config.get("judicial_parameters", {}).get("temperature", 0.0),
            "max_tokens": self.auditor_config.get("judicial_parameters", {}).get("max_tokens", 4096),
            "stream": False
        }

        # 3. Network Isolation (The "Spore" Check)
        # 可以在这里添加额外的网络策略检查，例如只允许特定的 endpoint
        
        try:
            response = requests.post(
                f"{base_url}/chat/completions", 
                headers=headers, 
                json=payload, 
                timeout=self.auditor_config.get("api", {}).get("timeout", 60)
            )
            response.raise_for_status()
            
            # 4. Result Parsing
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Attempt to extract pure JSON if the model chattered
            if "```json" in content:
                import re
                match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            
            # Fallback for direct JSON or simple text
            try:
                return json.loads(content)
            except:
                return {"verdict": "UNKNOWN", "reasoning": content, "summary": "Model returned non-JSON output."}
            
        except Exception as e:
            return {"verdict": "ERROR", "error": f"Bridge Communication Failure: {str(e)}"}