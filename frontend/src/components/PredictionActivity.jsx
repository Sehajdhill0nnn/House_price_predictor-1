import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const models = [['linear_regression', 'Linear Regression'], ['random_forest', 'Random Forest'], ['neural_network', 'Neural Network']]

export default function PredictionActivity({ history }) {
  const data = models.map(([key, label]) => ({ model: label, average: history.length ? history.reduce((sum, item) => sum + item.predictions[key], 0) / history.length : 0 }))
  return <section className="surface activity-comparison"><div className="panel-heading"><div><span className="eyebrow">History-linked view</span><h3>Average saved predictions</h3><p className="panel-caption">This view updates when prediction history changes. Training metrics above remain fixed.</p></div></div>{history.length ? <ResponsiveContainer width="100%" height={240}><BarChart data={data} margin={{ top: 12, right: 10, left: 4, bottom: 4 }}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="model" tick={{ fontSize: 10 }} interval={0} /><YAxis tickFormatter={(value) => `${Math.round(value / 100000)}L`} tick={{ fontSize: 10 }} /><Tooltip formatter={(value) => [`$ ${Number(value).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`, 'Average saved prediction']} /><Bar dataKey="average" name="Average saved prediction" fill="#2563eb" radius={[5, 5, 0, 0]} /></BarChart></ResponsiveContainer> : <div className="dashboard-empty">Delete or create history records to update this comparison.</div>}</section>
}
