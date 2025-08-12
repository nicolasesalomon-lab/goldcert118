import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import api from '../../lib/axios'

const schema = z.object({
  nombre: z.string().min(1),
  email: z.string().email().optional(),
  telefono: z.string().optional()
})

type FormData = z.infer<typeof schema>

export default function ProviderForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) })

  const onSubmit = async (data: FormData) => {
    await api.post('/providers', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 flex flex-col gap-2">
      <input {...register('nombre')} placeholder="Nombre" className="border p-2" />
      {errors.nombre && <span className="text-red-500">Nombre requerido</span>}
      <input {...register('email')} placeholder="Email" className="border p-2" />
      <input {...register('telefono')} placeholder="Teléfono" className="border p-2" />
      <button type="submit" className="bg-yellow-500 text-black p-2">Guardar</button>
    </form>
  )
}
