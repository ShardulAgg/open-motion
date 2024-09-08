import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { UnorderedListOutlined, CalendarOutlined } from '@ant-design/icons';
import { Layout, theme } from 'antd';
import logo from './logo.svg';
import { ConfigProvider } from 'antd';
import Month from './components/Month';
import Events from './components/Events';
import Form from './components/Form';
import { Button, Space, Typography } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
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
  const customTheme = {
    algorithm: defaultAlgorithm,
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 6,
    },
  };
  const location = useLocation();

  return (
    <Layout>
      <Header style={{ backgroundColor: 'gray' }}>
        <div className="button-group">
          <Space direction="horizontal" size="small">
            <Typography.Title level={2} style={{ color: 'white' }}>September 2024</Typography.Title>
            <Link to="/">
              <Button
                icon={<CalendarOutlined />}
                type={location.pathname === '/' ? 'primary' : 'default'}
              >
                Calendar
              </Button>
            </Link>
            <Link to="/events">
              <Button
                icon={<UnorderedListOutlined />}
                type={location.pathname === '/events' ? 'primary' : 'default'}
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
            <Button onClick={() => {/* Sync logic */ }}>
              Sync
            </Button>
          </Space>
        </div>
      </Header>
      <Content>
        <Routes>
          <Route path="/events" element={<Events />} />
          <Route path="/add-task" element={<Form />} />
          <Route path="/" element={<Month />} />
        </Routes>
      </Content>
    </Layout>
  );
};

export default App;
