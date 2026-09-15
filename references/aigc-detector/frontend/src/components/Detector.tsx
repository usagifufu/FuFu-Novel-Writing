import { useState, useEffect } from 'react';
import { Button, Input, Card, Alert, Progress, Typography, Divider, Tag, Modal, Grid } from 'antd';
import axios from 'axios';
import { DetectResult, MarkTracesResponse } from '../types';

const { TextArea } = Input;
const { Title, Text } = Typography;
const { useBreakpoint } = Grid;

// 添加样式
const styles = `
  .ai-trace {
    background-color: #fff2e8;
    border: 1px solid #ffbb96;
    border-radius: 3px;
    padding: 2px 4px;
    margin: 0 1px;
    cursor: pointer;
    transition: all 0.2s;
    white-space: pre-wrap;
    word-wrap: break-word;
    user-select: none;
  }
  .ai-trace:hover {
    background-color: #ffd591;
    border-color: #ff9c6e;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .ai-trace:active {
    background-color: #ffb366;
    transform: scale(0.98);
  }
  .ai-trace.word_repetition {
    background-color: #f6ffed;
    border-color: #b7eb8f;
  }
  .ai-trace.word_repetition:hover {
    background-color: #d9f7be;
  }
  .ai-trace.long_line {
    background-color: #fff1f0;
    border-color: #ffccc7;
  }
  .ai-trace.long_line:hover {
    background-color: #ffccc7;
  }
  .ai-trace.formal_connector,
  .ai-trace.formal_conclusion,
  .ai-trace.formal_attention,
  .ai-trace.formal_emphasis,
  .ai-trace.formal_reference {
    background-color: #f9f0ff;
    border-color: #d3adf7;
  }
  .ai-trace.formal_connector:hover,
  .ai-trace.formal_conclusion:hover,
  .ai-trace.formal_attention:hover,
  .ai-trace.formal_emphasis:hover,
  .ai-trace.formal_reference:hover {
    background-color: #efdbff;
  }
  .marked-text-container {
    white-space: pre-wrap;
    word-wrap: break-word;
    line-height: 1.6;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  }

  @media (max-width: 768px) {
    .ai-trace {
      padding: 1px 3px;
      margin: 0 1px;
      font-size: 13px;
    }

    .marked-text-container {
      font-size: 14px;
      line-height: 1.5;
    }
  }

  @media (max-width: 480px) {
    .ai-trace {
      padding: 1px 2px;
      font-size: 12px;
    }

    .marked-text-container {
      font-size: 13px;
      line-height: 1.4;
    }
  }
`;

