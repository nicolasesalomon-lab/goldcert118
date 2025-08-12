import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../../lib/axios'
import FileUploader from '../../components/FileUploader'
import { toast } from 'sonner'

const items = [
  { key: 'cb', label: 'CB' },
  { key: 'test_report', label: 'Test Report' },
  { key: 'manual', label: 'Manual' },
  { key: 'etiquetas', label: 'Etiquetas' },
  { key: 'mapa_modelos', label: 'Mapa modelos' },
  { key: 'declaracion_identidad', label: 'Declaración identidad' },
  { key: 'verificacion_identidad', label: 'Verificación identidad' },
]

export default function CertificationWizard() {
  const { id } = useParams()
  const [status, setStatus] = useState<Record<string, boolean>>({})

  useEffect(() => {
    items.forEach(it => {
      api.head(`/certifications/${id}/items/${it.key}/download`)
        .then(() => setStatus(s => ({ ...s, [it.key]: true })))
        .catch(() => setStatus(s => ({ ...s, [it.key]: false })))
    })
  }, [id])

  const handleUpload = async (tipo: string, file: File) => {
    const form = new FormData()
    form.append('file', file)
    await api.post(`/certifications/${id}/items/${tipo}`, form)
    toast.success('Archivo subido')
    setStatus(s => ({ ...s, [tipo]: true }))
  }

  const handleDownload = async (tipo: string) => {
    const res = await api.get(`/certifications/${id}/items/${tipo}/download`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = tipo
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="p-4 space-y-4">
      {items.map(it => (
        <div key={it.key} className="flex items-center gap-2">
          <span className="w-40">{it.label}</span>
          <span className={`px-2 text-sm rounded ${status[it.key] ? 'bg-green-600' : 'bg-gray-600'}`}>{status[it.key] ? 'completo' : 'pendiente'}</span>
          <FileUploader onUpload={(f) => handleUpload(it.key, f)} />
          {status[it.key] && <button onClick={() => handleDownload(it.key)} className="underline text-gold">Descargar</button>}
        </div>
      ))}
    </div>
  )
}
