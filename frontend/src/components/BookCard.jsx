import { Link } from "react-router-dom";

function BookCard({ book }) {
  return (
    <article className="rounded-lg border bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-800">{book.title}</h2>
      <p className="text-sm text-slate-600">Author: {book.author}</p>
      <p className="mt-2 text-sm text-amber-600">Rating: {book.rating} / 5</p>
      <p className="mt-3 text-sm text-slate-700">{book.description}</p>
      <Link className="mt-4 inline-block text-blue-600 hover:underline" to={`/books/${book.id}`}>
        View details
      </Link>
    </article>
  );
}

export default BookCard;

