const currentMonthElement = document.getElementById('currentMonth');
const calendarDaysElement = document.getElementById('calendarDays');
const prevMonthButton = document.getElementById('prevMonth');
const nextMonthButton = document.getElementById('nextMonth');
const eventPopup = document.getElementById('eventPopup');
const popupDate = document.getElementById('popupDate');
const eventList = document.getElementById('eventList');
const closeBtn = document.querySelector('.close-btn');

let currentDate = new Date();
let events = {};

function addEvent(date, eventName) {
    const key = date.toDateString();
    if (!events[key]) {
        events[key] = [];
    }
    events[key].push(eventName);
}

function updateCalendar() {
    currentMonthElement.textContent = currentDate.toLocaleString('pl', { month: 'long', year: 'numeric' });
    calendarDaysElement.innerHTML = '';

    const dayNames = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Nie'];
    dayNames.forEach(day => {
        const dayElement = document.createElement('div');
        dayElement.textContent = day;
        dayElement.classList.add('day-name');
        calendarDaysElement.appendChild(dayElement);
    });

    const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);

    let startIndex = firstDayOfMonth.getDay() - 1;
    if (startIndex === -1) startIndex = 6;

    for (let i = 0; i < startIndex; i++) {
        calendarDaysElement.appendChild(document.createElement('div'));
    }

    for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
        const dayElement = document.createElement('div');
        dayElement.textContent = day;

        const currentDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
        const key = currentDay.toDateString();

        if (events[key]) {
            dayElement.classList.add('event-day');
            const eventIndicator = document.createElement('span');
            eventIndicator.className = 'event-indicator';
            eventIndicator.title = events[key].join(', ');
            dayElement.appendChild(eventIndicator);
            dayElement.addEventListener('click', () => showEventPopup(currentDay, events[key]));
        }

        if (day === new Date().getDate() &&
            currentDate.getMonth() === new Date().getMonth() &&
            currentDate.getFullYear() === new Date().getFullYear()) {
            dayElement.classList.add('current-day');
        }

        calendarDaysElement.appendChild(dayElement);
    }

    const totalCells = 42;
    const filledCells = calendarDaysElement.children.length;
    for (let i = filledCells; i < totalCells; i++) {
        calendarDaysElement.appendChild(document.createElement('div'));
    }
}

function showEventPopup(date, eventsList) {
    popupDate.textContent = date.toLocaleDateString('pl', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    eventList.innerHTML = '';
    eventsList.forEach(event => {
        const li = document.createElement('li');
        li.textContent = event;
        eventList.appendChild(li);
    });
    eventPopup.style.display = 'block';
}

closeBtn.onclick = function() {
    eventPopup.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == eventPopup) {
        eventPopup.style.display = 'none';
    }
}

prevMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});

// Example usage of addEvent function
addEvent(new Date(2024, 6, 10), "Meeting with team");
addEvent(new Date(2024, 6, 15), "Kółko matematyczne, wielomiany. ");

updateCalendar();