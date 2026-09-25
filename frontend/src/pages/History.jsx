import { useEffect, useState } from 'react'
import { fetchHistory, deleteHistory } from '../services/api'
import PredictionHistory from '../components/PredictionHistory'

export default function History() { const [records, setRecords] = useState([]); const [error, setError] = useState(''); const load = () => fetchHistory().then(({ data }) => setRecords(data)).catch(() => setError('History is unavailable. Check that the backend is running.')); useEffect(() => { load() }, []); const remove = (id) => deleteHistory(id).then(load); return <><header className="page-header"><div><span className="eyebrow">Saved estimates</span><h1>Prediction history</h1><p>Click the arrow beside any prediction to view its property inputs and model prices.</p></div></header><section className="surface history-surface">{error && <div className="error-box">{error}</div>}<PredictionHistory records={records} onDelete={remove} /></section></> }