export default function Detector() {
  const screens = useBreakpoint();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DetectResult | null>(null);
  const [markedResult, setMarkedResult] = useState<MarkTracesResponse | null>(null);
  const [error, setError] = useState('');
  const [selectedTrace, setSelectedTrace] = useState<{trace: any, visible: boolean} | null>(null);

  useEffect(() => {
    // 注入样式
    const styleElement = document.createElement('style');
    styleElement.textContent = styles;
    document.head.appendChild(styleElement);

    // 添加点击事件监听器
    const handleTraceClick = (event: Event) => {
      const target = event.target as HTMLElement;
      if (target.classList.contains('ai-trace') && markedResult) {
        const traceId = target.getAttribute('data-trace-id');
        if (traceId) {
          const trace = markedResult.traces.find(t => t.id === traceId);
          if (trace) {
            setSelectedTrace({ trace, visible: true });
          }
        }
      }
    };

    document.addEventListener('click', handleTraceClick);

    return () => {
      document.head.removeChild(styleElement);
      document.removeEventListener('click', handleTraceClick);
    };
  }, [markedResult]);

  const onDetect = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    setMarkedResult(null);
    try {
      const resp = await axios.post('/api/detect', { text });
      setResult(resp.data.result);
      // 自动标记AI痕迹
      await onMarkTraces();
    } catch (e: any) {
      setError(e?.response?.data?.detail || '请求失败');
    } finally {
      setLoading(false);
    }
  };

  const onMarkTraces = async () => {
    if (!text.trim()) return;

    try {
      const resp = await axios.post('/api/mark-traces', { text });
      setMarkedResult(resp.data);
    } catch (e: any) {
      console.error('标记AI痕迹失败:', e);
      // 不显示错误，因为这不是主要功能
    }
  };

  const getLabelColor = (label: string) => {
    switch (label) {
      case 'human':
        return '#52c41a';
      case 'ai':
        return '#ff4d4f';
      case 'uncertain':
        return '#faad14';
      default:
        return '#d9d9d9';
    }
  };

  const getLabelText = (label: string) => {
    switch (label) {
      case 'human':
        return '人类';
      case 'ai':
        return 'AI';
      case 'uncertain':
        return '不确定';
      default:
        return '未知';
    }
  };

  const getTraceTypeName = (type: string) => {
    const typeMap: { [key: string]: string } = {
      'word_repetition': '词语重复',
      'long_line': '过长行',
      'formal_connector': '正式连接词',
      'formal_conclusion': '正式结论词',
      'formal_attention': '正式强调词',
      'formal_emphasis': '正式强调',
      'formal_reference': '正式引用',
      'complex_modifiers': '复杂修饰',
      'parallel_structure': '平行结构',
      'causal_chain': '因果链'
    };
    return typeMap[type] || type;
  };

  const getConfidenceText = (confidence: string) => {
    const confidenceMap: { [key: string]: string } = {
      'high': '高',
      'medium': '中',
      'low': '低'
    };
    return confidenceMap[confidence] || confidence;
  };

  const getConfidenceColor = (confidence: string) => {
    const colorMap: { [key: string]: string } = {
      'high': 'green',
      'medium': 'orange',
      'low': 'red'
    };
    return colorMap[confidence] || 'default';
  };

  const handleModalClose = () => {
    setSelectedTrace(null);
  };

  const getTraceDetail = (trace: any) => {
    const details: { [key: string]: string } = {
      'word_repetition': '人类写作时通常会使用不同的词汇来表达相同概念，避免重复使用相同的词语。AI模型有时会重复使用相同的词语，因为它们倾向于使用训练数据中最常见的表达。',
      'long_line': '人类写作通常会自然地分段和换行，避免过长的行。过长的行可能表示AI模型一次性生成了大量内容，没有考虑可读性。',
      'formal_connector': '正式连接词如"因此"、"此外"等通常出现在正式文档或学术写作中。AI模型经常使用这些词语来构建逻辑关系，但人类日常写作可能更随意。',
      'formal_conclusion': '正式结论词如"综上所述"、"总而言之"等是典型的学术或正式写作特征。AI模型常用这些词语来结束段落。',
      'formal_attention': '正式强调词如"值得注意的是"、"需要强调的是"等显示出正式写作风格。AI模型常用这些表达来吸引注意力。',
      'formal_emphasis': '强调性表达通常用于正式场合。AI模型可能过度使用这些表达来增强文本的说服力。',
      'formal_reference': '引用性表达如"根据以上"等显示出逻辑推理的特征。AI模型常用这些词语来建立论证关系。',
      'complex_modifiers': '多个定语修饰（如"的"字结构）是典型的中文正式写作特征。AI模型常使用这种结构来精确表达概念。',
      'parallel_structure': '平行结构（如重复使用"以及"）显示出对称性写作风格。AI模型常用这种结构来保持文本平衡。',
      'causal_chain': '因果链结构（如"通过...从而"）显示出逻辑推理特征。AI模型常用这种结构来解释因果关系。'
    };
    return details[trace.type] || '该痕迹类型显示出典型的AI生成特征，通常在人类自然写作中较少出现。';
  };

  return (
    <Card title="文本检测">
      <TextArea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={screens.xs ? 8 : screens.sm ? 9 : 10}
        placeholder="请输入要检测的文本..."
        style={{
          marginBottom: 16,
          fontSize: screens.xs ? '14px' : '16px'
        }}
      />
      <Button
        type="primary"
        onClick={onDetect}
        loading={loading}
        disabled={!text.trim()}
        block
        size={screens.xs ? 'middle' : 'large'}
        style={{
          fontSize: screens.xs ? '14px' : '16px',
          height: screens.xs ? '40px' : 'auto'
        }}
      >
        {loading ? '检测中...' : '开始检测'}
      </Button>
      {error && (
        <Alert
          message="错误"
          description={error}
          type="error"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}
      {result && (
        <Card
          style={{ marginTop: 16 }}
          bordered={false}
          styles={{ body: { padding: '16px' } }}
        >
          <Title level={4}>检测结果</Title>

          {/* 基本结果 */}
          <div style={{
            display: 'flex',
            flexDirection: screens.xs ? 'column' : 'row',
            alignItems: screens.xs ? 'stretch' : 'center',
            gap: screens.xs ? '12px' : '16px',
            marginBottom: '16px'
          }}>
            <div>
              <Text strong style={{
                color: getLabelColor(result.label),
                fontSize: screens.xs ? '14px' : '16px'
              }}>
                标签: {getLabelText(result.label)}
              </Text>
            </div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              flexWrap: 'wrap'
            }}>
              <Text style={{ fontSize: screens.xs ? '14px' : '16px' }}>置信度: </Text>
              <Progress
                percent={result.score * 100}
                status="active"
                showInfo={false}
                strokeColor={getLabelColor(result.label)}
                style={{
                  width: screens.xs ? '100px' : '120px',
                  marginRight: '8px'
                }}
              />
              <Text style={{ fontSize: screens.xs ? '14px' : '16px' }}>
                {(result.score * 100).toFixed(1)}%
              </Text>
            </div>
            <div>
              <Text style={{ fontSize: screens.xs ? '14px' : '16px' }}>判断置信度: </Text>
              <Tag
                color={getConfidenceColor(result.confidence)}
                style={{ fontSize: screens.xs ? '12px' : '14px' }}
              >
                {getConfidenceText(result.confidence)}
              </Tag>
            </div>
          </div>

          {/* 简要解释 */}
          <div style={{ marginBottom: '16px' }}>
            <Text strong>判断理由: </Text>
            <Text>{result.rationale}</Text>
          </div>

          {/* 详细分析 */}
          {result.detailed_analysis && (
            <div style={{ marginBottom: '16px' }}>
              <Text strong>详细分析: </Text>
              <div style={{
                backgroundColor: '#f9f9f9',
                padding: '12px',
                borderRadius: '4px',
                marginTop: '8px',
                whiteSpace: 'pre-wrap',
                lineHeight: '1.6'
              }}>
                {result.detailed_analysis}
              </div>
            </div>
          )}

          {/* 关键指标 */}
          {result.key_indicators && result.key_indicators.length > 0 && (
            <div style={{ marginBottom: '16px' }}>
              <Text strong>关键指标: </Text>
              <div style={{ marginTop: '8px' }}>
                {result.key_indicators.map((indicator, index) => (
                  <Tag key={index} style={{ marginBottom: '4px', marginRight: '8px' }}>
                    {indicator}
                  </Tag>
                ))}
              </div>
            </div>
          )}

          {/* 判断方法 */}
          {result.methodology && (
            <div>
              <Text strong>判断方法: </Text>
              <div style={{
                backgroundColor: '#f0f8ff',
                padding: '8px 12px',
                borderRadius: '4px',
                marginTop: '4px',
                fontSize: '12px',
                color: '#666'
              }}>
                {result.methodology}
              </div>
            </div>
          )}

          {markedResult && (
            <>
              <Divider />
              <Title level={5}>AI痕迹标记</Title>
              <div
                className="marked-text-container"
                dangerouslySetInnerHTML={{
                  __html: markedResult.marked_text
                }}
                style={{
                  padding: '12px',
                  backgroundColor: '#f9f9f9',
                  borderRadius: '4px',
                  fontSize: '14px',
                  border: '1px solid #e8e8e8',
                  minHeight: '100px'
                }}
              />
              <div style={{ marginTop: '12px' }}>
                <Text type="secondary">{markedResult.explanation}</Text>
              </div>
              {markedResult.traces.length > 0 && (
                <div style={{ marginTop: '12px' }}>
                  <Text strong>发现的痕迹类型：</Text>
                  <div style={{ marginTop: '8px' }}>
                    {Array.from(new Set(markedResult.traces.map(t => t.type))).map(type => (
                      <Tag key={type} color="orange" style={{ marginRight: '8px', marginBottom: '4px' }}>
                        {getTraceTypeName(type)}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </Card>
      )}

      {/* AI痕迹详情弹窗 */}
      <Modal
        title="AI生成痕迹详情"
        open={selectedTrace?.visible || false}
        onCancel={handleModalClose}
        footer={[
          <Button key="close" onClick={handleModalClose} size={screens.xs ? 'middle' : 'large'}>
            关闭
          </Button>
        ]}
        width={screens.xs ? '95%' : screens.sm ? '80%' : 600}
        style={{ top: screens.xs ? 20 : 100 }}
        bodyStyle={{
          maxHeight: screens.xs ? '60vh' : '70vh',
          overflow: 'auto'
        }}
      >
        {selectedTrace?.trace && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <Text strong style={{ fontSize: screens.xs ? '14px' : '16px' }}>痕迹类型：</Text>
              <Tag
                color="orange"
                style={{
                  marginLeft: 8,
                  fontSize: screens.xs ? '12px' : '14px'
                }}
              >
                {getTraceTypeName(selectedTrace.trace.type)}
              </Tag>
            </div>

            <div style={{ marginBottom: 16 }}>
              <Text strong style={{ fontSize: screens.xs ? '14px' : '16px' }}>识别内容：</Text>
              <div style={{
                backgroundColor: '#f5f5f5',
                padding: screens.xs ? '6px 8px' : '8px 12px',
                borderRadius: '4px',
                marginTop: '4px',
                fontFamily: 'monospace',
                fontSize: screens.xs ? '12px' : '14px',
                wordBreak: 'break-word'
              }}>
                {markedResult?.original_text.substring(selectedTrace.trace.start, selectedTrace.trace.end)}
              </div>
            </div>

            <div style={{ marginBottom: 16 }}>
              <Text strong style={{ fontSize: screens.xs ? '14px' : '16px' }}>判定原因：</Text>
              <div style={{
                marginTop: '4px',
                color: '#666',
                fontSize: screens.xs ? '13px' : '14px',
                lineHeight: '1.5'
              }}>
                {selectedTrace.trace.reason}
              </div>
            </div>

            <div>
              <Text strong style={{ fontSize: screens.xs ? '14px' : '16px' }}>详细解释：</Text>
              <div style={{
                marginTop: '8px',
                lineHeight: '1.6',
                fontSize: screens.xs ? '13px' : '14px'
              }}>
                {getTraceDetail(selectedTrace.trace)}
              </div>
            </div>
          </div>
        )}
      </Modal>
    </Card>
  );
}
