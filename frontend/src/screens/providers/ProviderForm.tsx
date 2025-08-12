import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { api } from '../../lib/axios'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

const schema = z.object({
  nombre: z.string().min(1),
  email: z.string().email().optional().or(z.literal('')),
  telefono: z.string().optional().or(z.literal('')),
})

type FormData = z.infer<typeof schema>

export default function ProviderForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) })
  const navigate = useNavigate()

  const onSubmit = async (data: FormData) => {
    try {
      await api.post('/providers', data)
      toast.success('Proveedor creado')
      navigate('/proveedores')
    } catch {
      toast.error('Error al guardar')
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-xl mb-4">Nuevo proveedor</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
        <input placeholder="Nombre" {...register('nombre')} className="w-full p-2 text-black" />
        {errors.nombre && <p className="text-red-500 text-sm">Requerido</p>}
        <input placeholder="Email" {...register('email')} className="w-full p-2 text-black" />
        <input placeholder="Teléfono" {...register('telefono')} className="w-full p-2 text-black" />
        <button type="submit" className="bg-gold text-black px-4 py-2">Guardar</button>
      </form>
    </div>
  )
}
