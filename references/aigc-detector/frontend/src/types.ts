export interface DetectResult {
  label: string;
  score: number;
  confidence: string;
  rationale: string;
  detailed_analysis: string;
  key_indicators: string[];
  methodology: string;
}

export interface DetectResponse {
  result: DetectResult;
}

export interface TraceMark {
  id: string;
  start: number;
  end: number;
  type: string;
  reason: string;
}

export interface MarkTracesResponse {
  original_text: string;
  marked_text: string;
  traces: TraceMark[];
  explanation: string;
}
