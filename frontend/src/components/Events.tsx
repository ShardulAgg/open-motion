import React, { useState, useEffect } from 'react';
import { Typography, List } from 'antd';
import axios from 'axios';

const { Title } = Typography;

interface Task {
  "event-name": string;
  "event-priority": string;
  "event-duration": string;
}

const Events: React.FC = () => {
    const [tasks, setTasks] = useState<Task[]>([]);

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await axios.get('http://localhost/get_categorized_events');
                setTasks(response.data['open_motion_events']);
            } catch (error) {
                console.error('Error fetching tasks:', error);
            }
        };

        fetchTasks();
    }, []);

    return (
        <div>
        <Title level={1}>Events</Title>
        <List
            dataSource={tasks}
            renderItem={(task, index) => (
                <List.Item key={index}>
                    <List.Item.Meta
                        title={task["event-name"]}
                        description={
                            <>
                                <p>Priority: {task["event-priority"]}</p>
                                <p>Duration: {task["event-duration"]}</p>
                            </>
                        }
                    />
                </List.Item>
            )}
        />
    </div>
    );
};

export default Events;