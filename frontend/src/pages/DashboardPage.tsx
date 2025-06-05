import { useEffect, useState } from "react"
import axios from "axios"
import dayjs from "dayjs"

export default function DashboardPage() {
  const [trigger, setTrigger] = useState<any[]>([])
  const [profili, setProfili] = useState<any[]>([])
  const [filtroLivello, setFiltroLivello] = useState("")

  const fetchData = async () => {
    const res1 = await axios.get("http://localhost:8000/trigger-aml")
    const res2 = await axios.get("http://localhost:8000/tutti-profili-rischio")
    setTrigger(res1.data)
    setProfili(res2.data)
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Dashboard AML</h1>

      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Trigger attivi</h2>
        <table className="w-full border bg-white">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Cliente ID</th>
              <th>Motivo</th>
              <th>Livello</th>
              <th>Data</th>
              <th>Stato</th>
            </tr>
          </thead>
          <tbody>
            {trigger.map(t => (
              <tr key={t.id} className="text-sm text-center">
                <td className="p-2">{t.cliente_id}</td>
                <td>{t.motivo}</td>
                <td>{t.livello}</td>
                <td>{dayjs(t.data).format("DD/MM/YYYY")}</td>
                <td>{t.stato}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">Storico Profili Rischio</h2>

        <label className="text-sm">Filtro per livello:</label>
        <select
          className="ml-2 border rounded p-1"
          onChange={(e) => setFiltroLivello(e.target.value)}
        >
          <option value="">Tutti</option>
          <option value="Alto">Alto</option>
          <option value="Medio">Medio</option>
          <option value="Basso">Basso</option>
        </select>

        <table className="w-full mt-4 border bg-white">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Cliente ID</th>
              <th>Punteggio</th>
              <th>Livello</th>
              <th>Articoli</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {profili
              .filter(p => !filtroLivello || p.livello === filtroLivello)
              .map(p => (
                <tr key={p.id} className="text-sm text-center">
                  <td className="p-2">{p.cliente_id}</td>
                  <td>{p.punteggio}</td>
                  <td>{p.livello}</td>
                  <td>{p.articoli_analizzati}</td>
                  <td>{dayjs(p.data).format("DD/MM/YYYY")}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}