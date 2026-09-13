import type { DashboardData } from '../types/dashboard';

export function RecessionGauge({ data }: { data: DashboardData }) {
  return <div className="risk-scale" aria-label={`Cycle risk ${data.risk_score} out of 100`}><div className="risk-track"><span className="risk-marker" style={{ left: `${Math.max(0, Math.min(100, data.risk_score))}%` }} /></div><div className="risk-scale-labels"><span>Healthy</span><span>Slowdown</span><span>Recession</span></div></div>;
}
