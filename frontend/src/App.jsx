import { useEffect, useState } from 'react'
import Navbar from './components/Navbar'
import Prediction from './pages/Prediction'
import Models from './pages/Models'
import History from './pages/History'
import Dataset from './pages/Dataset'
import ProjectAssistant from './components/ProjectAssistant'
import Dashboard from './pages/Dashboard'
import Footer from './components/Footer'
import { fetchMetrics } from './services/api'

export default function App() { const [active, setActive] = useState('dashboard'); const [metrics, setMetrics] = useState(null); const [predictions, setPredictions] = useState(null); const loadMetrics = () => fetchMetrics().then(({ data }) => setMetrics(data)).catch(() => setMetrics(null)); useEffect(() => { loadMetrics() }, []); return <div className="app-shell"><Navbar active={active} onNavigate={setActive} /><div className="app-content"><main className="main-content">{active === 'dashboard' && <Dashboard metrics={metrics} onNavigate={setActive} />}{active === 'predict' && <Prediction onSaved={loadMetrics} onPrediction={setPredictions} />}{active === 'models' && <Models metrics={metrics} />}{active === 'history' && <History />}{active === 'dataset' && <Dataset onTrained={loadMetrics} />}</main><Footer onNavigate={setActive} /></div><ProjectAssistant predictions={predictions} /></div> }
