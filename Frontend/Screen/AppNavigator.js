import React, { useContext, useEffect } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NavigationContainer } from '@react-navigation/native';
import { ContextApi } from './ContextApi';
import LoginScreen from './LoginScreen';
import HomeScreen from './HomeScreen';
import RoomDetails from './RoomDetails';
import ProfileScreen from './ProfileScreen';
import SignupScreen from './SignupScreen';
import UpdateProfile from './UpdateProfile';
import PropertyRegistration from './PropertyRegistration'
import MypropertyScreen from './MypropertyScreen'
import ChangePasswordScreen from './ChangePassword'

const Stack = createNativeStackNavigator();

const AppNavigator = () => {
  const { isAuthenticated, setLoading } = useContext(ContextApi);

  useEffect(() => {
    console.log(`Authenticated ${isAuthenticated}`);
  });

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {isAuthenticated ? (
          <>
            <Stack.Screen
              name="Home"
              component={HomeScreen}
              options={{ headerShown: false }}
            />
            <Stack.Screen name="ProfileScreen" component={ProfileScreen} />
            <Stack.Screen name="RoomDetails" component={RoomDetails} />
            <Stack.Screen name="UpdateProfile" component={UpdateProfile} />
            <Stack.Screen name="propertyRegistration" component={PropertyRegistration} />
            <Stack.Screen name="MypropertyScreen" component={MypropertyScreen}/>
            <Stack.Screen name="ChangePassword" component={ChangePasswordScreen}/>
          </>
        ) : (
          <>
            <Stack.Screen
              name="Login"
              component={LoginScreen}
              options={{ headerShown: false }}
            />
            <Stack.Screen name="Signup" component={SignupScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
