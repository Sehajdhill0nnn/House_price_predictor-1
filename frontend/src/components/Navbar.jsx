import { BarChart3, Clock3, Database, Gauge, House, LineChart, Settings2, UserRound } from 'lucide-react'

export default function Navbar({ active, onNavigate }) {
  const items = [
    ['dashboard', 'Dashboard', Gauge],
    ['predict', 'Predict price', House],
    ['models', 'Model comparison', BarChart3],
    ['history', 'Prediction history', Clock3],
    ['dataset', 'Dataset', Database],
  ]
  return <aside className="sidebar">
    <div className="brand"><span className="brand-mark"><LineChart size={20} /></span><div><strong>HouseAI</strong><small>University project</small></div></div>
    <nav>{items.map(([key, label, Icon]) => <button key={key} className={active === key ? 'nav-item active' : 'nav-item'} onClick={() => onNavigate(key)}><Icon size={18} /><span>{label}</span></button>)}</nav>
    <div className="sidebar-footer"><div className="sidebar-note"><span className="status-dot" />Models ready locally<br /><small>ML + deep learning</small></div><div className="profile-row"><span className="profile-avatar"><UserRound size={15} /></span><div><strong>Project workspace</strong><small>University edition</small></div><Settings2 size={15} /></div></div>
  </aside>
}
