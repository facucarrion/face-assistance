import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const AnnualCalendar = () => {
  const [date, setDate] = useState(new Date());

  const handleDateChange = newDate => {
    setDate(newDate);
  };

  const months = Array.from({ length: 12 }, (_, i) => i);

  return (
    <div>
      {months.map(month => (
        <div key={month} style={{ marginBottom: '16px' }}>
          <h3>{new Date(2024, month).toLocaleString('default', { month: 'long' })}</h3>
          <Calendar
            onChange={handleDateChange}
            value={date}
          />
        </div>
      ))}
    </div>
  );
};

export default AnnualCalendar;