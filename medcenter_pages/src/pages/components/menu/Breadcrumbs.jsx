import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Breadcrumbs.css'; // Подключаем отдельный файл стилей

// Словарь для перевода частей пути
const pathNames = {
  account: 'Аккаунт',
  queue: 'Очередь',
  info: 'Об учреждении',
  admin: 'Администрирование',
  register: 'Регистрация',
  login: 'Вход',
  
};

export default function Breadcrumbs() {
  const location = useLocation();

  const crumbs = location.pathname
    .split('/')
    .filter(crumb => crumb !== '');

  let path = '';

  return (
    <nav className="breadcrumbs">
      <ul>
        <li><Link to="/">Главная</Link></li>
        {crumbs.map((crumb, index) => {
          path += `/${crumb}`;
          const isLast = index === crumbs.length - 1;
          const displayName = pathNames[crumb] || decodeURIComponent(crumb);

          return (
            <li key={path}>
              <span className="separator">/</span>
              {isLast ? (
                <span className="current">{displayName}</span>
              ) : (
                <Link to={path}>{displayName}</Link>
              )}
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
