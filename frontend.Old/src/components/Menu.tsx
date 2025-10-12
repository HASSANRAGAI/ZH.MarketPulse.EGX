import React from 'react';
import { Link } from 'react-router-dom';
import './Menu.css';

const Menu: React.FC = () => {
  return (
    <nav className="menu">
      <ul>
        <li><Link to="/stocks">Stocks</Link></li>
        <li><Link to="/fair-values">Fair Values</Link></li>
        <li><Link to="/ipos">IPOs</Link></li>
      </ul>
    </nav>
  );
};

export default Menu;
