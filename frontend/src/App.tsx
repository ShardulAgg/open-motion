import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { UnorderedListOutlined, CalendarOutlined, SyncOutlined } from '@ant-design/icons';
import { Layout, theme, message } from 'antd';
import { ConfigProvider } from 'antd';
import Month from './components/Month';
import Events from './components/Events';
import Form from './components/Form';
import { Button, Space, Typography } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import axios from 'axios';
import dayjs from 'dayjs';
const { defaultAlgorithm, darkAlgorithm } = theme;

const { Header, Content, Footer } = Layout;


function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

function AppContent() {
  const [view, setView] = useState('monthly');
  const [syncing, setSyncing] = useState(false);
  const customTheme = {
    algorithm: defaultAlgorithm,
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 6,
    },
  };
  const location = useLocation();
  const currentDate = dayjs().format('MMMM YYYY');

  const handleSync = async () => {
    setSyncing(true);
    try {
      await axios.post('http://localhost/sync');
      message.success('Events synchronized successfully');
      // Reload the current page to show updated events
      window.location.reload();
    } catch (error) {
      console.error('Error syncing events:', error);
      message.error('Failed to sync events. Please ensure you are authenticated.');
    } finally {
      setSyncing(false);
    }
  };

  return (
    <Layout>
      <Header style={{ backgroundColor: 'gray' }}>
        <div className="button-group">
          <Space direction="horizontal" size="small">
            <Typography.Title level={2} style={{ color: 'white' }}>{currentDate}</Typography.Title>
            <Link to="/">
              <Button
                icon={<CalendarOutlined />}
                type={location.pathname === '/' ? 'primary' : 'default'}
              >
                Calendar
              </Button>
            </Link>
            <Link to="/tasks">
              <Button
                icon={<UnorderedListOutlined />}
                type={location.pathname === '/tasks' ? 'primary' : 'default'}
              >
                Tasks
              </Button>
            </Link>
            <Link to="/add-task">
              <Button
                icon={<PlusOutlined />}
                type={location.pathname === '/add-task' ? 'primary' : 'default'}
              >
                Add New Task
              </Button>
            </Link>
            <Button
              icon={<SyncOutlined spin={syncing} />}
              onClick={handleSync}
              loading={syncing}
            >
              Sync
            </Button>
          </Space>
        </div>
      </Header>
      <Content>
        <Routes>
          <Route path="/tasks" element={<Events />} />
          <Route path="/add-task" element={<Form />} />
          <Route path="/" element={<Month />} />
        </Routes>
      </Content>
    </Layout>
  );
};

export default App;
