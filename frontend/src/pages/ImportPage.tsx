import { useEffect, useState } from "react"
import { uploadCSV, getClienti } from "../api/clienti"
import ClienteCard from "../components/ClienteCard"
import { toast } from "react-toastify"

export default function ImportPage() {
  const [file, setFile] = useState<File | null>(null)
  const [clienti, setClienti] = useState<any[]>([])

  const fetchClienti = async () => {
    const res = await getClienti()
    setClienti(res)
  }

  const handleUpload = async () => {
    if (!file) return toast.error("Seleziona un file")
    await uploadCSV(file)
    toast.success("Clienti importati")
    fetchClienti()
  }

  useEffect(() => {
    fetchClienti()
  }, [])

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Importa clienti da CSV</h1>
      <div className="flex gap-2 mb-6">
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        <button
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          onClick={handleUpload}
        >
          Carica
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {clienti.map(c => (
          <ClienteCard key={c.id} cliente={c} />
        ))}
      </div>
    </div>
  )
}