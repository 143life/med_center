import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer>
            <ul>
                <li><Link to="/link1">Ссылка 1</Link></li>
                <li><Link to="/link2">Ссылка 2</Link></li>
                <li><Link to="/link3">Ссылка 3</Link></li>
            </ul>
            <p>Способы связи: email@example.com, +7 (XXX) XXX-XX-XX</p>
        </footer>
    )
}