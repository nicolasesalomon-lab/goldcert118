import { Route, Routes, Navigate } from 'react-router-dom'
import Login from './screens/Login'
import ProvidersList from './screens/providers/ProvidersList'
import ProviderForm from './screens/providers/ProviderForm'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/proveedores" element={<ProvidersList />} />
      <Route path="/proveedores/nuevo" element={<ProviderForm />} />
      <Route path="/" element={<Navigate to="/proveedores" />} />
    </Routes>
  )
}
