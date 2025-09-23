import { NavLink, useRouteLoaderData } from "react-router-dom";
import classes from "./QuotesNavigation.module.css";

export default function QuoteNavigation() {
  const token = useRouteLoaderData("root");
  return (
    <header className={classes.header}>
      <nav>
        <ul className={classes.list}>
          <li>
            <div
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
            >
              Search Bar
            </div>
          </li>
          {token && (
            <li>
              <NavLink
                to="/quotes/new"
                className={({ isActive }) =>
                  isActive ? classes.active : undefined
                }
              >
                Add Quote +
              </NavLink>
            </li>
          )}
        </ul>
      </nav>
    </header>
  );
}
