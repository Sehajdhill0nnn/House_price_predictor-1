import { useState } from 'react'
import { AlertCircle, Sparkles } from 'lucide-react'
import HouseForm from '../components/HouseForm'
import PredictionCard from '../components/PredictionCard'
import PredictionChart from '../components/PredictionChart'
import { predictHouse } from '../services/api'

export default function Prediction({ onSaved, onPrediction }) {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const submit = async (payload) => { setLoading(true); setError(''); try { const response = await predictHouse(payload); setResult(response.data); onPrediction?.(response.data.predictions); onSaved?.() } catch (err) { setError(err.response?.data?.detail || 'Could not reach the prediction service. Start the FastAPI server and train the models first.') } finally { setLoading(false) } }
  return <><header className="page-header"><div><span className="eyebrow">Prediction workspace</span><h1>House price predictor</h1><p>Compare three approaches on the same property profile.</p></div><div className="project-description"><span className="eyebrow">Project overview</span><strong>Machine learning comparison</strong><p>Linear Regression, Random Forest, and Neural Network predictions in one workspace.</p></div></header><div className="prediction-layout"><section className="surface"><HouseForm onSubmit={submit} loading={loading} /></section><aside className="results-column"><div className="results-heading"><span className="eyebrow">Live estimate</span><h2>Predicted prices</h2></div>{error && <div className="error-box"><AlertCircle size={17} />{error}</div>}{result ? <><div className="prediction-cards">{Object.entries(result.predictions).map(([model, value]) => <PredictionCard key={model} model={model} value={value} />)}</div><div className="average-card"><span>Consensus estimate</span><strong>$ {(result.average_prediction / 100000).toFixed(2)} Lakh</strong><small>Simple average across all three trained models</small></div><PredictionChart predictions={result.predictions} /></> : <div className="result-placeholder"><Sparkles size={28} /><h3>Your estimate will land here</h3><p>Fill in the property profile to see the models think in parallel.</p></div>}</aside></div></>
}
