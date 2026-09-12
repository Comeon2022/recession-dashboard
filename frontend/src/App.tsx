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

function pick(indicators: Indicator[], ids: string[]) { return indicators.filter((indicator) => ids.includes(indicator.id)); }
function scoreCounts(indicators: Indicator[]) { return indicators.reduce((counts, indicator) => { if (indicator.score !== null) counts[indicator.score] += 1; return counts; }, [0, 0, 0]); }
function find(indicators: Indicator[], id: string) { return indicators.find((indicator) => indicator.id === id); }

function Group({ title, subtitle, indicators, icon }: { title: string; subtitle: string; indicators: Indicator[]; icon: string }) {
  const scored = indicators.filter((indicator) => indicator.scored);
  const score = scored.reduce((sum, indicator) => sum + (indicator.score ?? 0), 0);
  const max = scored.length * 2;
  return <section className="topic-section"><div className="topic-heading"><div className="topic-title"><span className="topic-icon">{icon}</span><div><h2>{title}</h2><p>{subtitle}</p></div></div><span className="topic-score">{scored.length ? `${score} / ${max}` : 'הקשר בלבד'}</span></div><IndicatorGrid indicators={indicators} /></section>;
}

export default function App() {
  const data = current as DashboardData;
  const labor = pick(data.indicators, laborIds);
  const housing = pick(data.indicators, housingIds);
  const rates = pick(data.indicators, ratesIds);
  const consumerInputs = ['sahm-rule', 'initial-claims', 'wage-growth', 'mortgage-delinquency', 'mortgage-debt-service'].map((id) => find(data.indicators, id)).filter(Boolean) as Indicator[];
  const counts = scoreCounts(data.indicators);
  const updated = new Date(data.generated_at).toLocaleDateString('he-IL', { day: 'numeric', month: 'long', year: 'numeric' });
  return <main dir="rtl">
    <section className="summary-hero"><div className="summary-copy"><div className="eyebrow">מוניטור מאקרו · ארצות הברית</div><h1>מדד קרבה למיתון</h1><p className="summary-subtitle">ארה״ב | תמונת מצב של שוק העבודה, הדיור והריביות</p><p className="thesis">{data.summary}</p><div className="updated">עדכון אחרון · {updated}</div></div><div className="summary-score"><span>ציון סיכון</span><strong>{data.risk_score}</strong><small>מתוך 100 · ציון גולמי {data.total_score} / {data.max_score}</small><b>{data.regime === 'Slowdown' ? 'האטה' : data.regime}</b></div></section>
    {data.data_status && data.data_status !== 'ok' && <div className="data-warning">סטטוס נתונים: {data.data_status}. {data.warnings?.[0]}</div>}
    <section className="overall-section"><div className="section-heading"><div><div className="section-kicker">תמונת מצב</div><h2>התמונה הכוללת</h2><p>הסיגנלים המרכזיים שמרכיבים את ציון הסיכון הנוכחי.</p></div><div className="status-counts"><span><i className="dot healthy" />{counts[0]} בריאים</span><span><i className="dot warning" />{counts[1]} באזהרה</span><span><i className="dot recessionary" />{counts[2]} מיתוניים</span></div></div><div className="overall-grid"><div className="gauge-card"><RecessionGauge data={data}/></div><div className="interpretation"><SummaryPanel summary={data.summary}/><ScoreLegend/><div className="category-chips">{data.categories.filter((category) => category.max_score > 0).map((category) => <span key={category.id}><b>{category.name}</b><em>{category.risk_score}</em></span>)}</div></div></div></section>
    <div className="details-kicker"><div className="section-kicker">פירוט לפי נושאים</div><h2>מה מניע את התמונה?</h2></div>
    <Group title="שוק העבודה" subtitle="תעסוקה, שכר והביקוש לעובדים" indicators={labor} icon="↗" />
    <Group title="שוק הדיור" subtitle="בנייה, מכירות ולחץ פיננסי של משקי הבית" indicators={housing} icon="⌂" />
    <Group title="שוק האג״ח / ריביות" subtitle="צורת עקום התשואות והסיכון המאקרו־פיננסי" indicators={rates} icon="≈" />
    <section className="consumer-section"><div className="topic-heading"><div className="topic-title"><span className="topic-icon">◌</span><div><h2>מצב הצרכן</h2><p>סיכום נגזר של התעסוקה, ההכנסה והלחץ על משקי הבית — ללא ספירה כפולה.</p></div></div><span className="topic-score">פרשנות</span></div><div className="consumer-grid">{consumerInputs.map((indicator) => <div className="consumer-signal" key={indicator.id}><b>{indicator.name}</b><span>{indicator.display_value}</span></div>)}<p>שוק העבודה מציג חולשה מתונה, בעוד שנתוני האשראי והדיור מוסיפים נקודות לחץ שחשוב לעקוב אחריהן. המדדים כאן נגזרים מהאינדיקטורים הקיימים ואינם מוסיפים נקודות לציון הראשי.</p></div></section>
    <footer className="site-footer">{data.data_status === 'ok' ? 'נתוני FRED חיים · נתוני מדגם ידניים' : 'מצב נתוני מדגם'} · הציונים מחושבים באופן דטרמיניסטי.<br />הנתונים מתקבלים דרך FRED / שירות הנתונים של הבנק הפדרלי של סנט לואיס. האתר אינו מזוהה, נתמך או ממומן על ידי הבנק.</footer>
  </main>;
}
