import { createBrowserRouter } from "react-router-dom";
import HomePage from "../pages/Home.jsx";
import QuotesPage from "../pages/Quotes.jsx";
import ErrorPage from "../pages/Error.jsx";
import RootLayout from "../layout/RootLayout.jsx";
import AuthenticationPage from "../pages/Authentication.jsx";
import { action as LogoutAction } from "../pages/Logout.jsx";
import AuthorsPage from "../pages/Authors.jsx";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    children: [
      { index: true, element: <HomePage /> },
      { path: "quotes", 
        // element: <QuotesRootLayout />,
        children: [
          { index: true, element: <QuotesPage /> },
          // { path: "/quoteId", element: },
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
