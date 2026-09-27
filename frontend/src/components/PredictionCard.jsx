import { Award, BrainCircuit, TreePine, TrendingUp } from 'lucide-react'

const icons = { linear_regression: TrendingUp, random_forest: TreePine, neural_network: BrainCircuit }
const labels = { linear_regression: 'Linear Regression', random_forest: 'Random Forest', neural_network: 'Neural Network' }

export default function PredictionCard({ model, value, isBest = false }) {
  const Icon = icons[model]
  return <article className={`prediction-card ${model}${isBest ? ' best-model-card' : ''}`}><div className="card-icon"><Icon size={19} /></div><div><p>{labels[model]}{isBest && <span className="best-model-badge"><Award size={12} /> Best model</span>}</p><strong>{value == null ? '—' : `$ ${(value / 100000).toFixed(2)} Lakh`}</strong><small>Estimated sale price</small></div></article>
}
