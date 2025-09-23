import { Outlet } from "react-router-dom";
import QuotesNavigation from "../components/QuotesNavigation.jsx";

export default function QuotesRootLayout() {
    return (
        <>  
            <QuotesNavigation />
            <Outlet />
        </>
    )
}