import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { Driver } from './components/driver/Driver';

export default function App() {
  return (
    <Router>
      <Driver />
    </Router>
  );
}
