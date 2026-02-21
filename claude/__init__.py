"""
CDD Claude Integration Package
==============================
整合claude_integration、claude_skills、claude_tools的统一包。

宪法依据: §309 Claude Code自动化任务原则

目录结构:
- claude/           # 主包
  - config.yaml     # 主配置
  - tools/          # Python工具模块
  - skills/         # 技能定义文件
  - github_actions/ # GitHub Actions
  - hooks/          # Hooks配置
  - templates/      # 技能模板
"""

__version__ = "2.0.0"
__all__ = ["tools", "skills"]