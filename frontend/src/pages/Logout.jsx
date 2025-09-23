import { redirect } from "react-router-dom";

export function action() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return redirect('/');
}