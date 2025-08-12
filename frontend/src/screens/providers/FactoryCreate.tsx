import { useForm } from 'react-hook-form'
import { api } from '../../lib/axios'
import { toast } from 'sonner'

export default function FactoryCreate({ providerId, onCreated }: { providerId: number; onCreated: () => void }) {
  const { register, handleSubmit, reset } = useForm<{ nombre: string; direccion?: string }>()

  const onSubmit = async (data: { nombre: string; direccion?: string }) => {
    await api.post('/factories', { ...data, proveedor_id: providerId })
    toast.success('Fábrica creada')
    reset()
    onCreated()
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-x-2 mt-2">
      <input placeholder="Nombre" {...register('nombre', { required: true })} className="p-1 text-black" />
      <input placeholder="Dirección" {...register('direccion')} className="p-1 text-black" />
      <button type="submit" className="bg-gold text-black px-2">Guardar</button>
    </form>
  )
}
