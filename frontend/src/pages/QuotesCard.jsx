export default function QuotesCard() {
  return (
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
  );
}
