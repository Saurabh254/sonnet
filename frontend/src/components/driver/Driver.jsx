import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from '../common/LoginForm';
import SignUpForm from '../common/SignUpForm';
import { DriverHomePage } from './DriverHomePage';
import UserInfo from './UserInfo';

export const Driver = () => {
    return <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpForm />} />
        <Route path="/homepage" element={<DriverHomePage />} />
        <Route path="/homepage/:driver_id" element={<UserInfo />} />
    </Routes>
}