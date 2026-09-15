import dashscope
from dashscope import Generation
from app.config import settings

SYSTEM_PROMPT = (
    "你是一个AI文本检测分析器，只能输出JSON格式的结果。"
    "严格按照指定格式返回，不要添加任何其他内容。"
)

USER_PROMPT_TMPL = (
    "分析这段文本是否由AI生成，返回JSON格式：\n\n{text}\n\n"
    "JSON格式要求（严格遵守）：\n"
    '{{\n'
    '  "label": "ai 或 human 或 uncertain",\n'
    '  "score": 0到1之间的数字,\n'
    '  "confidence": "high 或 medium 或 low",\n'
    '  "rationale": "简短判断理由",\n'
    '  "detailed_analysis": "详细分析文字",\n'
    '  "key_indicators": ["指标1", "指标2"],\n'
    '  "methodology": "分析方法说明"\n'
    '}}\n\n'
    "重要：只返回JSON，不要添加任何其他文字或解释！"
)


def detect_with_qwen(text: str):
    if not settings.qwen_api_key:
        raise RuntimeError("DASHSCOPE_API_KEY 未配置")
    dashscope.api_key = settings.qwen_api_key
    prompt = USER_PROMPT_TMPL.format(text=text.strip())
    resp = Generation.call(
        model=settings.qwen_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=settings.detect_temperature,
        result_format="message",
        timeout=settings.qwen_timeout,
    )
    content = resp.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
    return content

