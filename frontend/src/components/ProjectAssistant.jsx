import { useRef, useState } from 'react'
import { Bot, MessageCircle, RotateCcw, Send, X } from 'lucide-react'
import api, { predictHouse } from '../services/api'

const predictSuggestion = 'Predict a house price'
const bestModelSuggestion = 'Which model is best?'
const welcome = { role: 'assistant', text: 'Hi. I can explain your models, metrics, graphs, dataset upload, APIs, and latest prediction results.', suggestions: [predictSuggestion, bestModelSuggestion, 'What is this project about?', 'Explain the preprocessing', 'How should I present this in a viva?', 'How do I upload a dataset?'] }
const defaultProperty = { overall_qual: 7, gr_liv_area: 1800, garage_cars: 2, garage_area: 500, total_bsmt_sf: 900, first_flr_sf: 1000, second_flr_sf: 800, full_bath: 2, bedroom_abv_gr: 3, tot_rms_abv_grd: 7, year_built: 2005, year_remod_add: 2010, lot_area: 9000, neighborhood: 'NAmes', kitchen_qual: 'Gd', exter_qual: 'Gd', bsmt_qual: 'Gd', garage_type: 'Attchd', heating: 'GasA', central_air: 'Y' }
const predictionFields = [['overall_qual', 'Quality', 'number', 1, 10], ['gr_liv_area', 'Living area', 'number', 1], ['garage_cars', 'Garage cars', 'number', 0], ['garage_area', 'Garage area', 'number', 0], ['total_bsmt_sf', 'Basement area', 'number', 0], ['first_flr_sf', 'First-floor area', 'number', 1], ['second_flr_sf', 'Second-floor area', 'number', 0], ['full_bath', 'Bathrooms', 'number', 0], ['bedroom_abv_gr', 'Bedrooms', 'number', 0], ['tot_rms_abv_grd', 'Total rooms', 'number', 1], ['year_built', 'Year built', 'number', 1800, 2026], ['year_remod_add', 'Year remodeled', 'number', 1800, 2026], ['lot_area', 'Lot area', 'number', 1]]
const predictionSelects = [['neighborhood', 'Neighborhood', ['NAmes', 'CollgCr', 'OldTown', 'Somerst', 'Gilbert']], ['kitchen_qual', 'Kitchen quality', ['Ex', 'Gd', 'TA', 'Fa', 'Po']], ['exter_qual', 'Exterior quality', ['Ex', 'Gd', 'TA', 'Fa', 'Po']], ['bsmt_qual', 'Basement quality', ['Ex', 'Gd', 'TA', 'Fa', 'Po', 'None']], ['garage_type', 'Garage type', ['Attchd', 'Detchd', 'BuiltIn', 'CarPort', 'Basment', '2Types', 'None']], ['heating', 'Heating', ['GasA', 'GasW', 'Grav', 'Wall', 'OthW', 'Floor']], ['central_air', 'Central air', ['Y', 'N']]]

