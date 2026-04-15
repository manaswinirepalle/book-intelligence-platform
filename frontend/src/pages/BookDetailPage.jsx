import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { fetchBookDetail, fetchRecommendations } from "../services/api";

function BookDetailPage() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [bookData, recData] = await Promise.all([fetchBookDetail(id), fetchRecommendations(id)]);
        setBook(bookData);
        setRecommendations(recData.recommendations || []);
      } catch {
        setError("Failed to load book details.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (loading) return <Loading label="Loading details..." />;
  if (error) return <ErrorMessage message={error} />;
  if (!book) return null;

  return (
    <section className="space-y-6">
      <article className="rounded-lg border bg-white p-5">
        <h2 className="text-2xl font-bold text-slate-800">{book.title}</h2>
        <p className="text-sm text-slate-600">Author: {book.author}</p>
        <p className="text-sm text-amber-600">Rating: {book.rating}</p>
        <p className="mt-4 text-slate-700">{book.description}</p>
        <div className="mt-4 grid grid-cols-1 gap-2 text-sm md:grid-cols-3">
          <div className="rounded bg-slate-100 p-2">Summary: {book.summary}</div>
          <div className="rounded bg-slate-100 p-2">Genre: {book.genre}</div>
          <div className="rounded bg-slate-100 p-2">Sentiment: {book.sentiment}</div>
        </div>
      </article>
      <section>
        <h3 className="mb-3 text-lg font-semibold">Recommended Books</h3>
        <div className="space-y-2">
          {recommendations.map((rec) => (
            <div key={rec.id} className="rounded border bg-white p-3">
              <p className="font-medium text-slate-800">{rec.title}</p>
              <p className="text-sm text-slate-600">{rec.author}</p>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}

export default BookDetailPage;

