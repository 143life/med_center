import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AccountPage from './pages/AccountPage'



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/account" element={<AccountPage personId={2}/>} />

      </Routes>
    </Router>
  );
}

export default App;
