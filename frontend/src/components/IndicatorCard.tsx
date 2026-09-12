import type { Indicator } from '../types/dashboard';

const icons: Record<string, string> = { payrolls: '▣', 'sahm-rule': '●', 'initial-claims': '▤', 'jolts-hires': '↗', 'jolts-quits': '↘', 'wage-growth': '$', 'ism-employment': '▥', 'ism-activity': '▤', lei: '⌁', 'yield-curve': '≈', 'housing-starts': '⌂', 'building-permits': '▧', 'new-home-sales': '⌂', 'months-supply': '◷', 'fhfa-home-prices': '◆', 'mortgage-rate-30y': '%', 'mortgage-delinquency': '▥', 'mortgage-debt-service': '◒' };

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  return <article className="indicator-card"><div className="card-top"><div className="card-identity"><span className="indicator-icon">{icons[indicator.id] ?? '•'}</span><span className="category">{indicator.category}</span></div><span className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{indicator.score === null ? 'Context' : `${indicator.score} · ${level}`}</span></div><h3>{indicator.name}</h3><div className="value">{indicator.display_value}</div><p>{indicator.explanation}</p><footer>{indicator.source}<span>{indicator.observation_date}</span></footer></article>;
}
