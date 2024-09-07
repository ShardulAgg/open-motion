import React, { useState, useEffect } from 'react';
import type { BadgeProps, CalendarProps } from 'antd';
import { Badge, Calendar } from 'antd';
import type { Dayjs } from 'dayjs';

interface CalendarEvent {
  kind: string;
  id: string;
  status: string;
  summary: string;
  description: string;
  start: {
    dateTime: string;
    timeZone: string;
  };
  end: {
    dateTime: string;
    timeZone: string;
  };
}

const Month: React.FC = () => {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://localhost/events');
        const data = await response.json();
        setEvents(data[0]);
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };

    fetchEvents();
  }, []);

  const getListData = (value: Dayjs) => {
    return events
      .filter(event => value.isSame(event.start.dateTime, 'day'))
      .map(event => ({
        type: event.description === 'open-motion' ? 'success' : 'processing',
        content: event.summary
      }));
  };

  const monthCellRender = (value: Dayjs) => {
    const num = value.month() === 8 ? 1394 : null;
    return num ? (
      <div className="notes-month">
        <section>{num}</section>
        <span>Backlog number</span>
      </div>
    ) : null;
  };

  const dateCellRender = (value: Dayjs) => {
    const listData = getListData(value);
    return (
      <ul className="events">
        {listData.map((item) => (
          <li key={item.content}>
            <Badge status={item.type as BadgeProps['status']} text={item.content} />
          </li>
        ))}
      </ul>
    );
  };

  const cellRender: CalendarProps<Dayjs>['cellRender'] = (current, info) => {
    if (info.type === 'date') return dateCellRender(current);
    if (info.type === 'month') return monthCellRender(current);
    return info.originNode;
  };

  return (
    <Calendar
      cellRender={cellRender}
      headerRender={({ value }) => (
        <div style={{ padding: '8px 0', textAlign: 'center' }}>
          {/* <h2>{`${value.format('MMMM')} ${value.format('YYYY')}`}</h2> */}
        </div>
      )}
    />
  );
};

export default Month;