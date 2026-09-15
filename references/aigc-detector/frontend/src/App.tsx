import { Layout, Grid } from 'antd';
import Detector from './components/Detector';

const { Header, Content } = Layout;
const { useBreakpoint } = Grid;

function App() {
  const screens = useBreakpoint();

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header
        style={{
          color: 'white',
          fontSize: screens.xs ? '14px' : screens.sm ? '16px' : '20px',
          textAlign: 'center',
          padding: screens.xs ? '0 8px' : screens.sm ? '0 12px' : '0 16px'
        }}
      >
        AI 文本检测助手
      </Header>
      <Content
        style={{
          padding: screens.xs ? '12px 8px' : screens.sm ? '16px 12px' : '24px 16px',
          maxWidth: '1200px',
          margin: '0 auto',
          width: '100%'
        }}
      >
        <Detector />
      </Content>
    </Layout>
  );
}

export default App;
