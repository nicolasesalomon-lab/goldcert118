import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { api } from '../lib/axios'
import { setToken } from '../lib/auth'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
})

type FormData = z.infer<typeof schema>

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) })
  const navigate = useNavigate()

  const onSubmit = async (data: FormData) => {
    try {
      const res = await api.post('/auth/login', data)
      setToken(res.data.access_token)
      navigate('/dashboard')
    } catch {
      toast.error('Credenciales inválidas')
    }
  }

  return (
    <div className="p-4 max-w-sm mx-auto mt-20">
      <h1 className="text-2xl mb-4 text-gold">GoldCert</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
        <input placeholder="Email" {...register('email')} className="w-full p-2 text-black" />
        {errors.email && <p className="text-red-500 text-sm">Email inválido</p>}
        <input type="password" placeholder="Password" {...register('password')} className="w-full p-2 text-black" />
        <button type="submit" className="w-full bg-gold text-black p-2">Login</button>
      </form>
    </div>
  )
}
