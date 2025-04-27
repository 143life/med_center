import React from 'react';
import { Link } from 'react-router-dom';
import Breadcrumbs from './Breadcrumbs';

export default function Header() {
    return (
        <header>
            <div className="header-left">
                <Breadcrumbs />

                <nav>
                    <ul>
                        <li><Link to="/info">Об учреждении</Link></li>
                        <li><Link to="/queue">Очередь</Link></li>
                        <li><Link to="/account">Аккаунт</Link></li>
                        <li><Link to="/admin">Административная панель</Link></li>
                    </ul>
                </nav>
            </div>
            <div className="auth">
                <Link to="/register">Регистрация</Link> / <Link to="/login">Вход</Link>
            </div>
        </header>
    );
}