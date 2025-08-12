import { useState } from 'react'

interface Props {
  options: string[]
  value?: string
  onChange: (v: string) => void
}

export default function ComboboxCreatable({ options, value, onChange }: Props) {
  const [opts, setOpts] = useState(options)
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value
    if (val === '__new__') {
      const name = prompt('Nuevo valor')
      if (name) {
        setOpts([...opts, name])
        onChange(name)
      }
    } else {
      onChange(val)
    }
  }
  return (
    <select value={value} onChange={handleChange} className="p-1 bg-gray-800 border border-gray-600">
      <option value="">Seleccionar...</option>
      {opts.map((o) => (
        <option key={o} value={o}>{o}</option>
      ))}
      <option value="__new__">Agregar...</option>
    </select>
  )
}
