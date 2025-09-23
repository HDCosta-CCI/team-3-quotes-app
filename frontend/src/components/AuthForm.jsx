import {
  Form,
  Link,
  useSearchParams,
  useActionData,
  useNavigation,
} from "react-router-dom";
import { login } from "../utils/api.js";
import classes from "./AuthForm.module.css";
import { useActionState } from "react";

async function loginAction(prevFormState, formData) {
  const email = formData.get("email");
  const password = formData.get("password");

  const result = await login({ email, password });
  if (!result.success) {
    return { errors: [result.message], enteredValues: { email: email, password } };
  }
  return { success: true }
}

function AuthForm() {
  const [formState, formAction, pending] = useActionState(loginAction, {
    errors: null,
  });
  const data = useActionData();
  const navigation = useNavigation();

  const [searchParams] = useSearchParams();
  const isLogin = searchParams.get("mode") === "login";
  const isSubmitting = navigation.state === "submitting";

  return (
    <>
      <h1>{isLogin ? "Sign-Up" : "Login"}</h1>
      <form action={formAction} method="post" className={classes.form}>
        {data && data.errors && (
          <ul>
            {Object.values(data.errors).map((err) => (
              <li key={err}>{err}</li>
            ))}
          </ul>
        )}
        {data && data.message && <p>{data.message}</p>}
        <div className={classes.container}>
          {isLogin && (
            <p className={classes.name}>
              <label htmlFor="first-name">First name</label>
              <input id="first-name" type="text" name="first-name" required  />
            </p>
          )}
          {isLogin && (
            <p className={classes.name}>
              <label htmlFor="last-name">Last name</label>
              <input id="last-name" type="text" name="last-name" required />
            </p>
          )}
        </div>
        <p>
          <label htmlFor="email">Email</label>
          <input id="email" type="email" name="email" required defaultValue={formState.enteredValues?.email} />
        </p>
        <p>
          <label htmlFor="image">Password</label>
          <input id="password" type="password" name="password" required defaultValue={formState.enteredValues?.password}/>
        </p>
        <div className={classes.actions}>
          <Link to={`?mode=${isLogin ? "signup" : "login"}`}>
            {isLogin ? "Sign-up" : "Login"}
          </Link>
          <button disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "Save"}
          </button>
        </div>
      </form>
    </>
  );
}

export default AuthForm;
