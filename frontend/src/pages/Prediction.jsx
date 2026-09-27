import { useEffect, useState } from 'react'
import { AlertCircle, ChevronDown, ChevronUp, Sparkles } from 'lucide-react'
import HouseForm from '../components/HouseForm'
import PredictionCard from '../components/PredictionCard'
import PredictionChart from '../components/PredictionChart'
import { fetchMetrics, predictHouse } from '../services/api'

export default function Prediction({ onSaved, onPrediction }) {
  const [result, setResult] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [showOtherModels, setShowOtherModels] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  useEffect(() => {
    fetchMetrics().then(({ data }) => setMetrics(data)).catch(() => setMetrics(null))
  }, [])

  const submit = async (payload) => {
    setLoading(true)
    setError('')
    setShowOtherModels(false)
    try {
      const response = await predictHouse(payload)
      setResult(response.data)
      onPrediction?.(response.data.predictions)
      onSaved?.()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not reach the prediction service. Start the FastAPI server and train the models first.')
    } finally {
      setLoading(false)
    }
  }

  const predictionModels = result ? Object.keys(result.predictions) : []
  const bestModel = result
    ? metrics?.models
      ? predictionModels.sort((a, b) => (metrics.models[a]?.mae ?? Infinity) - (metrics.models[b]?.mae ?? Infinity))[0]
      : predictionModels.includes('random_forest') ? 'random_forest' : predictionModels[0]
    : null
  const prices = result ? Object.values(result.predictions) : []
  const estimateRange = prices.length ? [Math.min(...prices), Math.max(...prices)] : null
  const bestMetrics = bestModel ? metrics?.models?.[bestModel] : null

  return <>
    <header className="page-header">
      <div><span className="eyebrow">Prediction workspace</span><h1>House price predictor</h1><p>Compare three approaches on the same property profile.</p></div>
      <div className="project-description"><span className="eyebrow">Project overview</span><strong>Machine learning comparison</strong><p>Linear Regression, Random Forest, and Neural Network predictions in one workspace.</p></div>
    </header>
    <div className="prediction-layout">
      <section className="surface"><HouseForm onSubmit={submit} loading={loading} /></section>
      <aside className="results-column">
        <div className="results-heading"><span className="eyebrow">Live estimate</span><h2>Predicted price</h2></div>
        {error && <div className="error-box"><AlertCircle size={17} />{error}</div>}
        {result ? <div className="prediction-results">
          <div className="prediction-cards"><PredictionCard model={bestModel} value={result.predictions[bestModel]} isBest /></div>
          <section className="estimate-details" aria-label="Estimate details">
            <div className="estimate-details-heading"><strong>Estimate details</strong><span>More context for this prediction</span></div>
            <div className="estimate-detail-grid">
              <article><span>Model range</span><strong>{estimateRange ? `$ ${(estimateRange[0] / 100000).toFixed(2)}–${(estimateRange[1] / 100000).toFixed(2)} Lakh` : '—'}</strong></article>
              <article><span>Validation MAE</span><strong>{bestMetrics ? `$ ${bestMetrics.mae.toLocaleString('en-US', { maximumFractionDigits: 0 })}` : '—'}</strong></article>
              <article><span>Validation R²</span><strong>{bestMetrics ? `${(bestMetrics.r2 * 100).toFixed(1)}%` : '—'}</strong></article>
            </div>
            <p>The model is selected by its lowest error on a held-out test set. Validation scores describe past test performance, not a guarantee for this property.</p>
          </section>
          <button className="other-models-toggle" type="button" aria-expanded={showOtherModels} onClick={() => setShowOtherModels((visible) => !visible)}>{showOtherModels ? <>Hide other models <ChevronUp size={15} /></> : <>See other model estimates <ChevronDown size={15} /></>}</button>
          {showOtherModels && <><div className="other-model-cards">{Object.entries(result.predictions).filter(([model]) => model !== bestModel).map(([model, value]) => <PredictionCard key={model} model={model} value={value} />)}</div><PredictionChart predictions={result.predictions} /></>}
        </div> : <div className="result-placeholder"><Sparkles size={28} /><h3>Your estimate will land here</h3><p>Fill in the property profile to see the models think in parallel.</p></div>}
      </aside>
    </div>
  </>
}
