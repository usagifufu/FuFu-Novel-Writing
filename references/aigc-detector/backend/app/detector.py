import json
import re
import uuid
from typing import List, Tuple
from app.qwen_client import detect_with_qwen
from app.schemas import TraceMark

def detect(text: str):
    raw = detect_with_qwen(text)

    try:
        # 清理和提取JSON
        cleaned_raw = raw.strip()

        # 移除可能的markdown代码块标记
        if cleaned_raw.startswith('```json'):
            cleaned_raw = cleaned_raw[7:]
        if cleaned_raw.startswith('```'):
            cleaned_raw = cleaned_raw[3:]
        if cleaned_raw.endswith('```'):
            cleaned_raw = cleaned_raw[:-3]

        cleaned_raw = cleaned_raw.strip()

        # 确保以{开头，以}结尾
        if not cleaned_raw.startswith('{'):
            start_idx = cleaned_raw.find('{')
            if start_idx != -1:
                cleaned_raw = cleaned_raw[start_idx:]

        if not cleaned_raw.endswith('}'):
            end_idx = cleaned_raw.rfind('}')
            if end_idx != -1:
                cleaned_raw = cleaned_raw[:end_idx+1]

        # 解析JSON
        data = json.loads(cleaned_raw)

        # 验证必需字段
        required_fields = ["label", "score"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必需字段: {field}")

        # 验证并清理数据
        label = str(data.get("label", "uncertain")).strip()
        if label not in ["ai", "human", "uncertain"]:
            label = "uncertain"

        score = float(data.get("score", 0.5))
        score = max(0.0, min(1.0, score))  # 确保在0-1范围内

        confidence = str(data.get("confidence", "medium")).strip()
        if confidence not in ["high", "medium", "low"]:
            confidence = "medium"

        rationale = str(data.get("rationale", "")).strip()
        detailed_analysis = str(data.get("detailed_analysis", "")).strip()

        key_indicators = data.get("key_indicators", [])
        if not isinstance(key_indicators, list):
            key_indicators = [str(key_indicators)]
        key_indicators = [str(item).strip() for item in key_indicators if str(item).strip()]

        methodology = str(data.get("methodology", "基于多维度特征分析的AI检测算法")).strip()

        return {
            "label": label,
            "score": score,
            "confidence": confidence,
            "rationale": rationale,
            "detailed_analysis": detailed_analysis,
            "key_indicators": key_indicators,
            "methodology": methodology
        }

    except Exception as e:
        # 如果所有解析都失败，返回标准错误响应
        return {
            "label": "uncertain",
            "score": 0.5,
            "confidence": "low",
            "rationale": f"检测失败: {str(e)[:100]}",
            "detailed_analysis": "由于AI模型返回格式不符合要求，无法提供详细分析。",
            "key_indicators": ["格式解析失败"],
            "methodology": "基础模式匹配"
        }

def mark_ai_traces(text: str) -> dict:
    """
    分析并标记文本中的AI生成痕迹，保持原始换行格式
    """
    original_text = text.rstrip()  # 保留开头换行，但移除结尾换行
    lines = original_text.split('\n')
    all_traces = []
    marked_lines = []

    # 逐行处理
    for line_idx, line in enumerate(lines):
        line_traces = []
        line_start_pos = sum(len(lines[i]) + 1 for i in range(line_idx))  # 该行在全文中的起始位置

        # 1. 检测重复词语或短语（按行）
        words = line.split()
        word_counts = {}
        for i, word in enumerate(words):
            if len(word) > 1:  # 只考虑长度>1的词
                if word in word_counts:
                    word_counts[word].append(i)
                else:
                    word_counts[word] = [i]

        for word, positions in word_counts.items():
            if len(positions) >= 2:  # 同一行内词语重复2次以上
                for pos in positions:
                    # 计算词语在该行中的位置
                    word_start_in_line = sum(len(words[j]) + 1 for j in range(pos))
                    global_start = line_start_pos + word_start_in_line
                    global_end = global_start + len(word)
                    trace_id = str(uuid.uuid4())
                    line_traces.append(TraceMark(
                        id=trace_id,
                        start=global_start,
                        end=global_end,
                        type="word_repetition",
                        reason=f"词语'{word}'在同一行内重复出现，显示AI生成特征"
                    ))

        # 2. 检测过长的句子（按行）
        if len(line.strip()) > 80:  # 行过长
            trace_id = str(uuid.uuid4())
            line_traces.append(TraceMark(
                id=trace_id,
                start=line_start_pos,
                end=line_start_pos + len(line),
                type="long_line",
                reason="行过长，可能缺乏人类自然的停顿"
            ))

        # 3. 检测过于正式的表达（按行）
        formal_patterns = [
            (r'因此[，,]', 'formal_connector'),
            (r'此外[，,]', 'formal_connector'),
            (r'综上所述[，,]', 'formal_conclusion'),
            (r'总而言之[，,]', 'formal_conclusion'),
            (r'值得注意的是[，,]', 'formal_attention'),
            (r'需要强调的是[，,]', 'formal_emphasis'),
            (r'根据以上[，,]', 'formal_reference'),
        ]

        for pattern, trace_type in formal_patterns:
            for match in re.finditer(pattern, line):
                global_start = line_start_pos + match.start()
                global_end = line_start_pos + match.end()
                trace_id = str(uuid.uuid4())
                line_traces.append(TraceMark(
                    id=trace_id,
                    start=global_start,
                    end=global_end,
                    type=trace_type,
                    reason=f"过于正式的表达：{match.group()}"
                ))

        # 4. 检测完美句式结构（按行）
        complex_patterns = [
            (r'的[^，,。！？]*的[^，,。！？]*的', 'complex_modifiers'),  # 多个"的"字结构
            (r'以及[^，,。！？]*以及', 'parallel_structure'),  # 多个"以及"
            (r'通过[^，,。！？]*从而', 'causal_chain'),  # 因果链
        ]

        for pattern, trace_type in complex_patterns:
            for match in re.finditer(pattern, line):
                global_start = line_start_pos + match.start()
                global_end = line_start_pos + match.end()
                trace_id = str(uuid.uuid4())
                line_traces.append(TraceMark(
                    id=trace_id,
                    start=global_start,
                    end=global_end,
                    type=trace_type,
                    reason=f"复杂的句式结构：{match.group()[:20]}..."
                ))

        # 对该行进行标记
        marked_line = line
        # 按位置倒序插入标记，避免位置偏移
        for trace in sorted(line_traces, key=lambda x: x.start, reverse=True):
            # 计算相对于该行的位置
            relative_start = trace.start - line_start_pos
            relative_end = trace.end - line_start_pos

            if 0 <= relative_start < len(marked_line) and 0 <= relative_end <= len(marked_line):
                before = marked_line[:relative_start]
                marked_part = marked_line[relative_start:relative_end]
                after = marked_line[relative_end:]
                marked_line = f"{before}<mark class='ai-trace {trace.type}' data-trace-id='{trace.id}' title='点击查看详情'>{marked_part}</mark>{after}"

        marked_lines.append(marked_line)
        all_traces.extend(line_traces)

    # 将标记后的行重新组合
    marked_text = '\n'.join(marked_lines)

    explanation = f"发现{len(all_traces)}个潜在的AI生成痕迹，包括重复词语、过长句子、正式表达和复杂句式等。"

    return {
        "original_text": original_text,
        "marked_text": marked_text,
        "traces": all_traces,
        "explanation": explanation
    }
