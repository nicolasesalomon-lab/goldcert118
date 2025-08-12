import api from './axios'

export async function login(email: string, password: string) {
  const params = new URLSearchParams()
  params.append('username', email)
  params.append('password', password)
  const { data } = await api.post('/auth/login', params)
  localStorage.setItem('token', data.access_token)
}
