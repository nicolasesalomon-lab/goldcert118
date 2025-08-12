import { Routes, Route, Navigate } from 'react-router-dom'
import { getToken } from './lib/auth'
import Login from './screens/Login'
import Dashboard from './screens/Dashboard'
import ProvidersList from './screens/providers/ProvidersList'
import ProviderForm from './screens/providers/ProviderForm'
import ProviderDetail from './screens/providers/ProviderDetail'
import ProductForm from './screens/products/ProductForm'
import CertificationWizard from './screens/cert/CertificationWizard'

function RequireAuth({ children }: { children: JSX.Element }) {
  return getToken() ? children : <Navigate to="/login" replace />
}

export const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={<Login />} />
    <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
    <Route path="/proveedores" element={<RequireAuth><ProvidersList /></RequireAuth>} />
    <Route path="/proveedores/nuevo" element={<RequireAuth><ProviderForm /></RequireAuth>} />
    <Route path="/proveedores/:id" element={<RequireAuth><ProviderDetail /></RequireAuth>} />
    <Route path="/productos/nuevo" element={<RequireAuth><ProductForm /></RequireAuth>} />
    <Route path="/productos/:id" element={<RequireAuth><ProductForm /></RequireAuth>} />
    <Route path="/certificaciones/:id" element={<RequireAuth><CertificationWizard /></RequireAuth>} />
    <Route path="*" element={<Navigate to="/login" />} />
  </Routes>
)
