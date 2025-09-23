import { router } from './routes/AppRoutes.jsx';
import { RouterProvider } from 'react-router-dom';

export default function App() {

  return (
    <RouterProvider router={router} />
  )
}

