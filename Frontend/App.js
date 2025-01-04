import { AuthProvider } from './Screen/ContextApi';
import AppNavigator from './Screen/AppNavigator';
const App = () => {
  return (
    <AuthProvider>
      <AppNavigator />
    </AuthProvider>  
  );   
};
export default App;
   