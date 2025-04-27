// src/pages/HomePage.jsx
import React, { useState, useEffect, useRef } from 'react';
import './base.css';
import './HomePage.css';
import Header from './components/all/Header';
import Footer from './components/all/Footer';

const HomePage = () => {
  const [slideIndex, setSlideIndex] = useState(0);
  const sliderRef = useRef(null);
  const slidesRef = useRef([]);

  const nextSlide = () => {
    setSlideIndex((prevIndex) => (prevIndex + 1) % slidesRef.current.length);
  };

  const prevSlide = () => {
    setSlideIndex((prevIndex) => (prevIndex - 1 + slidesRef.current.length) % slidesRef.current.length);
  };

  useEffect(() => {
    const interval = setInterval(nextSlide, 5000); // автопрокрутка каждые 5 сек

    const updateSlider = () => {
      if (sliderRef.current && slidesRef.current.length > 0) {
        const slideWidth = slidesRef.current[0].offsetWidth;
        sliderRef.current.style.transition = 'transform 0.6s ease'; // плавная прокрутка
        sliderRef.current.style.transform = `translateX(-${slideIndex * slideWidth}px)`;
      }
    };

    updateSlider();
    window.addEventListener('resize', updateSlider);
    return () => {
      clearInterval(interval);
      window.removeEventListener('resize', updateSlider);
    };
  }, [slideIndex]);

  return (
    <div className="wrapper">
      <Header />

      <main>
        <div className="slider-container">
          <div className="slider" ref={sliderRef}>
            <div className="slide" ref={el => slidesRef.current[0] = el}>
              <h2>Доменное имя в автоматической установке гостевой ОС в Oracle VirtualBox</h2>
              <p>Доменное имя в автоматической установке гостевой ОС в Oracle VirtualBox не является строго необходимым. Однако, если доменное имя указано, это может упростить настройку сети и интеграцию гостевой ОС в существующую инфраструктуру.</p>
              <ul>
                <li><b>Настройки DNS:</b> Гостевая ОС может быть автоматически настроена для использования DNS-серверов домена.</li>
                <li><b>Интеграция с Active Directory:</b> Автоматическое присоединение к домену.</li>
                <li><b>Настройки сетевых служб:</b> Использование доменного имени для сетевых служб.</li>
              </ul>
              <p>Если доменное имя не указано, потребуется ручная настройка сети и DNS.</p>
            </div>
            <div className="slide" ref={el => slidesRef.current[1] = el}>
              <h2>Информация о ВУЗе - Слайд 2</h2>
              <p>Информация об образовательных программах и факультетах.</p>
            </div>
            <div className="slide" ref={el => slidesRef.current[2] = el}>
              <h2>Информация о ВУЗе - Слайд 3</h2>
              <p>Информация о научной деятельности и достижениях.</p>
            </div>
          </div>

          <div className="slider-nav">
            <button onClick={prevSlide}>&#10094;</button>
            <button onClick={nextSlide}>&#10095;</button>
          </div>
        </div>
        <div className="info-container">
          <h2>Lorem ipsum</h2>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            Donec faucibus sem a ante auctor suscipit. Vestibulum sit amet quam viverra, dictum sapien et, 
            finibus lectus. Integer accumsan consequat mauris vitae fringilla. Phasellus id nulla libero. 
            Sed tincidunt tincidunt ex eu commodo. In et lacus iaculis, malesuada urna nec, consectetur neque. Sed purus sem, 
            vestibulum at lobortis vitae, suscipit et lectus.
          </p>
          
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default HomePage;
