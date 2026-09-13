import type { Indicator } from '../types/dashboard';

type Metric = { label: string; value: string };
type CardPresentation = { primaryLabel: string; primaryValue: string; support: Metric[] };
type Comparison = { label: string; value: string };

const icons: Record<string, string> = { payrolls: '▣', 'sahm-rule': '●', 'initial-claims': '◈', 'jolts-hires': '↗', 'jolts-quits': '↘', 'wage-growth': '$' };
const primaryLabels: Record<string, string> = {
  payrolls: 'Monthly change', 'sahm-rule': 'Unemployment rate', 'initial-claims': 'Latest claims',
  'jolts-hires': 'Latest hires rate', 'jolts-quits': 'Latest quits rate', 'wage-growth': 'Latest wage growth',
};

function presentation(indicator: Indicator): CardPresentation {
  const trend = (indicator as Indicator & { trend_metrics?: Record<string, string> }).trend_metrics;
  if (trend) {
    const entries = Object.entries(trend);
    return { primaryLabel: primaryLabels[indicator.id] ?? entries[0]?.[0] ?? 'Latest reading', primaryValue: entries[0]?.[1] ?? indicator.display_value, support: entries.slice(1).map(([label, value]) => ({ label, value })) };
  }
  const parts = indicator.display_value.split('|').map((part) => part.trim()).filter(Boolean);
  const primary = parts.shift() ?? indicator.display_value;
  const support = parts.map((part, index) => {
    const match = part.match(/^([^+−-]+?)\s*([+−-]?\s*\d.*)$/);
    return match ? { label: match[1].trim(), value: match[2].trim() } : { label: `Context ${index + 1}`, value: part };
  });
  return { primaryLabel: primaryLabels[indicator.id] ?? 'Latest reading', primaryValue: primary.replace(/\s*\([^)]*\)/, ''), support };
}

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  const role = indicator.id === 'sahm-rule' ? 'Confirmation · Context' : indicator.id === 'jolts-quits' ? 'Context' : indicator.score === null ? 'Context' : `Cycle score · ${level}`;
  const card = presentation(indicator);
  const historical = (indicator as Indicator & { historical_comparison?: { today?: { display: string }; recession_2020?: { display: string }; recession_2008?: { display: string }; recession_2001?: { display: string } } }).historical_comparison;
  const comparison: Comparison[] = [
    { label: 'Today', value: historical?.today?.display ?? card.primaryValue },
    { label: '2020', value: historical?.recession_2020?.display ?? 'N/A' },
    { label: '2008', value: historical?.recession_2008?.display ?? 'N/A' },
    { label: '2001', value: historical?.recession_2001?.display ?? 'N/A' },
  ];
  return <article className="indicator-card"><div className="card-top"><div className="card-identity"><span className="indicator-icon" aria-hidden="true">{icons[indicator.id] ?? '•'}</span><span className="sr-only">{indicator.category}</span></div><span className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{role}</span></div><h3>{indicator.name}</h3><div className="primary-metric"><small>{card.primaryLabel}</small><strong>{card.primaryValue}</strong></div>{card.support.length > 0 && <div className="trend-metrics" aria-label="Supporting metrics">{card.support.map(({ label, value }) => <span key={`${label}-${value}`}><small>{label}</small><strong>{value}</strong></span>)}</div>}<div className="recession-comparison" aria-label="Historical recession comparison"><small>Historical comparison</small><div>{comparison.map(({ label, value }) => <span key={label}><b>{label}</b><strong>{value}</strong></span>)}</div></div><p className="indicator-takeaway">{indicator.explanation}</p><footer><span>{indicator.source}</span><span>{indicator.observation_date}</span></footer></article>;
}
