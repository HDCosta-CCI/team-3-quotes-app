import { useState, useEffect } from "react";
import { fetchQuotes } from "../utils/api";
import "./Quotes.css";

export default function QuotesPage() {
  const [quotes, setQuotes] = useState([]);

  useEffect(() => {
    async function getQuotes() {
      const data = await fetchQuotes();
      setQuotes(data);
      console.log(quotes);
    }
    getQuotes();
  }, []);

  return (
    <div className="quotes-page">
      <h1>Quotes Page</h1>
      <ul className="quote-list">
        {quotes?.map((quote) => (
          <li key={quote.quote_id}>
            <div to={`/quotes/${quote.quote_id}`}>
              <h2 className="left">
                <i>"{quote.quote}"</i>
              </h2>
              <p className="right"> ~ {quote.author}</p>
              {quote.tags?.split(";").map((tag, index) => (
                <span key={index} className="tag">
                  {tag.trim()}
                </span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
