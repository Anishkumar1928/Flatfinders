import { AuthProvider } from './Screen/ContextApi';
import AppNavigator from './Screen/AppNavigator';
import ContactCard from './Screen/Component/ContactCard'
const App = () => {
  return (
    <AuthProvider>
      <AppNavigator />
    </AuthProvider>  
  );   
};
export default App;
   