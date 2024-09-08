import React from 'react';
import { Form, Input, Radio, Button, Typography, message } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const EventForm: React.FC = () => {
    const [form] = Form.useForm();
    const navigate = useNavigate();

    const onFinish = async (values: any) => {
        try {
            await axios.post('http://localhost/add_task', values);
            message.success('Event added successfully');
            navigate('/tasks');
        } catch (error) {
            console.error('Error adding event:', error);
            message.error('Failed to add event');
        }
    };

    return (
        <div>
            <Title level={2}>Add New Event</Title>
            <Form form={form} onFinish={onFinish} layout="vertical">
                <Form.Item
                    name="eventName"
                    label="Event Name"
                    rules={[{ required: true, message: 'Please input the event name!' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="priority"
                    label="Priority"
                    rules={[{ required: true, message: 'Please select the priority!' }]}
                >
                    <Radio.Group>
                        {['High', 'Medium', 'Low'].map((option) => (
                            <Radio key={option} value={option}>
                                {option}
                            </Radio>
                        ))}
                    </Radio.Group>
                </Form.Item>

                <Form.Item
    name="duration"
    label="Duration"
    rules={[{ required: true, message: 'Please select the duration!' }]}
>
    <Radio.Group>
        {[30, 60, 120, 240].map((minutes) => (
            <Radio key={minutes} value={`${minutes}`}>
                {minutes === 60 ? '1 hour' : 
                 minutes === 120 ? '2 hours' : 
                 minutes === 240 ? '4 hours' : 
                 `${minutes} minutes`}
            </Radio>
        ))}
    </Radio.Group>
</Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Add Event
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default EventForm;