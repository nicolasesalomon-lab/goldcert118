interface Props {
  onUpload: (file: File) => void
}

export default function FileUploader({ onUpload }: Props) {
  const handle = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) onUpload(file)
  }
  return <input type="file" onChange={handle} className="text-sm" />
}
