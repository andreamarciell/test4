import axios from "axios"

const API_BASE = "http://localhost:8000"

export async function uploadCSV(file: File) {
  const formData = new FormData()
  formData.append("file", file)
  const res = await axios.post(`${API_BASE}/importa-clienti/`, formData)
  return res.data
}

export async function getClienti() {
  const res = await axios.get(`${API_BASE}/clienti`)
  return res.data
}

export async function analizzaCliente(id: number) {
  const res = await axios.post(`${API_BASE}/profiling-cliente/${id}`)
  return res.data
}