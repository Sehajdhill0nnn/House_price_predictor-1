import { useState } from 'react'
import { ChevronDown, ChevronUp, Trash2 } from 'lucide-react'

const featureLabels = {
  overall_qual: 'Overall quality', gr_liv_area: 'Living area', garage_cars: 'Garage capacity', garage_area: 'Garage area',
  total_bsmt_sf: 'Basement area', first_flr_sf: 'First-floor area', second_flr_sf: 'Second-floor area', full_bath: 'Bathrooms',
  bedroom_abv_gr: 'Bedrooms', tot_rms_abv_grd: 'Total rooms', year_built: 'Year built', year_remod_add: 'Year remodeled',
  lot_area: 'Lot area', neighborhood: 'Neighborhood', kitchen_qual: 'Kitchen quality', exter_qual: 'Exterior quality',
  bsmt_qual: 'Basement quality', garage_type: 'Garage type', heating: 'Heating', central_air: 'Central air',
}

const formatFeature = (key, value) => {
  if (['gr_liv_area', 'garage_area', 'total_bsmt_sf', 'first_flr_sf', 'second_flr_sf', 'lot_area'].includes(key)) return `${Number(value).toLocaleString()} sq ft`
  if (key === 'garage_cars') return `${value} cars`
  return value
}

export default function PredictionHistory({ records, onDelete }) {
  const [expandedId, setExpandedId] = useState(null)
  if (!records.length) return <div className="empty-state">No saved predictions yet. Your recent estimates will appear here.</div>
  return <div className="history-list">{records.map((record) => { const expanded = expandedId === record.id; return <div className={`history-item ${expanded ? 'expanded' : ''}`} key={record.id}><div className="history-row"><div><strong>#{String(record.id).padStart(3, '0')}</strong><span>{new Date(record.created_at).toLocaleString()}</span></div><div className="history-price"><strong>$ {(record.average_prediction / 100000).toFixed(2)} Lakh</strong><button className="price-view-button" type="button" onClick={() => setExpandedId(expanded ? null : record.id)} aria-label={expanded ? 'Hide price details' : 'View price details'}>{expanded ? 'Hide' : 'View'}</button></div><div className="history-actions"><button className="details-button" type="button" title={expanded ? 'Hide prediction details' : 'View prediction details'} aria-label={expanded ? 'Hide prediction details' : 'View prediction details'} onClick={() => setExpandedId(expanded ? null : record.id)}>{expanded ? <ChevronUp size={15} /> : <ChevronDown size={15} />}<span>{expanded ? 'Hide details' : 'View details'}</span></button><button type="button" title="Delete prediction" aria-label="Delete prediction" onClick={() => onDelete(record.id)}><Trash2 size={16} /></button></div></div>{expanded && <div className="history-details"><div className="history-model-results"><strong>Model predictions</strong><span>Linear Regression: $ {record.predictions.linear_regression.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span><span>Random Forest: $ {record.predictions.random_forest.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span><span>Neural Network: $ {record.predictions.neural_network.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span></div><div className="history-feature-grid"><strong>Property details</strong>{Object.entries(record.house_features).map(([key, value]) => <span key={key}><b>{featureLabels[key] || key}</b>{formatFeature(key, value)}</span>)}</div></div>}</div> })}</div>
}
