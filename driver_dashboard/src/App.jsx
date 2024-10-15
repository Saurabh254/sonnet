import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUpForm from './components/SignUpForm';
import LoginForm from './components/LoginForm'; // Assuming you have a login component
import { DriverHomePage, UserPage } from './components/HomePage';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/signup" element={<SignUpForm />} />
        <Route path="/homepage" element={<DriverHomePage />} />
        <Route path="/homepage/:driver_id" element={<UserPage />} />
      </Routes>
    </Router>
  );
}
