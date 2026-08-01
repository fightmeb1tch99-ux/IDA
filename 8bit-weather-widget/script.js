const weatherIcon = document.getElementById('weather-icon');
const cityEl = document.getElementById('city');
const tempEl = document.getElementById('temp');
const descEl = document.getElementById('desc');
const cityInput = document.getElementById('city-input');
const searchBtn = document.getElementById('search-btn');

async function fetchWeather(city = 'Moscow') {
    try {
        const response = await fetch(`https://wttr.in/${city}?format=j1`);
        if (!response.ok) throw new Error('City not found');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        cityEl.innerText = 'Ошибка';
        descEl.innerText = 'Город не найден';
        console.error(error);
    }
}

function updateUI(data) {
    const current = data.current_condition[0];
    const city = data.nearest_area[0].areaName[0].value;
    const temp = current.temp_C;
    const desc = current.lang_ru ? current.lang_ru[0].value : current.weatherDesc[0].value;
    const code = current.weatherCode;

    cityEl.innerText = city;
    tempEl.innerText = `${temp}°C`;
    descEl.innerText = desc;

    setAnimation(code);
}

function setAnimation(code) {
    weatherIcon.innerHTML = '';
    
    // Simple weather code mapping
    // 113: Sunny, 116: Partly Cloudy, 119: Cloudy, 122: Overcast
    // 263, 266, 293, 296, 299, 302, 305, 308: Rain
    // 386, 389: Storm
    // 227, 230, 323, 326, 329, 332, 335, 338: Snow

    const c = parseInt(code);

    if (c === 113) {
        // Sunny
        const sun = document.createElement('div');
        sun.className = 'sun';
        weatherIcon.appendChild(sun);
    } else if (c === 116 || c === 119 || c === 122) {
        // Cloudy
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        weatherIcon.appendChild(cloud);
    } else if ([263, 266, 293, 296, 299, 302, 305, 308].includes(c)) {
        // Rain
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        weatherIcon.appendChild(cloud);
        for (let i = 0; i < 5; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            drop.style.left = `${10 + i * 10}px`;
            drop.style.animationDelay = `${Math.random()}s`;
            weatherIcon.appendChild(drop);
        }
    } else if ([227, 230, 323, 326, 329, 332, 335, 338].includes(c)) {
        // Snow
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        weatherIcon.appendChild(cloud);
        for (let i = 0; i < 5; i++) {
            const flake = document.createElement('div');
            flake.className = 'snow-flake';
            flake.style.left = `${10 + i * 10}px`;
            flake.style.animationDelay = `${Math.random() * 2}s`;
            weatherIcon.appendChild(flake);
        }
    } else if ([386, 389].includes(c)) {
        // Storm
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        weatherIcon.appendChild(cloud);
        const bolt = document.createElement('div');
        bolt.className = 'lightning';
        weatherIcon.appendChild(bolt);
    } else {
        // Default to cloud
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        weatherIcon.appendChild(cloud);
    }
}

searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city) fetchWeather(city);
});

cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city) fetchWeather(city);
    }
});

// Initial fetch
fetchWeather();
