import type { Indicator } from '../types/dashboard';

const icons: Record<string, string> = { payrolls: '▣', 'sahm-rule': '●', 'initial-claims': '◈', 'jolts-hires': '↗', 'jolts-quits': '↘', 'wage-growth': '$' };

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  const role = indicator.id === 'sahm-rule' ? 'Confirmation · Context' : indicator.id === 'jolts-quits' ? 'Context' : indicator.score === null ? 'Context' : `Cycle score · ${level}`;
  const trendMetrics = (indicator as Indicator & { trend_metrics?: Record<string, string> }).trend_metrics;
  const primary = indicator.display_value.split(' | ')[0].replace(/\s*\([^)]*\)/, '');
  const primaryLabel = trendMetrics ? Object.keys(trendMetrics)[0] : 'Latest reading';
  return <article className="indicator-card"><div className="card-top"><div className="card-identity"><span className="indicator-icon">{icons[indicator.id] ?? '•'}</span></div><span className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{role}</span></div><h3>{indicator.name}</h3><div className="primary-metric"><small>{primaryLabel}</small><strong>{primary}</strong></div>{trendMetrics && <div className="trend-metrics">{Object.entries(trendMetrics).slice(1).map(([label, value]) => <span key={label}><small>{label}</small><strong>{value}</strong></span>)}</div>}<p>{indicator.explanation}</p><footer><span>{indicator.source}</span><span>{indicator.observation_date}</span></footer></article>;
}
