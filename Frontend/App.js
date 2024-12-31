import { AuthProvider } from './Screen/ContextApi';
import AppNavigator from './Screen/AppNavigator';
import ChangePasswordScreen from './Screen/ChangePassword'
const App = () => {
  return (
    <AuthProvider>
      <AppNavigator />
    </AuthProvider>  
  );   
};
export default App;
  