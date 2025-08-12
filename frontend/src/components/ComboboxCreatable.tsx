import { useState } from 'react'

interface Option { value: string; label: string }

export default function ComboboxCreatable({ options, onChange }: { options: Option[]; onChange: (v: string) => void }) {
  const [value, setValue] = useState('')
  return (
    <input
      list="combo"
      value={value}
      onChange={e => { setValue(e.target.value); onChange(e.target.value) }}
      className="border p-2"
    />
  )
}
