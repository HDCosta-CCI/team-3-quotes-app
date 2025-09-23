import {
  Link,
  useSearchParams,
  useActionData,
  useNavigation,
  useNavigate
} from "react-router-dom";
import { login, signup } from "../utils/api.js";
import classes from "./AuthForm.module.css";
import { useActionState } from "react";

async function authAction(prevFormState, formData) {
  const mode = formData.get("mode");
  const email = formData.get("email");
  const password = formData.get("password");

  if (mode === "login") {
    const firstName = formData.get("first-name");
    const lastName = formData.get("last-name");

    const result = await signup({ email, password, firstName, lastName });

    if (!result.success) {
      return {
        errors: [result.message],
        enteredValues: { email, password, firstName, lastName },
      };
    }
    return { success: true };
  }

  const result = await login({ email, password });
  if (!result.success) {
    return { 
      errors: [result.message], 
      enteredValues: { email: email, password } };
  }
  return { success: true }
}

function AuthForm() {
  const [formState, formAction, pending] = useActionState(authAction, {
    errors: null,
  });
  const data = useActionData();
  const navigate = useNavigate();
  const navigation = useNavigation();

  const [searchParams] = useSearchParams();
  const isLogin = searchParams.get("mode") === "login";
  const isSubmitting = navigation.state === "submitting";

  if (formState?.success) {
    navigate("/"); 
  }

  return (
    <>
      <h1>{isLogin ? "Sign-Up" : "Login"}</h1>
      <form action={formAction} method="post" className={classes.form}>
        <input type="hidden" name="mode" value={isLogin ? "signup" : "login"} />
        {data && data.errors && (
          <ul>
            {Object.values(data.errors).map((err) => (
              <li key={err}>{err}</li>
            ))}
          </ul>
        )}
        {data && data.message && <p>{data.message}</p>}
        <div className={classes.container}>
          {!isLogin && (
            <p className={classes.name}>
              <label htmlFor="first-name">First name</label>
              <input id="first-name" type="text" name="first-name" required  />
            </p>
          )}
          {!isLogin && (
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
            {isLogin ? "New user? Sign up" : "Already have an account? Login"}
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
