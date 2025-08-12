import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { api } from '../../lib/axios'
import { useNavigate, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { toast } from 'sonner'
import ComboboxCreatable from '../../components/ComboboxCreatable'

const schema = z.object({
  nombre: z.string().min(1),
  proveedor_id: z.number(),
  modelo_proveedor: z.string().optional().or(z.literal('')),
  modelo_goldmund: z.string().optional().or(z.literal('')),
})

type FormData = z.infer<typeof schema>

export default function ProductForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [odc, setOdc] = useState('')
  const { data: providers } = useQuery(['providers'], async () => (await api.get('/providers')).data)
  const { data: odcs, refetch: refetchOdc } = useQuery(['odc'], async () => (await api.get('/odc')).data)
  const { register, handleSubmit, setValue } = useForm<FormData>({ resolver: zodResolver(schema) })

  useEffect(() => {
    if (id) {
      api.get(`/products/${id}`).then(res => {
        const p = res.data
        setValue('nombre', p.nombre)
        setValue('proveedor_id', p.proveedor_id)
        setValue('modelo_proveedor', p.modelo_proveedor || '')
        setValue('modelo_goldmund', p.modelo_goldmund || '')
        setOdc(p.odc?.nombre || '')
      })
    }
  }, [id, setValue])

  const onSubmit = async (data: FormData) => {
    try {
      let odcId: number | undefined
      if (odc) {
        const existing = odcs?.find((o: any) => o.nombre === odc)
        if (existing) odcId = existing.id
        else {
          const created = await api.post('/odc', { nombre: odc })
          odcId = created.data.id
          refetchOdc()
        }
      }
      const payload = { ...data, odc_id: odcId }
      if (id) await api.put(`/products/${id}`, payload)
      else await api.post('/products', payload)
      toast.success('Producto guardado')
      navigate('/productos')
    } catch {
      toast.error('Error al guardar')
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-xl mb-4">Producto</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
        <input placeholder="Nombre" {...register('nombre')} className="w-full p-2 text-black" />
        <select {...register('proveedor_id', { valueAsNumber: true })} className="w-full p-2 text-black">
          <option value="">Proveedor</option>
          {providers && providers.map((p: any) => (
            <option key={p.id} value={p.id}>{p.nombre}</option>
          ))}
        </select>
        <input placeholder="Modelo proveedor" {...register('modelo_proveedor')} className="w-full p-2 text-black" />
        <input placeholder="Modelo Goldmund" {...register('modelo_goldmund')} className="w-full p-2 text-black" />
        <ComboboxCreatable options={odcs?.map((o: any) => o.nombre) || []} value={odc} onChange={setOdc} />
        <button type="submit" className="bg-gold text-black px-4 py-2">Guardar</button>
      </form>
    </div>
  )
}
