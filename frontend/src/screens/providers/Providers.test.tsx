import { describe, it, expect } from 'vitest'

// simple placeholder test representing creating a provider and listing

describe('proveedores flow', () => {
  it('crear proveedor aparece en listado', () => {
    const providers: any[] = []
    providers.push({ id: 1, nombre: 'Prov 1' })
    expect(providers.map(p => p.nombre)).toContain('Prov 1')
  })
})
