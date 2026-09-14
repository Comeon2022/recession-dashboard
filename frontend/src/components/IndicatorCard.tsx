import type { Indicator } from '../types/dashboard';

type Metric = { label: string; value: string };
type CardPresentation = { primaryLabel: string; primaryValue: string; support: Metric[] };
type Comparison = { label: string; value: string; date: string };
type ComparisonDatum = { display: string; date?: string | null };

const icons: Record<string, string> = { payrolls: '▣', 'sahm-rule': '●', 'initial-claims': '◈', 'jolts-hires': '↗', 'jolts-quits': '↘', 'wage-growth': '$' };
const primaryLabels: Record<string, string> = { payrolls: 'Monthly change', 'sahm-rule': 'Unemployment rate', 'initial-claims': 'Latest claims', 'jolts-hires': 'Latest hires rate', 'jolts-quits': 'Latest quits rate', 'wage-growth': 'Latest wage growth' };

function presentation(indicator: Indicator): CardPresentation {
  const trend = (indicator as Indicator & { trend_metrics?: Record<string, string> }).trend_metrics;
  if (trend) { const entries = Object.entries(trend); return { primaryLabel: primaryLabels[indicator.id] ?? entries[0]?.[0] ?? 'Latest reading', primaryValue: entries[0]?.[1] ?? indicator.display_value, support: entries.slice(1).map(([label, value]) => ({ label, value })) }; }
  const parts = indicator.display_value.split('|').map((part) => part.trim()).filter(Boolean); const primary = parts.shift() ?? indicator.display_value;
  const support = parts.map((part, index) => { const match = part.match(/^([^+âˆ’-]+?)\s*([+âˆ’-]?\s*\d.*)$/); return match ? { label: match[1].trim(), value: match[2].trim() } : { label: `Context ${index + 1}`, value: part }; });
  return { primaryLabel: primaryLabels[indicator.id] ?? 'Latest reading', primaryValue: primary.replace(/\s*\([^)]*\)/, ''), support };
}

export function IndicatorCard({ indicator }: { indicator: Indicator }) {
  const level = indicator.score === null ? 'Context' : ['Healthy', 'Warning', 'Recessionary'][indicator.score];
  const role = indicator.id === 'sahm-rule' ? 'Confirmation · Context' : indicator.id === 'jolts-quits' ? 'Not scored' : indicator.score === null ? 'Not scored' : `Cycle score · ${level}`;
  const roleTitle = role === 'Not scored' ? 'Shown for context only. Not included in the main Cycle Risk score.' : role;
  const card = presentation(indicator);
  const historical = (indicator as Indicator & { historical_comparison?: { today?: ComparisonDatum; recession_2020?: ComparisonDatum; recession_2008?: ComparisonDatum; recession_2001?: ComparisonDatum } }).historical_comparison;
  const formatMonthYear = (date?: string | null) => date ? new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${date}T00:00:00Z`)) : '—';
  const historicalCell = (label: string, datum: ComparisonDatum | undefined, fallback: string): Comparison => ({ label, value: datum?.display ?? fallback, date: datum?.display === 'N/A' ? '—' : formatMonthYear(datum?.date) });
  const comparison = [historicalCell('Today', historical?.today, card.primaryValue), historicalCell('2020', historical?.recession_2020, 'N/A'), historicalCell('2008', historical?.recession_2008, 'N/A'), historicalCell('2001', historical?.recession_2001, 'N/A')];
  return <article className="indicator-card"><div className="card-top"><div className="card-identity"><span className="indicator-icon" aria-hidden="true">{icons[indicator.id] ?? '•'}</span><span className="sr-only">{indicator.category}</span></div><span title={roleTitle} aria-label={roleTitle} className={`badge ${indicator.score === null ? 'context' : `score-${indicator.score}`}`}>{role}</span></div><h3>{indicator.name}</h3><div className="primary-metric"><small>{card.primaryLabel}</small><strong>{card.primaryValue}</strong></div>{card.support.length > 0 && <div className="trend-metrics" aria-label="Supporting metrics">{card.support.map(({ label, value }) => <span key={`${label}-${value}`}><small>{label}</small><strong>{value}</strong></span>)}</div>}<div className="recession-comparison" aria-label="Historical recession comparison"><small>Historical comparison</small><div>{comparison.map(({ label, value, date }) => <span key={label}><b>{label}</b><strong>{value}</strong><em>{date}</em></span>)}</div></div><p className="indicator-takeaway">{indicator.explanation}</p><footer><span>{indicator.source}</span><span>{indicator.observation_date}</span></footer></article>;
}
