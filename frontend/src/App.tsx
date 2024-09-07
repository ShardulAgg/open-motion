import React, {useState} from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

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
  const [view, setView] = useState('monthly');
  const customTheme = {
    algorithm: defaultAlgorithm,
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 6,
    },
  };

  return (
    <Router>
      <Layout>
        <Header style={{backgroundColor:'gray'}}>
          <div className="button-group">
            <Space direction="horizontal" size="small">
              <Typography.Title level={2} style={{ color: 'white' }}>September 2024</Typography.Title>
              <Link to="/events">
                <Button icon={<PlusOutlined />}>
                  Events
                </Button>
              </Link>
              <Link to="/calendar">
                <Button icon={<PlusOutlined />}>
                  Calendar
                </Button>
              </Link>
              <Link to="/add-task">
                <Button icon={<PlusOutlined />}>
                  Add New Task
                </Button>
              </Link>
              <Button onClick={() => {/* Sync logic */}}>
                Sync
              </Button>
            </Space>
          </div>
        </Header>
        <Content>
          <Routes>
            <Route path="/calendar" element={<Month />} />
            <Route path="/events" element={<Events />} />
            <Route path="/add-task" element={<Form />} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
};

export default App;
