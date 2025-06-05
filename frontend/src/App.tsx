import DashboardPage from './pages/DashboardPage';
import ImportPage from './pages/ImportPage';
import { useState } from 'react';

export default function App() {
  const [tab, setTab] = useState<'import' | 'dashboard'>('import');

  return (
    <div className="min-h-screen p-4">
      <div className="mb-4 flex gap-4">
        <button className="px-4 py-2 bg-primary text-white rounded" onClick={() => setTab('import')}>Importa</button>
        <button className="px-4 py-2 bg-primary text-white rounded" onClick={() => setTab('dashboard')}>Dashboard</button>
      </div>
      {tab === 'import' ? <ImportPage /> : <DashboardPage />}
    </div>
  );
}

