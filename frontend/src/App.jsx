import { Link, Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import BookDetailPage from "./pages/BookDetailPage";
import QAPage from "./pages/QAPage";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <h1 className="text-xl font-bold text-slate-800">Book Intelligence Platform</h1>
          <nav className="space-x-4">
            <Link className="text-blue-600 hover:underline" to="/">Dashboard</Link>
            <Link className="text-blue-600 hover:underline" to="/qa">Q&A</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/books/:id" element={<BookDetailPage />} />
          <Route path="/qa" element={<QAPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

