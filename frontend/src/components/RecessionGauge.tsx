import type { DashboardData } from '../types/dashboard';

export function RecessionGauge({ data }: { data: DashboardData }) {
  const rotation = -90 + (data.risk_score / 100) * 180;
  return <div className="gauge-wrap"><div className="gauge" style={{ '--needle': `${rotation}deg` } as React.CSSProperties}><div className="gauge-needle" /></div><div className="gauge-labels"><span>Healthy</span><span>Slowdown</span><span>Recession</span></div><div className="score"><strong>{data.risk_score}</strong><span> / 100</span></div><div className="regime">{data.regime}</div><small>Raw score {data.total_score} / {data.max_score}</small></div>;
}
