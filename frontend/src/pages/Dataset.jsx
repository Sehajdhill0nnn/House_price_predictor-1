import { useEffect, useState } from 'react'
import { AlertCircle, CheckCircle2, Database, Upload } from 'lucide-react'
import { fetchDatasetSchema, trainUploadedDataset } from '../services/api'

export default function Dataset({ onTrained }) {
  const [schema, setSchema] = useState(null)
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchDatasetSchema().then(({ data }) => setSchema(data)).catch(() => setError('Could not load the dataset schema.'))
  }, [])

  const submit = async (event) => {
    event.preventDefault()
    if (!file) return setError('Choose a CSV file first.')
    setLoading(true)
    setError('')
    setStatus('Uploading and retraining all three models...')
    try {
      const { data } = await trainUploadedDataset(file)
      setStatus(`${data.filename} trained successfully with ${data.rows} rows.`)
      onTrained?.()
    } catch (err) {
      setStatus('')
      setError(err.response?.data?.detail || 'Dataset upload or training failed.')
    } finally {
      setLoading(false)
    }
  }

  return <><header className="page-header"><div><span className="eyebrow">Model data</span><h1>Upload a dataset</h1><p>Train a new set of predictions from your own compatible CSV.</p></div></header><div className="dataset-layout"><section className="surface upload-panel"><div className="upload-icon"><Database size={25} /></div><h2>Replace training data</h2><p className="upload-copy">Upload a CSV with the selected property features and a <strong>SalePrice</strong> column. Current models stay active until training finishes.</p><form onSubmit={submit}><label className="file-drop"><Upload size={22} /><strong>{file ? file.name : 'Choose a CSV file'}</strong><span>{file ? `${(file.size / 1024 / 1024).toFixed(2)} MB selected` : 'Maximum file size: 25 MB'}</span><input type="file" accept=".csv,text/csv" onChange={(event) => setFile(event.target.files?.[0] || null)} /></label><button className="primary-button" type="submit" disabled={loading}>{loading ? <><span className="spinner" />Training models...</> : 'Upload and train'}<span>↗</span></button></form>{status && <div className="success-box"><CheckCircle2 size={17} />{status}</div>}{error && <div className="error-box"><AlertCircle size={17} />{error}</div>}</section><section className="surface schema-panel"><span className="eyebrow">CSV contract</span><h2>Required columns</h2><p>Column names must match the trained feature contract exactly.</p><div className="schema-list">{schema?.required_columns?.map((column) => <span key={column}>{column}</span>) || <span>Loading schema...</span>}</div></section></div></>
}
