import { useEffect, useState } from "react";
import ErrorMessage from "../components/ErrorMessage";
import Loading from "../components/Loading";
import { askQuestion, fetchHistory } from "../services/api";

function QAPage() {
  const [question, setQuestion] = useState("Suggest books for someone who likes thoughtful sci-fi stories.");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [metaMessage, setMetaMessage] = useState("");

  const loadHistory = async () => {
    try {
      setHistory(await fetchHistory());
    } catch {
      // Keep the page usable even if history fails.
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!question.trim()) {
      setError("Please enter a question before asking.");
      return;
    }

    setLoading(true);
    setError("");
    setMetaMessage("");
    try {
      const result = await askQuestion(question);
      setAnswer(result.answer);
      setSources(result.sources || []);
      if (result.fallback) {
        setMetaMessage("AI model is offline. Showing a context-based fallback answer.");
      } else if (result.cached) {
        setMetaMessage("Showing a cached answer for faster response.");
      } else {
        setMetaMessage("AI answer generated successfully.");
      }
      await loadHistory();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(detail || "Could not generate an answer right now. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="space-y-6">
      <form className="space-y-3 rounded-lg border bg-white p-5" onSubmit={handleSubmit}>
        <h2 className="text-xl font-semibold text-slate-800">RAG Q&A</h2>
        <textarea
          className="h-28 w-full rounded-md border p-3"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask anything about books in your library..."
        />
        <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-60" disabled={loading}>
          Ask AI
        </button>
      </form>
      {loading && <Loading label="Thinking with retrieved context..." />}
      {error && <ErrorMessage message={error} />}
      {metaMessage && (
        <div className="rounded-md border border-blue-200 bg-blue-50 p-3 text-sm text-blue-700">
          {metaMessage}
        </div>
      )}
      {answer && (
        <article className="rounded-lg border bg-white p-5">
          <h3 className="mb-2 text-lg font-semibold">Answer</h3>
          <p className="text-slate-700">{answer}</p>
          <h4 className="mt-4 font-semibold">Sources</h4>
          {sources.length > 0 ? (
            <ul className="list-disc pl-5 text-sm text-slate-700">
              {sources.map((src, idx) => (
                <li key={`${src.book_id}-${idx}`}>{src.title} - {src.source}</li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-500">No source references available yet.</p>
          )}
        </article>
      )}
      <section className="rounded-lg border bg-white p-5">
        <h3 className="mb-3 text-lg font-semibold">Chat History</h3>
        <div className="space-y-3">
          {history.map((item) => (
            <div key={item.id} className="rounded border bg-slate-50 p-3">
              <p className="text-sm font-medium text-slate-700">Q: {item.question}</p>
              <p className="mt-1 text-sm text-slate-600">A: {item.answer}</p>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}

export default QAPage;

