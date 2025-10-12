import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Menu from './components/Menu';
import StocksPage from './pages/StocksPage';
import FairValuesPage from './pages/FairValuesPage';
import IPOsPage from './pages/IPOsPage';
import Newstockspage from './pages/newstockspage';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-layouts/styles/material.css';
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-react-grids/styles/material.css';
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Menu />
      <Routes>
        <Route path="/" element={<Navigate to="/stocks" />} />
        <Route path="/stocks" element={<StocksPage />} />
        <Route path="/fair-values" element={<FairValuesPage />} />
        <Route path="/ipos" element={<IPOsPage />} />
        <Route path="/new" element={<Newstockspage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
