import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUpForm from './components/common/SignUpForm';
import LoginForm from './components/common/LoginForm'; // Assuming you have a login component
import { DriverHomePage } from './components/driver/DriverHomePage';
import UserInfo from './components/driver/UserInfo';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/signup" element={<SignUpForm />} />
        <Route path="/homepage" element={<DriverHomePage />} />
        <Route path="/homepage/:driver_id" element={<UserInfo />} />
      </Routes>
    </Router>
  );
}
