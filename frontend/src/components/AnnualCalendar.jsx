import React, { useState } from 'react';

const AnnualCalendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());

  const renderCalendar = (date) => {
    const month = date.getMonth();
    const year = date.getFullYear();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    const monthYear = `${monthNames[month]} ${year}`;
    
    let dayOfWeek = firstDay.getDay();
    if (dayOfWeek === 0) dayOfWeek = 7;

    let calendarBody = [];
    let week = [];
    for (let i = 1; i < dayOfWeek; i++) {
      week.push(<td key={`empty-${i}`} className="border p-2"></td>);
    }

    for (let day = 1; day <= lastDay.getDate(); day++) {
      if (dayOfWeek > 7) {
        calendarBody.push(<tr key={`week-${calendarBody.length}`}>{week}</tr>);
        week = [];
        dayOfWeek = 1;
      }
      week.push(<td key={day} className="border p-2 text-center">{day}</td>);
      dayOfWeek++;
    }

    while (dayOfWeek <= 7) {
      week.push(<td key={`empty-end-${dayOfWeek}`} className="border p-2"></td>);
      dayOfWeek++;
    }
    calendarBody.push(<tr key={`week-end-${calendarBody.length}`}>{week}</tr>);

    return { monthYear, calendarBody };
  }

  const prevMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() - 1, 1));
  }

  const nextMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() + 1, 1));
  }

  const { monthYear, calendarBody } = renderCalendar(currentDate);

  return (
    <div className="w-full max-w-md border border-gray-300 rounded-lg shadow p-4 bg-white">
      <div className="flex justify-between items-center mb-4">
        <button className="text-gray-600 hover:text-gray-900" onClick={prevMonth}>‹</button>
        <span className="font-semibold text-lg">{monthYear}</span>
        <button className="text-gray-600 hover:text-gray-900" onClick={nextMonth}>›</button>
      </div>
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className="border p-2 text-center">Lun</th>
            <th className="border p-2 text-center">Mar</th>
            <th className="border p-2 text-center">Mié</th>
            <th className="border p-2 text-center">Jue</th>
            <th className="border p-2 text-center">Vie</th>
            <th className="border p-2 text-center">Sáb</th>
            <th className="border p-2 text-center">Dom</th>
          </tr>
        </thead>
        <tbody>
          {calendarBody}
        </tbody>
      </table>
    </div>
  );
};

export default AnnualCalendar;
