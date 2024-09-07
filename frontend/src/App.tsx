import React, {useState} from 'react';
import { Layout, theme } from 'antd';
import logo from './logo.svg';
import { ConfigProvider } from 'antd';
import Month from './components/Month';
import Weekly from './components/Week';
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
    <Layout>
      <Header style={{backgroundColor:'gray'}}>
        <div className="button-group">
          <Space direction="horizontal" size="small">
          <Typography.Title level={2} style={{ color: 'white' }}>September 2024</Typography.Title>
            <Button 
              icon={<PlusOutlined />}
              onClick={() => {/* Add new task logic */}}
            >
              Add New Task
            </Button>
            <Button 
              onClick={() => {/* Sync logic */}}
            >
              Sync
            </Button>
          </Space>
        </div>
      </Header>
      <Content>
      <Space direction="horizontal" size="small">
            <Button 
              type={view === 'weekly' ? 'primary' : 'default'}
              onClick={() => setView('weekly')}
              disabled={view === 'weekly'}
            >
              Weekly View
            </Button>
            <Button 
              type={view === 'monthly' ? 'primary' : 'default'}
              onClick={() => setView('monthly')}
              disabled={view === 'monthly'}
            >
              Monthly View
            </Button>
            </Space>
        {view === 'weekly' ? <Weekly /> : <Month />}
      </Content>
    </Layout>
  );
};

export default App;
