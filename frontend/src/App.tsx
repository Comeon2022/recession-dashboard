import current from './data/current.json';
import type { DashboardData, Indicator } from './types/dashboard';
import { RecessionGauge } from './components/RecessionGauge';
import { SummaryPanel } from './components/SummaryPanel';
import { ScoreLegend } from './components/ScoreLegend';
import { IndicatorGrid } from './components/IndicatorGrid';
import './styles/dashboard.css';

const laborIds = ['payrolls', 'sahm-rule', 'initial-claims', 'jolts-hires', 'jolts-quits', 'wage-growth'];
const housingIds = ['housing-starts', 'building-permits', 'new-home-sales', 'months-supply', 'fhfa-home-prices', 'mortgage-rate-30y', 'mortgage-delinquency', 'mortgage-debt-service'];
const ratesIds = ['yield-curve'];
const fragilityIds = ['vix', 'financial-stress', 'credit-conditions', 'margin-debt-gdp'];
function pick(indicators: Indicator[], ids: string[]) { return indicators.filter((indicator) => ids.includes(indicator.id)); }
function find(indicators: Indicator[], id: string) { return indicators.find((indicator) => indicator.id === id); }
function scoreCounts(indicators: Indicator[]) { return indicators.reduce((counts, indicator) => { if (indicator.score !== null) counts[indicator.score] += 1; return counts; }, [0, 0, 0]); }

function Group({ title, subtitle, indicators, icon }: { title: string; subtitle: string; indicators: Indicator[]; icon: string }) {
  const scored = indicators.filter((indicator) => indicator.scored);
  const score = scored.reduce((sum, indicator) => sum + (indicator.score ?? 0), 0);
  const curve = indicators[0]?.yield_curve_regime;
  return <section className="topic-section"><div className="topic-heading"><div className="topic-title"><span className="topic-icon">{icon}</span><div><h2>{title}</h2><p>{subtitle}</p></div></div><span className="topic-score">{scored.length ? `${score} / ${scored.length * 2}` : 'Context only'}</span></div>{curve && <div className="curve-regime"><b>Curve regime</b><span>{curve.curve_phase.replace(/_/g, ' ')}</span><span>{curve.steepening_type.replace(/_/g, ' ')}</span><small>2s10s {curve.spread_2s10s_bp > 0 ? '+' : ''}{curve.spread_2s10s_bp} bp · 3m10y {curve.spread_3m10y_bp} bp · {curve.months_since_uninversion ?? '—'} months since un-inversion</small></div>}<IndicatorGrid indicators={indicators} /></section>;
}

export default function App() {
  const data = current as DashboardData;
  const labor = pick(data.indicators, laborIds), housing = pick(data.indicators, housingIds), rates = pick(data.indicators, ratesIds), fragility = pick(data.indicators, fragilityIds);
  const consumerInputs = ['sahm-rule', 'initial-claims', 'wage-growth', 'mortgage-delinquency', 'mortgage-debt-service'].map((id) => find(data.indicators, id)).filter(Boolean) as Indicator[];
  const counts = scoreCounts(data.indicators);
  const updated = new Date(data.generated_at).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' });
  return <main>
    <section className="summary-hero"><div className="summary-copy"><div className="eyebrow">MACRO MONITOR · UNITED STATES</div><h1>Recession Risk Index</h1><p className="summary-subtitle">United States | September 2026</p><p className="thesis">Labor conditions are cooling, but the economy is not yet confirming a full recession regime.</p><div className="updated">Last updated · {updated}</div></div><div className="summary-score"><span>Risk score</span><strong>{data.risk_score}</strong><small>Normalized / 100 · Raw score {data.total_score} / {data.max_score}</small><b>{data.regime}</b></div></section>
    {data.data_status && data.data_status !== 'ok' && <div className="data-warning">Data status: {data.data_status}. {data.warnings?.[0]}</div>}
    <section className="overall-section"><div className="section-heading"><div><div className="section-kicker">OVERALL PICTURE</div><h2>The current macro picture</h2><p>Signals are softening, but the dashboard remains in a slowdown rather than recession regime.</p></div><div className="status-counts"><span><i className="dot healthy" />{counts[0]} Healthy</span><span><i className="dot warning" />{counts[1]} Warning</span><span><i className="dot recessionary" />{counts[2]} Recessionary</span></div></div><div className="overall-grid"><div className="gauge-card"><RecessionGauge data={data}/></div><div className="interpretation"><SummaryPanel summary={data.summary}/><ScoreLegend/><div className="category-chips">{data.categories.filter((category) => category.max_score > 0).map((category) => <span key={category.id}><b>{category.name}</b><em>{category.risk_score}</em></span>)}</div></div></div></section>
    <div className="details-kicker"><div className="section-kicker">SIGNAL BREAKDOWN</div><h2>What is driving the picture?</h2></div>
    <Group title="Labor Market" subtitle="Employment, wages, and the demand for workers" indicators={labor} icon="↗" />
    <Group title="Housing Market" subtitle="Construction, sales, and household financing pressure" indicators={housing} icon="⌂" />
    <Group title="Bond Market / Rates" subtitle="The yield curve and macro-financial risk" indicators={rates} icon="≈" />
    <section className="fragility-section"><div className="topic-heading"><div className="topic-title"><span className="topic-icon">◌</span><div><h2>Market Fragility / Stress</h2><p>Public volatility, financial stress, credit conditions, and leverage context.</p></div></div><span className="topic-score">Context only</span></div><IndicatorGrid indicators={fragility} /></section>
    <section className="consumer-section"><div className="topic-heading"><div className="topic-title"><span className="topic-icon">◌</span><div><h2>Consumer Condition</h2><p>A derived reading of employment, income, and household credit pressure.</p></div></div><span className="topic-score">Interpretation</span></div><div className="consumer-grid">{consumerInputs.map((indicator) => <div className="consumer-signal" key={indicator.id}><b>{indicator.name}</b><span>{indicator.display_value}</span></div>)}<p>The consumer is weakening at the margin, but broad stress remains limited. This panel summarizes existing indicators and does not add points to the main score.</p></div></section>
    <footer className="site-footer">{data.data_status === 'ok' ? 'Live FRED + manual sample data' : 'Sample data mode'} · Deterministic, rule-based scores.<br />Data obtained through the FRED API / Federal Reserve Bank of St. Louis data service. This dashboard is not affiliated with, endorsed by, or sponsored by the Federal Reserve Bank of St. Louis.</footer>
  </main>;
}
