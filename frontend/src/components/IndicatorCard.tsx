import type { Indicator } from '../types/dashboard';

const icons: Record<string, string> = { payrolls: '▣', 'sahm-rule': '●', 'initial-claims': '◈', 'jolts-hires': '↗', 'jolts-quits': '↘', 'wage-growth': '$' };

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  const role = indicator.id === 'sahm-rule' ? 'Confirmation · Context' : indicator.id === 'jolts-quits' ? 'Context' : indicator.score === null ? 'Context' : `Cycle score · ${level}`;
  const trendMetrics = (indicator as Indicator & { trend_metrics?: Record<string, string> }).trend_metrics;
  return <article className="indicator-card"><div className="card-top"><div className="card-identity"><span className="indicator-icon">{icons[indicator.id] ?? '•'}</span><span className="category">{indicator.category}</span></div><span className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{role}</span></div><h3>{indicator.name}</h3><div className="value">{indicator.display_value}</div>{trendMetrics && <div className="trend-metrics">{Object.entries(trendMetrics).map(([label, value]) => <span key={label}><small>{label}</small><strong>{value}</strong></span>)}</div>}<p>{indicator.explanation}</p><footer>{indicator.source}<span>{indicator.observation_date}</span></footer></article>;
}
