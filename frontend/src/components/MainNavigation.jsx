import { Form, NavLink, useRouteLoaderData } from "react-router-dom";
import classes from "./MainNavigation.module.css";

function MainNavigation() {
  
  const token = useRouteLoaderData('root');
  return (
    <header className={classes.header}>
      <nav className={classes.nav}>
        <NavLink to="/" className={classes.logo}>
          <h2>Quotes APP</h2>
        </NavLink>
        {!token && (
          <ul className={classes.list1}>
            <li> <NavLink to="/quotes" className={({ isActive }) => isActive ? classes.active : undefined}>Quotes</NavLink> </li>
            <li> <NavLink to="/auth/?mode=login" className={({ isActive }) => isActive ? classes.active : undefined}>Login/Sign-up</NavLink> </li>
          </ul>
        )}
        {token && (
          <ul className={classes.list2}>
            <li> <NavLink to="" className={({ isActive }) => isActive ? classes.active : undefined}>Home</NavLink> </li>
            <li> <NavLink to="/authors" className={({ isActive }) => isActive ? classes.active : undefined}>Authors</NavLink> </li>
            <li> <NavLink to="/quotes" className={({ isActive }) => isActive ? classes.active : undefined}>Quotes</NavLink> </li>
            <li> <NavLink to="" className={({ isActive }) => isActive ? classes.active : undefined}>My Quotes</NavLink> </li>
            <li className={classes.userInfo}>
              <details>
                <summary>Haysten</summary>
                <Form action="/logout" method="post"><button>Logout</button></Form>
              </details>
            </li>
          </ul>
        )}
      </nav>
    </header>
  );
}

export default MainNavigation;
