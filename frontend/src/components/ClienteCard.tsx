import React, { useState } from "react"
import { analizzaCliente } from "../api/clienti"

type Props = {
  cliente: {
    id: number
    nome: string
    cognome: string
    data_nascita: string
    nazionalità: string
  }
}

export default function ClienteCard({ cliente }: Props) {
  const [loading, setLoading] = useState(false)
  const [rischio, setRischio] = useState<any | null>(null)

  const handleAnalizza = async () => {
    setLoading(true)
    const result = await analizzaCliente(cliente.id)
    setRischio(result.profilo_rischio)
    setLoading(false)
  }

  const handleReport = () => {
    window.open(`http://localhost:8000/report/${cliente.id}`, "_blank")
  }

  const badge = (livello: string) => {
    const base = "px-2 py-1 text-xs rounded text-white font-semibold"
    if (livello === "Alto") return base + " bg-red-600"
    if (livello === "Medio") return base + " bg-yellow-500 text-black"
    return base + " bg-green-600"
  }

  return (
    <div className="border p-4 shadow-lg rounded-xl bg-white space-y-3 transition hover:shadow-2xl">
      <div>
        <p className="font-bold text-lg text-primary">{cliente.nome} {cliente.cognome}</p>
        <p className="text-sm text-gray-500">{cliente.data_nascita} — {cliente.nazionalità}</p>
      </div>
      <div className="flex flex-col sm:flex-row gap-2">
        <button
          className="px-3 py-1 bg-accent text-white rounded hover:bg-sky-600 transition"
          onClick={handleAnalizza}
          disabled={loading}
        >
          {loading ? "Analisi..." : "Analizza"}
        </button>
        <button
          className="px-3 py-1 bg-primary text-white rounded hover:bg-indigo-700 transition"
          onClick={handleReport}
        >
          Scarica Report
        </button>
      </div>

      {rischio && (
        <div className="border-t pt-2 mt-2">
          <p className="text-sm">Punteggio: {rischio.punteggio}</p>
          <p className={badge(rischio.livello)}>Livello: {rischio.livello}</p>
          <ul className="text-sm mt-2 space-y-1">
            {Object.entries(rischio.url_sospetti).map(([url, score]) => (
              <li key={url}>
                <a href={url} className="text-blue-700 underline" target="_blank">
                  {url}
                </a> — {score}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}