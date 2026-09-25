import { useState } from 'react'
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { AreaChart as AreaChartIcon, BarChart3, LineChart as LineChartIcon } from 'lucide-react'

const labels = {
  linear_regression: 'Linear Regression',
  random_forest: 'Random Forest',
  neural_network: 'Neural Network',
}

const colors = {
  'Linear Regression': '#274c5e',
  'Random Forest': '#e27648',
  'Neural Network': '#2a9d8f',
}

export default function PredictionChart({ predictions }) {
  const [view, setView] = useState('bar')
  const data = Object.entries(predictions).map(([key, value]) => ({
    model: labels[key],
    price: value,
  }))

  return <div className="prediction-chart chart-panel">
    <div className="panel-title">
      <div>
        <span className="eyebrow">Live comparison</span>
        <h3>Prediction spread</h3>
      </div>
      <div className="chart-controls" role="group" aria-label="Graph view">
        {[['bar', BarChart3, 'Bar chart'], ['line', LineChartIcon, 'Line chart'], ['area', AreaChartIcon, 'Area chart']].map(([key, Icon, label]) => <button key={key} className={view === key ? 'chart-control active' : 'chart-control'} type="button" title={label} aria-label={label} onClick={() => setView(key)}><Icon size={14} /></button>)}
      </div>
    </div>
    <ResponsiveContainer width="100%" height={230}>
      {view === 'bar' && <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="model" tick={{ fontSize: 10 }} interval={0} />
        <YAxis tickFormatter={(value) => `${Math.round(value / 100000)}L`} tick={{ fontSize: 10 }} />
        <Tooltip formatter={(value) => [`$ ${Number(value).toLocaleString('en-IN')}`, 'Prediction']} />
        <Bar dataKey="price" name="Predicted price" radius={[5, 5, 0, 0]}>
          {data.map((entry) => <Cell key={entry.model} fill={colors[entry.model]} />)}
        </Bar>
      </BarChart>}
      {view === 'line' && <LineChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="model" tick={{ fontSize: 10 }} interval={0} />
        <YAxis tickFormatter={(value) => `${Math.round(value / 100000)}L`} tick={{ fontSize: 10 }} />
        <Tooltip formatter={(value) => [`$ ${Number(value).toLocaleString('en-IN')}`, 'Prediction']} />
        <Line type="monotone" dataKey="price" name="Predicted price" stroke="#e27648" strokeWidth={3} dot={{ r: 5, fill: '#e27648' }} />
      </LineChart>}
      {view === 'area' && <AreaChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="model" tick={{ fontSize: 10 }} interval={0} />
        <YAxis tickFormatter={(value) => `${Math.round(value / 100000)}L`} tick={{ fontSize: 10 }} />
        <Tooltip formatter={(value) => [`$ ${Number(value).toLocaleString('en-IN')}`, 'Prediction']} />
        <Area type="monotone" dataKey="price" name="Predicted price" stroke="#2a9d8f" fill="#2a9d8f" fillOpacity={0.22} strokeWidth={3} />
      </AreaChart>}
    </ResponsiveContainer>
  </div>
}
