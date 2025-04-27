import React, { useEffect, useState } from "react";
//import BASE_URL from './settings'
import './base.css';
import './AccountPage.css';
import Header from './components/menu/Header';
import Footer from './components/all/Footer';

const BASE_URL = "http://192.168.1.42:8000";

export default function AccountPage({ personId }) {
  const [person, setPerson] = useState(null);
  const [isLoadingDelayed, setIsLoadingDelayed] = useState(false);

  useEffect(() => {
    const delayTimer = setTimeout(() => {
      setIsLoadingDelayed(true);
    }, 300); // 300 мс — сколько ждём перед показом "Загрузка..."

    fetch(`${BASE_URL}/api/v1/medcenter/account/person/${personId}`)
      .then(response => response.json())
      .then(data => {
        setPerson(data.data);
        clearTimeout(delayTimer); // если данные пришли быстро — убиваем таймер
      })
      .catch(error => {
        console.error('Ошибка при загрузке:', error);
        clearTimeout(delayTimer);
      });

    return () => clearTimeout(delayTimer); // на всякий случай чистим таймер при размонтировании
  }, [personId]);

  if (!person) {
    return isLoadingDelayed ? (
      <div className="p-4 text-center">Загрузка...</div>
    ) : null;
  }


  return (
    <div className="wrapper">
      <Header />

      <main className="account-main">
        <div className="account-container">
          <h1 className="account-title">Личный кабинет</h1>
          <div className="account-card">
            <div className="account-info">
              <p><strong>Имя:</strong> {person.first_name}</p>
              <p><strong>Фамилия:</strong> {person.last_name}</p>
              <p><strong>Отчество:</strong> {person.patronymic}</p>
              <p><strong>Дата рождения:</strong> {formatDate(person.date_birth)}</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('ru-RU', options);
}