import { useEffect, useState } from "react";
import BookCard from "../components/BookCard";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { fetchBooks, scrapeBooks } from "../services/api";

function DashboardPage() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [error, setError] = useState("");

  const loadBooks = async () => {
    setLoading(true);
    setError("");
    try {
      setBooks(await fetchBooks());
    } catch {
      setError("Failed to load books.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, []);

  const handleScrape = async () => {
    setScraping(true);
    try {
      await scrapeBooks(2);
      await loadBooks();
    } catch {
      setError("Scraping failed. Check backend logs.");
    } finally {
      setScraping(false);
    }
  };

  return (
    <section>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-800">Books Dashboard</h2>
        <button
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-60"
          onClick={handleScrape}
          disabled={scraping}
        >
          {scraping ? "Scraping..." : "Bulk Scrape Books"}
        </button>
      </div>
      {loading && <Loading label="Fetching books..." />}
      {error && <ErrorMessage message={error} />}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {books.map((book) => (
          <BookCard key={book.id} book={book} />
        ))}
      </div>
    </section>
  );
}

export default DashboardPage;

