import type { Indicator } from '../types/dashboard';

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  return <article className="indicator-card"><div className="card-top"><span className="category">{indicator.category}</span><span className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{indicator.score === null ? 'Context' : `${indicator.score} · ${level}`}</span></div><h3>{indicator.name}</h3><div className="value">{indicator.display_value}</div><p>{indicator.explanation}</p><footer>{indicator.source}<span>{indicator.observation_date}</span></footer></article>;
}
