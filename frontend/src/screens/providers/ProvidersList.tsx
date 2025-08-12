import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import api from '../../lib/axios'

interface Provider {
  id: number
  nombre: string
  email?: string
}

export default function ProvidersList() {
  const { data } = useQuery(['providers'], async () => {
    const res = await api.get('/providers')
    return res.data as Provider[]
  })

  return (
    <div className="p-4">
      <div className="flex justify-between mb-2">
        <h1 className="text-xl">Proveedores</h1>
        <Link to="/proveedores/nuevo" className="bg-yellow-500 text-black p-2">Nuevo</Link>
      </div>
      <ul>
        {data?.map(p => (
          <li key={p.id} className="border-b py-1">{p.nombre}</li>
        ))}
      </ul>
    </div>
  )
}
