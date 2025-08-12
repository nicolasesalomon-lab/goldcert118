import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../../lib/axios'
import FactoryCreate from './FactoryCreate'
import { useState } from 'react'

export default function ProviderDetail() {
  const { id } = useParams()
  const providerId = Number(id)
  const { data: provider } = useQuery(['provider', id], async () => (await api.get(`/providers/${id}`)).data)
  const { data: factories, refetch } = useQuery(['factories', id], async () => (await api.get('/factories', { params: { provider_id: id } })).data)
  const [showForm, setShowForm] = useState(false)

  if (!provider) return <p className="p-4">Cargando...</p>

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl">{provider.nombre}</h1>
      <button onClick={() => setShowForm(!showForm)} className="bg-gray-700 px-2 py-1">Crear fábrica</button>
      {showForm && <FactoryCreate providerId={providerId} onCreated={() => { setShowForm(false); refetch() }} />}
      <ul className="mt-4 space-y-1">
        {factories && factories.map((f: any) => (
          <li key={f.id}>{f.nombre}</li>
        ))}
      </ul>
    </div>
  )
}