export default function ProjectAssistant({ predictions }) {
  const [open, setOpen] = useState(false)
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([welcome])
  const [loading, setLoading] = useState(false)
  const [showPredictor, setShowPredictor] = useState(false)
  const [property, setProperty] = useState(defaultProperty)
  const [priceResult, setPriceResult] = useState(null)
  const [predictionError, setPredictionError] = useState('')
  const [position, setPosition] = useState(null)
  const drag = useRef({ active: false, moved: false, offsetX: 0, offsetY: 0 })
  const clearChat = () => {
    if (loading) return
    setMessages([welcome])
    setQuestion('')
    setPriceResult(null)
    setPredictionError('')
  }
  const updateProperty = (key, value) => setProperty((current) => ({ ...current, [key]: value }))
  const selectSuggestion = (suggestion) => { if (suggestion === predictSuggestion) setShowPredictor(true); else ask(suggestion) }
  const predictPrice = async (event) => {
    event.preventDefault()
    setPredictionError('')
    setPriceResult(null)
    setLoading(true)
    try {
      const { data } = await predictHouse(property)
      setPriceResult(data)
    } catch (error) {
      setPredictionError(error.response?.data?.detail || 'Prediction failed. Check that the backend and trained models are running.')
    } finally {
      setLoading(false)
    }
  }
  const startDrag = (event) => {
    const bounds = event.currentTarget.getBoundingClientRect()
    drag.current = { active: true, moved: false, offsetX: event.clientX - bounds.left, offsetY: event.clientY - bounds.top }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  const moveAssistant = (event) => {
    if (!drag.current.active) return
    const nextX = Math.max(14, Math.min(window.innerWidth - 66, event.clientX - drag.current.offsetX))
    const nextY = Math.max(14, Math.min(window.innerHeight - 66, event.clientY - drag.current.offsetY))
    if (Math.abs(nextX - (position?.x ?? nextX)) > 2 || Math.abs(nextY - (position?.y ?? nextY)) > 2) drag.current.moved = true
    setPosition({ x: nextX, y: nextY })
  }
  const endDrag = (event) => {
    if (!drag.current.active) return
    drag.current.active = false
    event.currentTarget.releasePointerCapture?.(event.pointerId)
    if (!drag.current.moved) setOpen((value) => !value)
  }
  const launcherStyle = { ...(position ? { left: position.x, top: position.y, right: 'auto', bottom: 'auto' } : {}), cursor: 'grab', touchAction: 'none' }
  const panelStyle = position ? { left: Math.max(14, Math.min(position.x, window.innerWidth - 374)), top: Math.max(14, position.y - 532), right: 'auto', bottom: 'auto' } : undefined
  const ask = async (value = question) => {
    const text = value.trim()
    if (!text || loading) return
    setMessages((current) => [...current, { role: 'user', text }])
    setQuestion('')
    setLoading(true)
    try {
      const { data } = await api.post('/assistant/ask', { question: text, predictions })
      setMessages((current) => [...current, { role: 'assistant', text: data.answer, suggestions: data.suggestions }])
    } catch {
      setMessages((current) => [...current, { role: 'assistant', text: 'I cannot reach the project assistant right now. Make sure the FastAPI backend is running.' }])
    } finally {
      setLoading(false)
    }
  }
  return <><button className="assistant-launcher" style={launcherStyle} type="button" onPointerDown={startDrag} onPointerMove={moveAssistant} onPointerUp={endDrag} aria-label="Open project assistant" title="Drag or open project assistant">{open ? <X size={20} /> : <MessageCircle size={20} />}<span className="assistant-badge">AI</span></button>{open && <section className="assistant-panel" style={panelStyle}><header><div className="assistant-title"><span className="assistant-icon"><Bot size={17} /></span><div><strong>Project assistant</strong><small>Local model guide</small></div></div><div className="assistant-header-actions"><button type="button" onClick={clearChat} disabled={loading} aria-label="Clear chat" title="Clear chat"><RotateCcw size={16} /></button><button type="button" onClick={() => setOpen(false)} aria-label="Close assistant" title="Close assistant"><X size={16} /></button></div></header><div className="assistant-messages">{messages.map((message, index) => <div className={`assistant-message ${message.role}`} key={`${message.role}-${index}`}><p>{message.text}</p>{message.suggestions?.length > 0 && <div className="assistant-suggestions">{message.suggestions.map((suggestion) => <button type="button" key={suggestion} onClick={() => selectSuggestion(suggestion)}>{suggestion}</button>)}</div>}</div>)}{showPredictor && <form className="assistant-predict-form" onSubmit={predictPrice}><p>Enter property details to get predictions from all three models.</p><div className="assistant-predict-grid">{predictionFields.map(([key, label, type, min, max]) => <label key={key}>{label}<input required type={type} value={property[key]} min={min} max={max} onChange={(event) => updateProperty(key, Number(event.target.value))} /></label>)}{predictionSelects.map(([key, label, options]) => <label key={key}>{label}<select value={property[key]} onChange={(event) => updateProperty(key, event.target.value)}>{options.map((option) => <option key={option} value={option}>{option}</option>)}</select></label>)}</div><button className="assistant-predict-submit" type="submit" disabled={loading}>{loading ? 'Calculating...' : 'Predict price'}</button></form>}{priceResult && <div className="assistant-price-result"><strong>Predicted prices</strong><span>Linear Regression: ${priceResult.predictions.linear_regression.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span><span>Random Forest: ${priceResult.predictions.random_forest.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span><span>Neural Network: ${priceResult.predictions.neural_network.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span><b>Average: ${priceResult.average_prediction.toLocaleString('en-US', { maximumFractionDigits: 0 })}</b></div>}{predictionError && <p className="assistant-prediction-error">{predictionError}</p>}{loading && <div className="assistant-message assistant"><p className="typing">Thinking...</p></div>}</div><form className="assistant-input" onSubmit={(event) => { event.preventDefault(); ask() }}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask about your project..." aria-label="Ask the project assistant" /><button type="submit" aria-label="Send question"><Send size={16} /></button></form></section>}</>
}
