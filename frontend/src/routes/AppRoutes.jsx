import { createBrowserRouter } from "react-router-dom";
import QuotesRootLayout from "../layout/QuotesRootLayout.jsx";
import RootLayout from "../layout/RootLayout.jsx";
import HomePage from "../pages/Home.jsx";
import QuotesPage from "../pages/Quotes.jsx";
import NewQuotesPage from "../pages/NewQuote.jsx";
import ErrorPage from "../pages/Error.jsx";
import AuthenticationPage from "../pages/Authentication.jsx";
import { tokenLoader } from "../utils/auth.js";
import { action as LogoutAction } from "../pages/Logout.jsx";
import AuthorsPage from "../pages/Authors.jsx";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    loader: tokenLoader,
    children: [
      { index: true, element: <HomePage /> },
      { path: "quotes", 
        element: <QuotesRootLayout />,
        children: [
          { index: true, element: <QuotesPage /> },
          { path: "new", element: <NewQuotesPage />},
        ]
      },
      { path: "authors",
        element: <AuthorsPage />,
      },
      { path: "/auth", element: <AuthenticationPage /> },
      { path: "/logout", action: LogoutAction }
    ]
  }
]);
